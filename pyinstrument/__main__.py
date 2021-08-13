from __future__ import annotations

import codecs
import fnmatch
import glob
import optparse
import os
import runpy
import shutil
import sys
import time
from typing import Any, List, Type, cast

import pyinstrument
from pyinstrument import Profiler, renderers
from pyinstrument.frame import BaseFrame
from pyinstrument.processors import ProcessorOptions
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.session import Session
from pyinstrument.util import (
    file_is_a_tty,
    file_supports_color,
    file_supports_unicode,
    object_with_import_path,
)
from pyinstrument.vendor import appdirs

# pyright: strict


def main():
    usage = "usage: pyinstrument [options] scriptfile [arg] ..."
    version_string = "pyinstrument {v}, on Python {pyv[0]}.{pyv[1]}.{pyv[2]}".format(
        v=pyinstrument.__version__,
        pyv=sys.version_info,
    )
    parser = optparse.OptionParser(usage=usage, version=version_string)
    parser.allow_interspersed_args = False

    def dash_m_callback(option: str, opt: str, value: str, parser: optparse.OptionParser):
        parser.values.module_name = value  # type: ignore

        # everything after the -m argument should be passed to that module
        parser.values.module_args = parser.rargs + parser.largs  # type: ignore
        parser.rargs[:] = []  # type: ignore
        parser.largs[:] = []  # type: ignore

    parser.add_option(
        "",
        "--load-prev",
        dest="load_prev",
        action="store",
        metavar="ID",
        help="instead of running a script, load a previous report",
    )

    parser.add_option(
        "-m",
        "",
        dest="module_name",
        action="callback",
        callback=dash_m_callback,
        type="str",
        help="run library module as a script, like 'python -m module'",
    )
    parser.add_option(
        "",
        "--from-path",
        dest="from_path",
        action="store_true",
        help="(POSIX only) instead of the working directory, look for scriptfile in the PATH environment variable",
    )

    parser.add_option(
        "-o", "--outfile", dest="outfile", action="store", help="save to <outfile>", default=None
    )

    parser.add_option(
        "-r",
        "--renderer",
        dest="renderer",
        action="store",
        type="string",
        help=(
            "how the report should be rendered. One of: 'text', 'html', 'json', or python "
            "import path to a renderer class"
        ),
        default="text",
    )

    parser.add_option(
        "",
        "--html",
        dest="output_html",
        action="store_true",
        help=optparse.SUPPRESS_HELP,
        default=False,
    )  # deprecated shortcut for --renderer=html

    parser.add_option(
        "-t",
        "--timeline",
        dest="timeline",
        action="store_true",
        help="render as a timeline - preserve ordering and don't condense repeated calls",
    )

    parser.add_option(
        "",
        "--hide",
        dest="hide_fnmatch",
        action="store",
        metavar="EXPR",
        help=(
            "glob-style pattern matching the file paths whose frames to hide. Defaults to "
            "hiding non-application code"
        ),
    )
    parser.add_option(
        "",
        "--hide-regex",
        dest="hide_regex",
        action="store",
        metavar="REGEX",
        help=(
            "regex matching the file paths whose frames to hide. Useful if --hide doesn't give "
            "enough control."
        ),
    )

    parser.add_option(
        "",
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
    parser.add_option(
        "",
        "--show-regex",
        dest="show_regex",
        action="store",
        metavar="REGEX",
        help=(
            "regex matching the file paths whose frames to always show. "
            "Useful if --show doesn't give enough control."
        ),
    )
    parser.add_option(
        "",
        "--show-all",
        dest="show_all",
        action="store_true",
        help="show everything",
        default=False,
    )

    parser.add_option(
        "",
        "--unicode",
        dest="unicode",
        action="store_true",
        help="(text renderer only) force unicode text output",
    )
    parser.add_option(
        "",
        "--no-unicode",
        dest="unicode",
        action="store_false",
        help="(text renderer only) force ascii text output",
    )

    parser.add_option(
        "",
        "--color",
        dest="color",
        action="store_true",
        help="(text renderer only) force ansi color text output",
    )
    parser.add_option(
        "",
        "--no-color",
        dest="color",
        action="store_false",
        help="(text renderer only) force no color text output",
    )

    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(2)

    options, args = parser.parse_args()
    # work around a type checking bug...
    args = cast(List[str], args)

    if args == [] and options.module_name is None and options.load_prev is None:
        parser.print_help()
        sys.exit(2)

    if options.module_name is not None and options.from_path:
        parser.error("The options -m and --from-path are mutually exclusive.")

    if options.from_path and sys.platform == "win32":
        parser.error("--from-path is not supported on Windows")

    if options.hide_fnmatch is not None and options.hide_regex is not None:
        parser.error("You can‘t specify both --hide and --hide-regex")

    if options.hide_fnmatch is not None:
        options.hide_regex = fnmatch.translate(options.hide_fnmatch)

    show_options_used = [
        options.show_fnmatch is not None,
        options.show_regex is not None,
        options.show_all,
    ]
    if show_options_used.count(True) > 1:
        parser.error("You can only specify one of --show, --show-regex and --show-all")

    if options.show_fnmatch is not None:
        options.show_regex = fnmatch.translate(options.show_fnmatch)
    if options.show_all:
        options.show_regex = r".*"

    if options.load_prev:
        session = load_report(options.load_prev)
    else:
        if options.module_name is not None:
            if not (sys.path[0] and os.path.samefile(sys.path[0], ".")):
                # when called with '-m', search the cwd for that module
                sys.path[0] = os.path.abspath(".")

            sys.argv[:] = [options.module_name] + options.module_args
            code = "run_module(modname, run_name='__main__', alter_sys=True)"
            globs = {"run_module": runpy.run_module, "modname": options.module_name}
        else:
            sys.argv[:] = args
            if options.from_path:
                progname = shutil.which(args[0])
                if progname is None:
                    sys.exit(f"Error: program {args[0]} not found in PATH!")
            else:
                progname = args[0]
                if not os.path.exists(progname):
                    sys.exit(f"Error: program {args[0]} not found!")

            # Make sure we overwrite the first entry of sys.path ('.') with directory of the program.
            sys.path[0] = os.path.dirname(progname)

            code = "run_path(progname, run_name='__main__')"
            globs = {"run_path": runpy.run_path, "progname": progname}

        # there is no point using async mode for command line invocation,
        # because it will always be capturing the whole program, we never want
        # any execution to be <out-of-context>, and it avoids duplicate
        # profiler errors.
        profiler = Profiler(async_mode="disabled")

        profiler.start()

        try:
            exec(code, globs, None)
        except (SystemExit, KeyboardInterrupt):
            pass

        session = profiler.stop()

    if options.output_html:
        options.renderer = "html"

    if options.outfile:
        f = codecs.open(options.outfile, "w", "utf-8")
        should_close_f_after_writing = True
    else:
        f = sys.stdout
        should_close_f_after_writing = False

    renderer_kwargs = {
        "processor_options": {
            "hide_regex": options.hide_regex,
            "show_regex": options.show_regex,
        }
    }

    if options.timeline is not None:
        renderer_kwargs["timeline"] = options.timeline

    if options.renderer == "text":
        unicode_override = options.unicode is not None
        color_override = options.color is not None
        unicode: Any = options.unicode if unicode_override else file_supports_unicode(f)
        color: Any = options.color if color_override else file_supports_color(f)

        renderer_kwargs.update({"unicode": unicode, "color": color})

    renderer_class = get_renderer_class(options.renderer)
    renderer = renderer_class(**renderer_kwargs)

    # remove this frame from the trace
    renderer.processors.append(remove_first_pyinstrument_frame_processor)

    if isinstance(renderer, HTMLRenderer) and not options.outfile and file_is_a_tty(f):
        # don't write HTML to a TTY, open in browser instead
        output_filename = renderer.open_in_browser(session)
        print("stdout is a terminal, so saved profile output to %s" % output_filename)
    else:
        f.write(renderer.render(session))
        if should_close_f_after_writing:
            f.close()

    if options.renderer == "text":
        _, report_identifier = save_report(session)
        print("To view this report with different options, run:")
        print("    pyinstrument --load-prev %s [options]" % report_identifier)
        print("")


def get_renderer_class(renderer: str) -> Type[renderers.Renderer]:
    if renderer == "text":
        return renderers.ConsoleRenderer
    elif renderer == "html":
        return renderers.HTMLRenderer
    elif renderer == "json":
        return renderers.JSONRenderer
    else:
        return object_with_import_path(renderer)


def report_dir() -> str:
    data_dir: str = appdirs.user_data_dir("pyinstrument", "com.github.joerick")  # type: ignore
    report_dir = os.path.join(data_dir, "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir


def load_report(identifier: str) -> Session:
    """
    Returns the session referred to by identifier
    """
    path = os.path.join(report_dir(), identifier + ".pyisession")
    return Session.load(path)


def save_report(session: Session):
    """
    Saves the session to a temp file, and returns that path.
    Also prunes the number of reports to 10 so there aren't loads building up.
    """
    # prune this folder to contain the last 10 sessions
    previous_reports = glob.glob(os.path.join(report_dir(), "*.pyisession"))
    previous_reports.sort(reverse=True)
    while len(previous_reports) > 10:
        report_file = previous_reports.pop()
        os.remove(report_file)

    identifier = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))

    path = os.path.join(report_dir(), identifier + ".pyisession")
    session.save(path)
    return path, identifier


# pylint: disable=W0613
def remove_first_pyinstrument_frame_processor(
    frame: BaseFrame | None, options: ProcessorOptions
) -> BaseFrame | None:
    """
    The first frame when using the command line is always the __main__ function. I want to remove
    that from the output.
    """
    if frame is None:
        return None

    if frame.file_path is None:
        return frame

    if "pyinstrument" in frame.file_path and len(frame.children) == 1:
        frame = frame.children[0]
        frame.remove_from_parent()
        return frame

    return frame


if __name__ == "__main__":
    main()
