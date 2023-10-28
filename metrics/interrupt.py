from platform import platform

from pyinstrument import Profiler

p = Profiler()

p.start()


def func():
    fd = open("/dev/urandom", "rb")
    _ = fd.read(1024 * 1024)


func()

# this failed on ubuntu 12.04
platform()

p.stop()

print(p.output_text())

p.write_html("ioerror_out.html")
