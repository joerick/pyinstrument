import asyncio
import threading
import urllib.parse
from ast import parse
from textwrap import dedent

import IPython
from IPython import get_ipython  # type: ignore
from IPython.core.magic import Magics, line_cell_magic, magics_class, no_var_expand
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import IFrame, display

from .. import Profiler

_active_profiler = None

_ASYNCIO_HTML_WARNING = """
To enable asyncio mode, use <pre>%%pyinstrument --async_mode=enabled</pre><br>
Note that due to IPython limitations this will run in a separate thread!
""".strip()
_ASYNCIO_TEXT_WARNING = (
    _ASYNCIO_HTML_WARNING.replace("<pre>", "`").replace("</pre>", "`").replace("<br>", "\n")
)

from collections import namedtuple

Option = namedtuple(
    "Option", "short, long, dest, action, metavar, default, help, callback, type".split(", ")
)


class ParserRecorder:
    _options: dict

    def __init__(self, /):
        self._options = {}

    def arguments(self, skip=[]):
        """
        Apply the recorded arguments as options for this magic, except the one in `skip`.
        """
        acc = []
        for key, opt in self._options.items():
            print("key...", key)
            if key in skip:
                print(
                    "skip",
                )
                continue
            if opt.action == "callback":
                continue

            type_as_type = {"string": str}.get(opt.type, opt.type)
            if opt.short:
                assert len(opt.short) >= 2, opt.short
                if opt.long:
                    args = (opt.short, opt.long)
                else:
                    args = (opt.short,)
            else:
                assert len(opt.long) >= 2
                args = (opt.long,)
            kwargs = dict(
                dest=opt.dest,
                action=opt.action,
                metavar=opt.metavar,
                default=opt.default,
                help=opt.help,
                type=type_as_type,
            )
            if opt.action in ["store_true", "store_false"]:
                assert kwargs["metavar"] is None
                del kwargs["metavar"]
                assert kwargs["type"] in (bool, None), kwargs
                del kwargs["type"]
            print("apply", kwargs)
            acc.append(argument(*args, **kwargs))

        def inner(f):
            for dec in acc:
                f = dec(f)
            return f

        return inner

    def add_option(
        self,
        short,
        long,
        /,
        action,
        help,
        dest=None,
        metavar=None,
        default=None,
        callback=None,
        type=None,
    ):
        key = long if long else short
        assert key not in self._options
        self._options[key] = Option(
            short,
            long,
            dest=dest,
            action=action,
            default=default,
            help=help,
            metavar=metavar,
            callback=callback,
            type=type,
        )


from pyinstrument.__main__ import _define_options

pr = ParserRecorder()
_define_options(pr)
# for opt, val in pr._options.items():
# print(opt, "\n   ", val)


def _get_active_profiler():
    """
    Allows the code inserted into the cell to access the pyinstrument Profiler
    instance, to start/stop it.
    """
    return _active_profiler


@magics_class
class PyinstrumentMagic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        if IPython.version_info < (8, 15):  # type: ignore
            from ._utils import PrePostAstTransformer

            # This will leak _get_active_profiler into the users space until we can magle it
            pre = parse(
                "\nfrom pyinstrument.magic.magic import _get_active_profiler; _get_active_profiler().start()\n"
            )
            post = parse("\n_get_active_profiler().stop()")
            self._transformer = PrePostAstTransformer(pre, post)
        else:
            from IPython.core.magics.ast_mod import ReplaceCodeTransformer  # type: ignore

            self._transformer = ReplaceCodeTransformer.from_string(
                dedent(
                    """
            from pyinstrument.magic.magic import _get_active_profiler as ___get_prof
            ___get_prof().start()
            try:
                __code__
            finally:
                ___get_prof().stop()
            __ret__
            """
                )
            )

    @magic_arguments()
    @pr.arguments()
    @argument(
        "--async_mode",
        default="disabled",
        help="Configures how this Profiler tracks time in a program that uses async/await. See: https://pyinstrument.readthedocs.io/en/latest/reference.html#pyinstrument.Profiler.async_mode",
    )
    @argument(
        "-h",
        "--height",
        default=400,
        help="Output height",
    )
    @argument(
        "code",
        type=str,
        nargs="*",
        help="When used as a line magic, the code to profile",
    )
    @no_var_expand
    @line_cell_magic
    def pyinstrument(self, line, cell=None):
        """
        Run a cell with the pyinstrument statistical profiler.

        Converts the line/cell's AST to something like:
            try:
                profiler.start()
                run_code
            finally:
                profiler.stop()
            profiler.output_html()
        """
        global _active_profiler
        args = parse_argstring(self.pyinstrument, line)
        ip = get_ipython()

        if not ip:
            raise RuntimeError("couldn't get ipython shell instance")

        code = cell or line

        if not code:
            return

        # Turn off the last run (e.g. a user interrupted)
        if _active_profiler and _active_profiler.is_running:
            _active_profiler.stop()
        if self._transformer in ip.ast_transformers:
            ip.ast_transformers.remove(self._transformer)

        _active_profiler = Profiler(
            interval=args.interval,
            async_mode=args.async_mode,
            use_timing_thread=args.use_timing_thread,
        )
        ip.ast_transformers.append(self._transformer)
        if args.async_mode == "disabled":
            cell_result = ip.run_cell(code)
        else:
            cell_result = self.run_cell_async(ip, code)
        mangled_keys = [k for k in ip.user_ns.keys() if "-" in k]
        for k in mangled_keys:
            del ip.user_ns[k]
        ip.ast_transformers.remove(self._transformer)

        if (
            args.async_mode == "disabled"
            and cell_result.error_in_exec
            and isinstance(cell_result.error_in_exec, RuntimeError)
            and "event loop is already running" in str(cell_result.error_in_exec)
        ):
            # if the cell is async, the Magic doesn't work, raising the above
            # exception instead. We display a warning and return.
            display(
                {
                    "text/plain": _ASYNCIO_TEXT_WARNING,
                    "text/html": _ASYNCIO_HTML_WARNING,
                },
                raw=True,
            )
            return

        html = _active_profiler.output_html(timeline=args.timeline)

        as_iframe = IFrame(
            src="data:text/html, " + urllib.parse.quote(html),
            width="100%",
            height=args.height,
            extras=['style="resize: vertical"'],
        )
        as_text = _active_profiler.output_text(timeline=args.timeline)
        # repr_html may be a bit fragile, but it's been stable for a while
        display({"text/html": as_iframe._repr_html_(), "text/plain": as_text}, raw=True)  # type: ignore

        assert not _active_profiler.is_running
        _active_profiler = None

    def run_cell_async(self, ip, code):
        # This is a bit of a hack, but it's the only way to get the cell to run
        # asynchronously. We need to run the cell in a separate thread, and then
        # wait for it to finish.
        #
        # Please keep an eye on this issue to see if there's a better way:
        # https://github.com/ipython/ipython/issues/11314
        old_loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        try:
            threading.Thread(target=loop.run_forever).start()
            asyncio.set_event_loop(loop)
            coro = ip.run_cell_async(code)
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            return future.result().result
        finally:
            loop.call_soon_threadsafe(loop.stop)
            asyncio.set_event_loop(old_loop)
