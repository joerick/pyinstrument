import warnings
# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")

from pyinstrument.profiler import Profiler
from pyinstrument.context_manager_api import profile

__version__ = '3.1.1'
__all__ = ['Profiler', '__version__', 'profile']
