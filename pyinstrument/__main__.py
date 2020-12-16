import sys, os, codecs, runpy, tempfile, glob, time, fnmatch, optparse
import pyinstrument
from pyinstrument import Profiler, renderers
from pyinstrument.session import ProfilerSession
from pyinstrument.util import object_with_import_path
from pyinstrument.vendor.six import exec_, PY2
from pyinstrument.vendor import appdirs


def main():
    usage = ("usage: pyinstrument [options] scriptfile [arg] ...")
    version_string = 'pyinstrument {v}, on Python {pyv[0]}.{pyv[1]}.{pyv[2]}'.format(
        v=pyinstrument.__version__,
        pyv=sys.version_info,
    )
    parser = optparse.OptionParser(usage=usage, version=version_string)
    parser.allow_interspersed_args = False

    def dash_m_callback(option, opt, value, parser):
        parser.values.module_name = value
        # everything after the -m argument should be passed to that module
        parser.values.module_args = parser.rargs + parser.largs
        parser.rargs[:] = []
        parser.largs[:] = []

    parser.add_option('', '--load-prev',
        dest='load_prev', action='store', metavar='ID',
        help="Instead of running a script, load a previous report")

    parser.add_option('-m', '',
        dest='module_name', action='callback', callback=dash_m_callback,
        type="str",
        help="run library module as a script, like 'python -m module'")

    parser.add_option('-o', '--outfile',
        dest="outfile", action='store',
        help="save to <outfile>", default=None)

    parser.add_option('-r', '--renderer',
        dest='renderer', action='store', type='string',
        help=("how the report should be rendered. One of: 'text', 'html', 'json', or python "
              "import path to a renderer class"),
        default='text')

    parser.add_option('', '--html',
        dest="output_html", action='store_true',
        help=optparse.SUPPRESS_HELP, default=False)  # deprecated shortcut for --renderer=html

    parser.add_option('-t', '--timeline',
        dest='timeline', action='store_true',
        help="render as a timeline - preserve ordering and don't condense repeated calls")

    parser.add_option('', '--hide',
        dest='hide_fnmatch', action='store', metavar='EXPR',
        help=("glob-style pattern matching the file paths whose frames to hide. Defaults to "
              "'*{sep}lib{sep}*'.").format(sep=os.sep),
        default='*{sep}lib{sep}*'.format(sep=os.sep))
    parser.add_option('', '--hide-regex',
        dest='hide_regex', action='store', metavar='REGEX',
        help=("regex matching the file paths whose frames to hide. Useful if --hide doesn't give "
              "enough control."))

    parser.add_option('', '--show',
        dest='show_fnmatch', action='store', metavar='EXPR',
        help=("glob-style pattern matching the file paths whose frames to "
              "show, regardless of --hide or --hide-regex. For example, use "
              "--show '*/<library>/*' to show frames within a library that "
              "would otherwise be hidden."))
    parser.add_option('', '--show-regex',
        dest='show_regex', action='store', metavar='REGEX',
        help=("regex matching the file paths whose frames to always show. "
              "Useful if --show doesn't give enough control."))
    parser.add_option('', '--show-all',
        dest='show_all', action='store_true',
        help="show everything", default=False)

    parser.add_option('', '--unicode',
        dest='unicode', action='store_true',
        help='(text renderer only) force unicode text output')
    parser.add_option('', '--no-unicode',
        dest='unicode', action='store_false',
        help='(text renderer only) force ascii text output')

    parser.add_option('', '--color',
        dest='color', action='store_true',
        help='(text renderer only) force ansi color text output')
    parser.add_option('', '--no-color',
        dest='color', action='store_false',
        help='(text renderer only) force no color text output')

    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(2)

    options, args = parser.parse_args()

    if args == [] and options.module_name is None and options.load_prev is None:
        parser.print_help()
        sys.exit(2)

    if not options.hide_regex:
        options.hide_regex = fnmatch.translate(options.hide_fnmatch)
    
    if not options.show_regex and options.show_fnmatch:
        options.show_regex = fnmatch.translate(options.show_fnmatch)
     
    if options.show_all:
        options.show_regex = r'.*'

    if options.load_prev:
        session = load_report(options.load_prev)
    else:
        if options.module_name is not None:
            if not (sys.path[0] and os.path.samefile(sys.path[0], '.')):
                # when called with '-m', search the cwd for that module
                sys.path.insert(0, os.path.abspath('.'))

            sys.argv[:] = [options.module_name] + options.module_args
            code = "run_module(modname, run_name='__main__')"
            globs = {
                'run_module': runpy.run_module,
                'modname': options.module_name
            }
        else:
            sys.argv[:] = args
            progname = args[0]
            sys.path.insert(0, os.path.dirname(progname))
            with open(progname, 'rb') as fp:
                code = compile(fp.read(), progname, 'exec')
            globs = {
                '__file__': progname,
                '__name__': '__main__',
                '__package__': None,
            }

        profiler = Profiler()

        profiler.start()

        try:
            exec_(code, globs, None)
        except (SystemExit, KeyboardInterrupt):
            pass

        profiler.stop()
        session = profiler.last_session

    if options.output_html:
        options.renderer = 'html'

    output_to_temp_file = (options.renderer == 'html'
                           and not options.outfile
                           and file_is_a_tty(sys.stdout))

    if options.outfile:
        f = codecs.open(options.outfile, 'w', 'utf-8')
        should_close_f_after_writing = True
    elif not output_to_temp_file:
        if PY2:
            f = codecs.getwriter('utf-8')(sys.stdout)
        else:
            f = sys.stdout
        should_close_f_after_writing = False

    renderer_kwargs = {'processor_options': {
        'hide_regex': options.hide_regex,
        'show_regex': options.show_regex,
    }}

    if options.timeline is not None:
        renderer_kwargs['timeline'] = options.timeline

    if options.renderer == 'text':
        unicode_override = options.unicode != None
        color_override = options.color != None
        unicode = options.unicode if unicode_override else file_supports_unicode(f)
        color = options.color if color_override else file_supports_color(f)
        
        renderer_kwargs.update({'unicode': unicode, 'color': color})

    renderer_class = get_renderer_class(options.renderer)
    renderer = renderer_class(**renderer_kwargs)

    # remove this frame from the trace
    renderer.processors.append(remove_first_pyinstrument_frame_processor)


    if output_to_temp_file:
        output_filename = renderer.open_in_browser(session)
        print('stdout is a terminal, so saved profile output to %s' % output_filename)
    else:
        f.write(renderer.render(session))
        if should_close_f_after_writing:
            f.close()

    if options.renderer == 'text':
        _, report_identifier = save_report(session)
        print('To view this report with different options, run:')
        print('    pyinstrument --load-prev %s [options]' % report_identifier)
        print('')


