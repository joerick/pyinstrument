from pyinstrument.util import file_supports_color, file_supports_unicode
import sys
from .profiler import Profiler
from .renderers import ShortConsoleRenderer
import inspect


class ProfileContext:
    def __init__(self, *, color=None, unicode=None):
        self.profiler = Profiler()
        self.color_override = color
        self.unicode_override = unicode
    
    def __call__(self, **kwargs):
        return ProfileContext(**kwargs)
    
    def __enter__(self):
        caller_frame = inspect.currentframe().f_back
        self.profiler.start(
            caller_frame=caller_frame, 
            target_description='Block at {}:{}'.format(caller_frame.f_code.co_filename, 
                                                       caller_frame.f_lineno)
        )
    
    def __exit__(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        if is_notebook():
            from IPython.core.display import display, HTML
            display(HTML(self.profiler.output_html()))
        else:
            f = sys.stderr
            c = self.color_override
            u = self.unicode_override
            renderer = ShortConsoleRenderer(
                color=c if c is not None else file_supports_color(f),
                unicode=u if u is not None else file_supports_unicode(f),
            )

            f.write(renderer.render(session))

def is_notebook():
    if 'get_ipython' in globals():
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    else:
        return False      # Probably standard Python interpreter

profile = ProfileContext()
