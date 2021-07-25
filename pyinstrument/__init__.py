import warnings

from pyinstrument.profiler import Profiler

__version__ = "4.0.0"

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")
