from pyinstrument.profiler import Profiler
import warnings

__version__ = '2.3.0'

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")
