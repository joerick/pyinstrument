import warnings

from pyinstrument.context_manager import profile
from pyinstrument.profiler import Profiler

__all__ = ["__version__", "Profiler", "load_ipython_extension", "profile"]
__version__ = "5.0.3"

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")


def load_ipython_extension(ipython):
    """
    This function is called by IPython to load the pyinstrument IPython
    extension, which is done with the magic command `%load_ext pyinstrument`.
    """

    from pyinstrument.magic import PyinstrumentMagic

    ipython.register_magics(PyinstrumentMagic)
