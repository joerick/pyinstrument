from __future__ import print_function

import urllib.parse
from ast import parse

from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import IFrame, display

from .. import Profiler
from ._utils import PrePostAstTransformer

_active_profiler = None


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
        default="enabled",
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
        ip.run_cell(code)
        ip.ast_transformers.remove(self._transformer)

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
