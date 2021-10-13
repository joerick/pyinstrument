from .magic import PyinstrumentMagic


def load_ipython_extension(ipython):
    ipython.register_magics(PyinstrumentMagic)
