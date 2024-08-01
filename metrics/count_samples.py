import time

import pyinstrument


def do_nothing():
    pass


def busy_wait(duration: float):
    start = time.time()
    while time.time() - start < duration:
        do_nothing()


def count_samples(duration: float, interval: float, use_timing_thread: bool):
    profiler = pyinstrument.Profiler(interval=interval, use_timing_thread=use_timing_thread)
    profiler.start()
    busy_wait(duration)
    session = profiler.stop()

    reference = duration / interval
    sample_count = len(session.frame_records)
    print(f"Interval: {interval}, use_timing_thread: {use_timing_thread}")
    print(
        f"Expected samples: {reference}, actual samples: {sample_count}, {sample_count / reference:.2f}x"
    )


count_samples(0.1, 0.001, False)
count_samples(0.1, 0.001, True)
count_samples(0.1, 0.0001, False)
count_samples(0.1, 0.0001, True)
