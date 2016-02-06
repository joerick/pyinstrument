from pyinstrument.profiler import Profiler, instrument_profile, PyInstrumentMagic


# TODO: ensure this doesn't break if ipython isn't available
from IPython import get_ipython
ip = get_ipython()
ip.register_magics(PyInstrumentMagic)
