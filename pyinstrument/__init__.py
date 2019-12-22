from pyinstrument.profiler import Profiler
import warnings

__version__ = '3.1.1'

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")
