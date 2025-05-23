from __future__ import annotations

import asyncio
import html
import threading
import urllib.parse
from ast import parse
from textwrap import dedent

import IPython
from IPython import get_ipython  # type: ignore
from IPython.core.magic import Magics, line_cell_magic, magics_class, no_var_expand
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import IFrame, display

from pyinstrument import Profiler, renderers
from pyinstrument.__main__ import compute_render_options
from pyinstrument.frame import Frame
from pyinstrument.frame_ops import delete_frame_from_tree
from pyinstrument.processors import ProcessorOptions
from pyinstrument.renderers.console import ConsoleRenderer
from pyinstrument.renderers.html import HTMLRenderer

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


class InterruptSilently(Exception):
    """Exception used to interrupt execution without showing traceback"""


@magics_class
class PyinstrumentMagic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self._transformer = None

    def recreate_transformer(self, target_description: str):
        if IPython.version_info < (8, 15):  # type: ignore
            from ._utils import PrePostAstTransformer

            # This will leak _get_active_profiler into the users space until we can magle it
            pre = parse(
                dedent(
                    f"""
                    from pyinstrument.magic.magic import _get_active_profiler
                    _get_active_profiler().start(target_description={target_description!r})
                    """
                )
            )
            post = parse("\n_get_active_profiler().stop()")
            self._transformer = PrePostAstTransformer(pre, post)
        else:
            from IPython.core.magics.ast_mod import ReplaceCodeTransformer  # type: ignore

            self._transformer = ReplaceCodeTransformer.from_string(
                dedent(
                    f"""
                    from pyinstrument.magic.magic import _get_active_profiler as ___get_prof
                    ___get_prof().start(target_description={target_description!r})
                    try:
                        __code__
                    finally:
                        ___get_prof().stop()
                    __ret__
                    """
                )
            )

    @magic_arguments()
    @argument(
        "-p",
        "--render-option",
        dest="render_options",
        action="append",
        metavar="RENDER_OPTION",
        type=str,
        help=(
            "options to pass to the renderer, in the format 'flag_name' or 'option_name=option_value'. "
            "For example, to set the option 'time', pass '-p time=percent_of_total'. To pass multiple "
            "options, use the -p option multiple times. You can set processor options using dot-syntax, "
            "like '-p processor_options.filter_threshold=0'. option_value is parsed as a JSON value or "
            "a string."
        ),
    )
    @argument(
        "--show-regex",
        dest="show_regex",
        action="store",
        metavar="REGEX",
        help=(
            "regex matching the file paths whose frames to always show. "
            "Useful if --show doesn't give enough control."
        ),
    )
    @argument(
        "--show",
        dest="show_fnmatch",
        action="store",
        metavar="EXPR",
        help=(
            "glob-style pattern matching the file paths whose frames to "
            "show, regardless of --hide or --hide-regex. For example, use "
            "--show '*/<library>/*' to show frames within a library that "
            "would otherwise be hidden."
        ),
    )
    @argument(
        "--interval",
        type=float,
        default=0.001,
        help="The minimum time, in seconds, between each stack sample. See: https://pyinstrument.readthedocs.io/en/latest/reference.html#pyinstrument.Profiler.interval",
    )
    @argument(
        "--show-all",
        action="store_true",
        help="SHow all frames, including root frames with no time, and Internal IPython frames.",
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
    @argument(
        "--hide",
        dest="hide_fnmatch",
        action="store",
        metavar="EXPR",
        help=(
            "glob-style pattern matching the file paths whose frames to hide. Defaults to "
            "hiding non-application code"
        ),
    )
    @argument(
        "--hide-regex",
        dest="hide_regex",
        action="store",
        metavar="REGEX",
        help=(
            "regex matching the file paths whose frames to hide. Useful if --hide doesn't give "
            "enough control."
        ),
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

        # 2024, always override this  for now in IPython,
        # we can make an option later if necessary
        args.unicode = True
        args.color = True

        ip = get_ipython()

        if not ip:
            raise RuntimeError("couldn't get ipython shell instance")

        if cell:
            target_description = f"Cell [{ip.execution_count}]"
        else:
            target_description = f"Line in cell [{ip.execution_count}]"
        code = cell or line

        if not code:
            return

        # Turn off the last run (e.g. a user interrupted)
        if _active_profiler and _active_profiler.is_running:
            _active_profiler.stop()
        if self._transformer in ip.ast_transformers:
            ip.ast_transformers.remove(self._transformer)

        _active_profiler = Profiler(interval=args.interval, async_mode=args.async_mode)
        self.recreate_transformer(target_description=target_description)
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

        # If a KeyboardInterrupt occurred during the magic execution,
        # raise an exception to prevent further executions.
        if isinstance(cell_result.error_in_exec, KeyboardInterrupt):
            # The traceback is already shown during the cell execution above, so we
            # don't re-raise the exception directly.
            old_custom_tb = ip.CustomTB
            old_custom_exceptions = ip.custom_exceptions

            def _silent_exception_handler(self, etype, value, tb, tb_offset=None):
                # restore the original handlers
                ip.CustomTB = old_custom_tb
                ip.custom_exceptions = old_custom_exceptions
                # swallow the InterruptSilently entirely

            # install our silent handler
            ip.set_custom_exc((InterruptSilently,), _silent_exception_handler)
            raise InterruptSilently()

        html_config = compute_render_options(
            args, renderer_class=HTMLRenderer, unicode_support=True, color_support=True
        )

        text_config = compute_render_options(
            args, renderer_class=HTMLRenderer, unicode_support=True, color_support=True
        )

        html_renderer = renderers.HTMLRenderer(show_all=args.show_all, timeline=args.timeline)
        html_renderer.preprocessors.append(strip_ipython_frames_processor)
        html_str = _active_profiler.output(html_renderer)
        as_iframe = IFrame(
            src="data:text/html, Loading…",
            width="100%",
            height=args.height,
            extras=['style="resize: vertical"', f'srcdoc="{html.escape(html_str)}"'],
        )

        text_renderer = renderers.ConsoleRenderer(**text_config)
        text_renderer.processors.append(strip_ipython_frames_processor)

        as_text = _active_profiler.output(text_renderer)
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
            return future.result()
        finally:
            loop.call_soon_threadsafe(loop.stop)
            asyncio.set_event_loop(old_loop)


IPYTHON_INTERNAL_FILES = (
    "IPython/core/interactiveshell.py",
    "IPython/terminal/interactiveshell.py",
    "IPython/core/async_helpers.py",
    "IPython/terminal/ipapp.py",
    "traitlets/config/application.py",
    "ipython/IPython/__init__.py",
    "ipykernel/zmqshell",
    "pyinstrument/magic/magic.py",
)


def strip_ipython_frames_processor(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    A processor function that removes internal IPython nodes.
    """
    if frame is None:
        return None

    for child in frame.children:
        strip_ipython_frames_processor(child, options=options)

        if child.file_path is not None and any(
            f in child.file_path for f in IPYTHON_INTERNAL_FILES
        ):
            delete_frame_from_tree(child, replace_with="children")
            break

    return frame
