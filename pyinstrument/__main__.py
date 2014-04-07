from optparse import OptionParser
import sys
import os
import codecs
from pyinstrument import Profiler

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
            exec code in globs, None
        except SystemExit, KeyboardInterrupt:
            pass

        profiler.stop()

        if options.outfile:
            f = codecs.open(options.outfile, 'w', 'utf-8')
            unicode = True
        else:
            f = sys.stdout
            unicode = 'utf' in os.environ.get('LC_CTYPE', '').lower()

        if options.output_html:
            f.write(profiler.output_html())
        else:
            f.write(profiler.output_text(unicode=unicode))

        f.close()
    else:
        parser.print_usage()
    return parser

if __name__ == '__main__':
    main()
