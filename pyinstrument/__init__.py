import warnings

from pyinstrument.profiler import Profiler

__version__ = "3.4.1"

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")
