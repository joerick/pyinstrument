from pyinstrument import Profiler

p = Profiler(use_signal=False)

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

with open("overflow_out.html", "w") as f:
    f.write(p.output_html())
