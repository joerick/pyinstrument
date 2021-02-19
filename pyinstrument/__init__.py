from pyinstrument.profiler import Profiler
import warnings

__version__ = '3.4.1'

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")
