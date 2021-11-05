import warnings

from pyinstrument.profiler import Profiler

__version__ = "4.0.4"

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")


def load_ipython_extension(ipython):
    from pyinstrument.magic import PyinstrumentMagic

    ipython.register_magics(PyinstrumentMagic)
