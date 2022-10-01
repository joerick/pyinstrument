import asyncio
import threading
import urllib.parse
from ast import parse

from IPython import get_ipython  # type: ignore
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import IFrame, display

from .. import Profiler
from ._utils import PrePostAstTransformer

_active_profiler = None

_ASYNCIO_HTML_WARNING = """
To enable asyncio mode, use <pre>%%pyinstrument --async_mode=enabled</pre><br>
Note that due to IPython limitations this will run in a separate thread!
""".strip()
_ASYNCIO_TEXT_WARNING = (
    _ASYNCIO_HTML_WARNING.replace("<pre>", "`").replace("</pre>", "`").replace("<br>", "\n")
)


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
        # This will leak _get_active_profiler into the users space until we can magle it
        self.pre = parse(
            "\nfrom pyinstrument.magic.magic import _get_active_profiler; _get_active_profiler().start()\n"
        )
        self.post = parse("\n_get_active_profiler().stop()")
        self._transformer = PrePostAstTransformer(self.pre, self.post)

    @magic_arguments()
    @argument(
        "--interval",
        type=float,
        default=0.001,
        help="The minimum time, in seconds, between each stack sample. See: https://pyinstrument.readthedocs.io/en/latest/reference.html#pyinstrument.Profiler.interval",
    )
    @argument(
        "--async_mode",
        default="disabled",
        help="Configures how this Profiler tracks time in a program that uses async/await. See: https://pyinstrument.readthedocs.io/en/latest/reference.html#pyinstrument.Profiler.async_mode",
    )
    @argument(
        "--height",
        "-h",
        default=400,
        help="Output height",
    )
    @argument(
        "--timeline",
        type=bool,
        default=False,
        help="Show output timeline view",
    )
    @argument(
        "code",
        type=str,
        nargs="*",
        help="When used as a line magic, the code to profile",
    )
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

        _active_profiler = Profiler(interval=args.interval, async_mode=args.async_mode)
        ip.ast_transformers.append(self._transformer)
        if args.async_mode == "disabled":
            cell_result = ip.run_cell(code)
        else:
            cell_result = self.run_cell_async(ip, code)
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
        display({"text/html": as_iframe._repr_html_(), "text/plain": as_text}, raw=True)

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
