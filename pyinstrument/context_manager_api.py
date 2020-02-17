from pyinstrument.util import file_supports_color, file_supports_unicode
import sys
from .profiler import Profiler


class ProfileContext:
    def __init__(self, *, color=None, unicode=None):
        self.profiler = Profiler()
        self.color_override = color
        self.unicode_override = unicode
    
    def __call__(self, **kwargs):
        return ProfileContext(**kwargs)
    
    def __enter__(self):
        self.profiler.start()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.profiler.stop()

        if is_notebook():
            
            from IPython.core.display import display, HTML
            display(HTML(self.profiler.output_html()))
        else:
            f = sys.stdout
            c = self.color_override
            u = self.unicode_override
            f.write(
                self.profiler.output_text(
                    color=c if c is not None else file_supports_color(f),
                    unicode=u if u is not None else file_supports_unicode(f),
                )
            )

def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

profile = ProfileContext()