def file_supports_color(file_obj):
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return (supported_platform and is_a_tty)


def file_supports_unicode(file_obj):
    encoding = getattr(file_obj, 'encoding', None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return ('utf' in codec_info.name)


def file_is_a_tty(file_obj):
    return hasattr(file_obj, 'isatty') and file_obj.isatty()


def get_renderer_class(renderer):
    if renderer == 'text':
        return renderers.ConsoleRenderer
    elif renderer == 'html':
        return renderers.HTMLRenderer
    elif renderer == 'json':
        return renderers.JSONRenderer
    else:
        return object_with_import_path(renderer)


def report_dir():
    data_dir = appdirs.user_data_dir('pyinstrument', 'com.github.joerick')
    report_dir = os.path.join(data_dir, 'reports')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return report_dir

def load_report(identifier=None):
    '''
    Returns the session referred to by identifier
    '''
    path = os.path.join(
        report_dir(),
        identifier + '.pyireport'
    )
    return ProfilerSession.load(path)

def save_report(session):
    '''
    Saves the session to a temp file, and returns that path.
    Also prunes the number of reports to 10 so there aren't loads building up.
    '''
    # prune this folder to contain the last 10 sessions
    previous_reports = glob.glob(os.path.join(report_dir(), '*.pyireport'))
    previous_reports.sort(reverse=True)
    while len(previous_reports) > 10:
        report_file = previous_reports.pop()
        os.remove(report_file)

    identifier = time.strftime('%Y-%m-%dT%H-%M-%S', time.localtime(session.start_time))

    path = os.path.join(
        report_dir(),
        identifier + '.pyireport'
    )
    session.save(path)
    return path, identifier

# pylint: disable=W0613
def remove_first_pyinstrument_frame_processor(frame, options):
    '''
    The first frame when using the command line is always the __main__ function. I want to remove
    that from the output.
    '''
    if frame is None:
        return None

    if 'pyinstrument' in frame.file_path and len(frame.children) == 1:
        frame = frame.children[0]
        frame.remove_from_parent()
        return frame

    return frame


if __name__ == '__main__':
    main()
