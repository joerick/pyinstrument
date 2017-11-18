from optparse import OptionParser
import sys
import os
import codecs
from pyinstrument import Profiler
from pyinstrument.profiler import get_recorder_class, get_renderer_class
from .six import exec_


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
    parser.add_option('', '--flame',
        dest='output_flame', action='store_true',
        help='output an HTML flame chart', default=False)
    parser.add_option('-r', '--renderer',
        dest='output_renderer', action='store', type='string',
        help='python import path to a renderer class', default=None)

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

        if options.output_renderer:
            renderer = options.output_renderer
        elif options.output_html:
            renderer = 'html'
        else:
            renderer = 'text'

        recorder = get_renderer_class(renderer).preferred_recorder

        profiler = Profiler(recorder=recorder)

        profiler.start()

        try:
            exec_(code, globs, None)
        except (SystemExit, KeyboardInterrupt):
            pass

        profiler.stop()

        if options.outfile:
            f = codecs.open(options.outfile, 'w', 'utf-8')
        else:
            f = sys.stdout

        renderer_kwargs = {}

        if renderer == 'text':
            unicode_override = options.unicode != None
            color_override = options.color != None
            unicode = options.unicode if unicode_override else file_supports_unicode(f)
            color = options.color if color_override else file_supports_color(f)
            
            renderer_kwargs = {'unicode': unicode, 'color': color}

        f.write(profiler.output(renderer=renderer, **renderer_kwargs))
        f.close()
    else:
        parser.print_usage()


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
