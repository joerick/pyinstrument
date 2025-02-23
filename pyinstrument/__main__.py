from __future__ import annotations

import fnmatch
import glob
import json
import optparse
import os
import runpy
import shutil
import sys
import time
from typing import Any, List, TextIO, cast

import pyinstrument
from pyinstrument import Profiler, renderers
from pyinstrument.session import Session
from pyinstrument.util import (
    file_is_a_tty,
    file_supports_color,
    file_supports_unicode,
    object_with_import_path,
)
from pyinstrument.vendor import appdirs, keypath

# pyright: strict
# pyright: reportUnknownMemberType=false


def main():
    usage = "usage: pyinstrument [options] scriptfile [arg] ..."
    version_string = "pyinstrument {v}, on Python {pyv[0]}.{pyv[1]}.{pyv[2]}".format(
        v=pyinstrument.__version__,
        pyv=sys.version_info,
    )
    parser: Any = optparse.OptionParser(usage=usage, version=version_string)
    parser.allow_interspersed_args = False

    def store_and_consume_remaining(
        option: optparse.Option, opt: str, value: str, parser: optparse.OptionParser
    ):
        """
        A callback for optparse that stores the value and consumes all
        remaining arguments, storing them in the same variable as a tuple.
        """

        # assert a few things we know to be true about the parser
        assert option.dest
        assert parser.rargs is not None
        assert parser.largs is not None

        # everything after this argument should be consumed
        remaining_arguments = parser.rargs + parser.largs
        parser.rargs[:] = []
        parser.largs[:] = []

        setattr(parser.values, option.dest, ValueWithRemainingArgs(value, remaining_arguments))

    parser.add_option(
        "--load",
        dest="load",
        action="store",
        metavar="FILENAME",
        help="instead of running a script, load a profile session from a pyisession file",
    )

    parser.add_option(
        "",
        "--load-prev",
        dest="load_prev",
        action="store",
        metavar="IDENTIFIER",
        help="instead of running a script, load a previous profile session as specified by an identifier",
    )

    parser.add_option(
        "-m",
        "",
        dest="module",
        action="callback",
        callback=store_and_consume_remaining,
        type="string",
        help="run library module as a script, like 'python -m module'",
    )
    parser.add_option(
        "-c",
        "",
        dest="program",
        action="callback",
        callback=store_and_consume_remaining,
        type="string",
        help="program passed in as string, like 'python -c \"...\"'",
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
            "how the report should be rendered. One of: 'text', 'html', 'json', 'speedscope', "
            "'pyisession', 'pstats', or python import path to a renderer class. Defaults to "
            "the appropriate format for the extension if OUTFILE is given, otherwise, defaults "
            "to 'text'."
        ),
        default=None,
    )

    parser.add_option(
        "-p",
        "--render-option",
        dest="render_options",
        action="append",
        metavar="RENDER_OPTION",
        type="string",
        help=(
            "options to pass to the renderer, in the format 'flag_name' or 'option_name=option_value'. "
            "For example, to set the option 'time', pass '-p time=percent_of_total'. To pass multiple "
            "options, use the -p option multiple times. You can set processor options using dot-syntax, "
            "like '-p processor_options.filter_threshold=0'. option_value is parsed as a JSON value or "
            "a string."
        ),
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
        default=False,
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
    parser.add_option(
        "-i",
        "--interval",
        action="store",
        type=float,
        help=(
            "Minimum time, in seconds, between each stack sample. Smaller values "
            "allow resolving shorter duration function calls but incur a "
            "greater runtime and memory consumption overhead. For longer running "
            "scripts, setting a larger interval reduces the memory consumption "
            "required to store the stack samples."
        ),
        default=0.001,
    )
    parser.add_option(
        "",
        "--use-timing-thread",
        dest="use_timing_thread",
        action="store_true",
        help=(
            "Use a separate thread to time the interval between stack samples. "
            "This can reduce the overhead of sampling on some systems."
        ),
    )

    # parse the options

    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(2)

    options, args = parser.parse_args()  # type: ignore

    # make command line options type-checked
    options = cast(CommandLineOptions, options)
    # work around a type checking bug...
    args = cast(List[str], args)  # type: ignore

    session_options_used = [
        options.load is not None,
        options.load_prev is not None,
        options.module is not None,
        options.program is not None,
        len(args) > 0,
    ]
    if session_options_used.count(True) == 0:
        parser.print_help()
        sys.exit(2)
    if session_options_used.count(True) > 1:
        parser.error("You can only specify one of --load, --load-prev, -m, or script arguments")

    if options.module is not None and options.from_path:
        parser.error("The options -m and --from-path are mutually exclusive.")

    if options.from_path and sys.platform == "win32":
        parser.error("--from-path is not supported on Windows")

    renderer_class = get_renderer_class(options)

    # open the output file

    if options.outfile:
        f = open(
            options.outfile,
            "w",
            encoding="utf-8",
            errors="surrogateescape",
            newline="" if renderer_class.output_is_binary else None,
        )
        should_close_f_after_writing = True
    else:
        f = sys.stdout
        should_close_f_after_writing = False

    inner_exception = None

    # create the renderer

    try:
        renderer = create_renderer(renderer_class, options, output_file=f)
    except OptionsParseError as e:
        parser.error(e.args[0])
        exit(1)

    if renderer.output_is_binary and not options.outfile and file_is_a_tty(f):
        parser.error(
            "Can't write binary output to a terminal. Redirect to a file or use --outfile."
        )
        exit(1)

    # get the session - execute code or load from disk

    if options.load_prev:
        session = load_report_from_temp_storage(options.load_prev)
    elif options.load:
        session = Session.load(options.load)
    else:
        # we are running some code
        if options.module is not None:
            if not (sys.path[0] and os.path.samefile(sys.path[0], ".")):
                # when called with '-m', search the cwd for that module
                sys.path[0] = os.path.abspath(".")

            argv = [options.module.value] + options.module.remaining_args
            code = "run_module(modname, run_name='__main__', alter_sys=True)"
            globs = {"run_module": runpy.run_module, "modname": options.module.value}
        elif options.program is not None:
            argv = ["-c", *options.program.remaining_args]
            code = options.program.value
            globs = {"__name__": "__main__"}
            # set the first path entry to '' to match behaviour of python -c
            sys.path[0] = ""
        else:
            argv = args
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

        old_argv = sys.argv.copy()

        # there is no point using async mode for command line invocation,
        # because it will always be capturing the whole program, we never want
        # any execution to be <out-of-context>, and it avoids duplicate
        # profiler errors.
        profiler = Profiler(
            interval=options.interval,
            async_mode="disabled",
            use_timing_thread=options.use_timing_thread,
        )

        profiler.start(target_description=f'Program: {" ".join(argv)}')

        try:
            sys.argv[:] = argv
            exec(code, globs, None)
        except (SystemExit, KeyboardInterrupt) as e:
            inner_exception = e
        finally:
            sys.argv[:] = old_argv

        session = profiler.stop()

    if isinstance(renderer, renderers.HTMLRenderer) and not options.outfile and file_is_a_tty(f):
        # don't write HTML to a TTY, open in browser instead
        output_filename = renderer.open_in_browser(session)
        print("stdout is a terminal, so saved profile output to %s" % output_filename)
    else:
        f.write(renderer.render(session))
        if should_close_f_after_writing:
            f.close()

    if isinstance(renderer, renderers.ConsoleRenderer) and not options.outfile:
        _, report_identifier = save_report_to_temp_storage(session)
        print("To view this report with different options, run:")
        print("    pyinstrument --load-prev %s [options]" % report_identifier)
        print("")

    if inner_exception:
        # If the script raised an exception, re-raise it now to resume
        # the normal Python exception handling (printing the traceback, etc.)
        raise inner_exception


class OptionsParseError(Exception):
    pass


def compute_render_options(
    options: CommandLineOptions,
    renderer_class: type[renderers.Renderer],
    unicode_support: bool,
    color_support: bool,
) -> dict[str, Any]:
    """
    Given a list of `CommandLineOptions`, compute the
    rendering options for the given renderer.

    Raises an `OptionsParseError` if there is an error parsing the options.

    unicode_support:
        indicate whether the expected output supports unicode
    color_support:
        indicate whether the expected output supports color

    Both of these will be used to determine the  default of outputting unicode
    or color, but can be overridden with `options.color` and `option.unicode`.
    """

    # parse show/hide options
    if options.hide_fnmatch is not None and options.hide_regex is not None:
        raise OptionsParseError("You can‘t specify both --hide and --hide-regex")

    hide_regex: str | None
    show_regex: str | None
    if options.hide_fnmatch is not None:
        hide_regex = fnmatch.translate(options.hide_fnmatch)
    else:
        hide_regex = options.hide_regex

    show_options_used = [
        options.show_fnmatch is not None,
        options.show_regex is not None,
        options.show_all,
    ]
    if show_options_used.count(True) > 1:
        raise OptionsParseError("You can only specify one of --show, --show-regex and --show-all")

    if options.show_fnmatch is not None:
        show_regex = fnmatch.translate(options.show_fnmatch)
    elif options.show_all:
        show_regex = r".*"
    else:
        show_regex = options.show_regex

    render_options: dict[str, Any] = {}

    if issubclass(renderer_class, renderers.FrameRenderer):
        render_options["processor_options"] = {
            "hide_regex": hide_regex,
            "show_regex": show_regex,
        }

    if issubclass(renderer_class, renderers.ConsoleRenderer):
        unicode_override = options.unicode is not None
        color_override = options.color is not None
        unicode: Any = options.unicode if unicode_override else unicode_support
        color: Any = options.color if color_override else color_support

        render_options.update({"unicode": unicode, "color": color})

    if options.timeline:
        render_options["timeline"] = True
    if options.show_all:
        render_options["show_all"] = True

    # apply user options
    if options.render_options is not None:
        for renderer_option in options.render_options:
            key, sep, value = renderer_option.partition("=")

            if sep == "":
                # we're setting a flag, like `-p unicode`
                keypath.set_value_at_keypath(render_options, key, True)
            else:
                # it's a key=value structure
                try:
                    # try parsing as a JSON value
                    parsed_value = json.loads(value)
                except json.JSONDecodeError:
                    # otherwise treat it as a string
                    parsed_value = value

                keypath.set_value_at_keypath(render_options, key, parsed_value)

    return render_options


def create_renderer(
    renderer_class: type[renderers.Renderer], options: CommandLineOptions, output_file: TextIO
) -> renderers.Renderer:
    render_options = compute_render_options(
        options,
        renderer_class=renderer_class,
        unicode_support=file_supports_unicode(output_file),
        color_support=file_supports_color(output_file),
    )

    try:
        return renderer_class(**render_options)
    except (TypeError, renderers.Renderer.MisconfigurationError) as err:
        # TypeError is probably a bad renderer option, so we produce a nicer error message
        raise OptionsParseError(
            f"Failed to create {renderer_class.__name__}. Check your renderer options.\n  {err}\n"
        )


def get_renderer_class(options: CommandLineOptions) -> type[renderers.Renderer]:
    renderer = options.renderer

    if options.output_html:
        renderer = "html"

    if renderer is None and options.outfile:
        renderer = guess_renderer_from_outfile(options.outfile)

    if renderer is None:
        renderer = "text"

    if renderer == "text":
        return renderers.ConsoleRenderer
    elif renderer == "html":
        return renderers.HTMLRenderer
    elif renderer == "json":
        return renderers.JSONRenderer
    elif renderer == "speedscope":
        return renderers.SpeedscopeRenderer
    elif renderer == "pyisession" or renderer == "session":  # session is the old name
        return renderers.SessionRenderer
    elif renderer == "pstats":
        return renderers.PstatsRenderer
    else:
        try:
            return object_with_import_path(renderer)
        except (ValueError, ModuleNotFoundError, AttributeError) as err:
            # ValueError means we failed to import this object
            raise OptionsParseError(
                f"Failed to find renderer with name {renderer!r}.\n"
                "Options are text, html, json, speedscope, pstats or a Python\n"
                "import path to a Renderer class.\n"
                "\n"
                f"Underlying error: {err}\n"
            )


def guess_renderer_from_outfile(outfile: str) -> str | None:
    # ignore case of outfile
    outfile = outfile.lower()

    _, ext = os.path.splitext(outfile)

    if ext == ".txt":
        return "text"
    elif ext in [".html", ".htm"]:
        return "html"
    elif outfile.endswith(".speedscope.json"):
        return "speedscope"
    elif ext == ".json":
        return "json"
    elif ext == ".pyisession":
        return "session"
    elif ext == ".pstats":
        return "pstats"
    else:
        return None


def report_dir() -> str:
    data_dir = appdirs.user_data_dir("pyinstrument", "com.github.joerick")  # type: ignore
    report_dir = os.path.join(data_dir, "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir


def load_report_from_temp_storage(identifier: str) -> Session:
    """
    Returns the session referred to by identifier
    """
    path = os.path.join(report_dir(), identifier + ".pyisession")
    try:
        return Session.load(path)
    except FileNotFoundError:
        sys.exit(f"pyinstrument: Couldn't find a profile with identifier {identifier}")


def save_report_to_temp_storage(session: Session):
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


class CommandLineOptions:
    """
    A type that codifies the `options` variable.
    """

    module: ValueWithRemainingArgs | None
    program: ValueWithRemainingArgs | None
    load: str | None
    load_prev: str | None
    from_path: str | None
    hide_fnmatch: str | None
    show_fnmatch: str | None
    hide_regex: str | None
    show_regex: str | None
    show_all: bool
    output_html: bool
    outfile: str | None
    render_options: list[str] | None

    unicode: bool | None
    color: bool | None
    renderer: str | None
    timeline: bool
    interval: float
    use_timing_thread: bool | None


class ValueWithRemainingArgs:
    def __init__(self, value: str, remaining_args: list[str]):
        self.value = value
        self.remaining_args = remaining_args


if __name__ == "__main__":
    main()
