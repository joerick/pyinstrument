import sys, os, codecs, runpy, tempfile
from optparse import OptionParser
import pyinstrument
from pyinstrument import Profiler
from .six import exec_


def main():
    usage = ("usage: pyinstrument [options] scriptfile [arg] ...")
    version_string = 'pyinstrument {v}, on Python {pyv[0]}.{pyv[1]}.{pyv[2]}'.format(
        v=pyinstrument.__version__,
        pyv=sys.version_info,
    )
    parser = OptionParser(usage=usage, version=version_string)
    parser.allow_interspersed_args = False

    parser.add_option('-m', '',
        dest='module_name', action='store',
        help="run library module as a script, like 'python -m module'")

    parser.add_option('-r', '--renderer',
        dest='renderer', action='store', type='string',
        help="how the report should be rendered. One of: 'text', 'html', 'json', or python import path to a renderer class", 
        default='text')

    parser.add_option('', '--html',
        dest="output_html", action='store_true',
        help="Shortcut for '--renderer=html'", default=False)

    parser.add_option('-o', '--outfile',
        dest="outfile", action='store',
        help="save report to <outfile>", default=None)

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

    if args == [] and options.module_name is None:
        parser.print_help()
        sys.exit(2)

    if options.module_name is not None:
        sys.argv[:] = [options.module_name] + args
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

    if options.output_html:
        options.renderer = 'html'
    
    output_to_temp_file = (options.renderer == 'html'
                           and not options.outfile
                           and file_is_a_tty(sys.stdout))

    if options.outfile:
        f = codecs.open(options.outfile, 'w', 'utf-8')
    elif output_to_temp_file:
        output_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        f = codecs.getwriter('utf-8')(output_file)
        output_filename = output_file.name
    else:
        f = sys.stdout

    renderer_kwargs = {}

    if options.renderer == 'text':
        unicode_override = options.unicode != None
        color_override = options.color != None
        unicode = options.unicode if unicode_override else file_supports_unicode(f)
        color = options.color if color_override else file_supports_color(f)
        
        renderer_kwargs = {'unicode': unicode, 'color': color}

    f.write(profiler.output(renderer=options.renderer, **renderer_kwargs))
    f.close()

    if output_to_temp_file:
        print('stdout is a terminal, so saved profile output to %s' % output_filename)
        import webbrowser, urllib.parse
        url = urllib.parse.urlunparse(('file', '', output_filename, '', '', ''))
        webbrowser.open(url)



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


if __name__ == '__main__':
    main()
