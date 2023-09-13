from pyinstrument import Profiler

p = Profiler()

p.start()


def func(num):
    if num == 0:
        return
    b = 0
    for x in range(1, 100000):
        b += x

    return func(num - 1)


func(900)

p.stop()

print(p.output_text())

p.write_html("overflow_out.html")
