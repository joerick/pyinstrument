from optparse import OptionParser
import sys
import os
import codecs
from pyinstrument import Profiler
from pyinstrument.profiler import SignalUnavailableError

# Python 3 compatibility. Mostly borrowed from SymPy
PY3 = sys.version_info[0] > 2

if PY3:
    import builtins
    exec_ = getattr(builtins, "exec")
else:
    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("exec _code_ in _globs_, _locs_")

def main():
    usage = ("usage: pyinstrument [options] scriptfile [arg] ...")
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False

    parser.add_option('', '--setprofile',
        dest='setprofile', action='store_true',
        help='run in setprofile mode, instead of signal mode', default=False)

    parser.add_option('', '--html',
        dest="output_html", action='store_true',
        help="output HTML instead of text", default=False)
    parser.add_option('-o', '--outfile',
        dest="outfile", action='store',
        help="save report to <outfile>", default=None)

    parser.add_option('', '--unicode',
        dest='unicode', action='store_true',
        help='force unicode text output')
    parser.add_option('', '--no-unicode',
        dest='unicode', action='store_false',
        help='force ascii text output')

    parser.add_option('', '--color',
        dest='color', action='store_true',
        help='force ansi color text output')
    parser.add_option('', '--no-color',
        dest='color', action='store_false',
        help='force no color text output')

    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(2)

    (options, args) = parser.parse_args()
    sys.argv[:] = args

    if len(args) > 0:
        progname = args[0]
        sys.path.insert(0, os.path.dirname(progname))

        with open(progname, 'rb') as fp:
            code = compile(fp.read(), progname, 'exec')
        globs = {
            '__file__': progname,
            '__name__': '__main__',
            '__package__': None,
        }

        try:
            profiler = Profiler(use_signal=not options.setprofile)
        except SignalUnavailableError:
            profiler = Profiler(use_signal=False)

        profiler.start()

        try:
            exec_(code, globs, None)
        except IOError as e:
            import errno

            if e.errno == errno.EINTR:
                print(
                    'Failed to run program due to interrupted system system call.\n'
                    'This happens because pyinstrument is sending OS signals to the running\n'
                    'process to interrupt it. If your program has long-running syscalls this\n'
                    'can cause a problem.\n'
                    '\n'
                    'You can avoid this error by running in \'setprofile\' mode. Do this by\n'
                    'passing \'--setprofile\' when calling pyinstrument at the command-line.\n'
                    '\n'
                    'For more information, see\n'
                    'https://github.com/joerick/pyinstrument/issues/16\n'
                )

            raise
        except (SystemExit, KeyboardInterrupt):
            pass

        profiler.stop()

        if options.outfile:
            f = codecs.open(options.outfile, 'w', 'utf-8')
        else:
            f = sys.stdout

        unicode_override = options.unicode != None
        color_override = options.color != None

        unicode = options.unicode if unicode_override else file_supports_unicode(f)
        color = options.color if color_override else file_supports_color(f)

        if options.output_html:
            f.write(profiler.output_html())
        else:
            f.write(profiler.output_text(unicode=unicode, color=color))

        f.close()
    else:
        parser.print_usage()
    return parser

def file_supports_color(file_obj):
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)

    is_a_tty = hasattr(file_obj, 'isatty') and file_obj.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

def file_supports_unicode(file_obj):
    encoding = getattr(file_obj, 'encoding', None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    if 'utf' in codec_info.name:
        return True
    return False

if __name__ == '__main__':
    main()
