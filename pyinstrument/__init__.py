import warnings

from pyinstrument.profiler import Profiler

__version__ = "4.4.0"

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")


def load_ipython_extension(ipython):
    """
    This function is called by IPython to load the pyinstrument IPython
    extension, which is done with the magic command `%load_ext pyinstrument`.
    """

    from pyinstrument.magic import PyinstrumentMagic

    ipython.register_magics(PyinstrumentMagic)
