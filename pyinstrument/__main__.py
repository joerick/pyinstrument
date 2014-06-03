from optparse import OptionParser
import sys
import os
import codecs
from pyinstrument import Profiler
from pyinstrument.compat import exec_

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
    usage = "usage: %prog [-h] [-o output_file_path] scriptfile [arg] ..."
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False
    parser.add_option('', '--html',
        dest="output_html", action='store_true',
        help="output HTML instead of text", default=False)
    parser.add_option('-o', '--outfile',
        dest="outfile", action='store',
        help="save stats to <outfile>", default=None)

    if not sys.argv[1:]:
        parser.print_usage()
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

        profiler = Profiler()
        profiler.start()

        try:
            exec_(code, globs, None)
        except (SystemExit, KeyboardInterrupt):
            pass

        profiler.stop()

        if options.outfile:
            f = codecs.open(options.outfile, 'w', 'utf-8')
            unicode = True
            color = False
        else:
            f = sys.stdout
            unicode = stdout_supports_unicode()
            color = stdout_supports_color()

        if options.output_html:
            f.write(profiler.output_html())
        else:
            f.write(profiler.output_text(unicode=unicode, color=color))

        f.close()
    else:
        parser.print_usage()
    return parser

def stdout_supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)

    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

def stdout_supports_unicode():
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    utf_in_locale = 'utf' in os.environ.get('LC_CTYPE', '').lower()

    return is_a_tty and utf_in_locale

if __name__ == '__main__':
    main()
