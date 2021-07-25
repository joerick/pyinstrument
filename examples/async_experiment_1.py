import asyncio
import time

import pyinstrument


def do_nothing():
    pass


def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()


async def say(what, when, profile=False):
    if profile:
        p = pyinstrument.Profiler()
        p.start()

    busy_wait(0.1)
    sleep_start = time.time()
    await asyncio.sleep(when)
    print(f"slept for {time.time() - sleep_start:.3f} seconds")
    busy_wait(0.1)

    print(what)
    if profile:
        p.stop()
        p.print(show_all=True)


loop = asyncio.get_event_loop()

loop.create_task(say("first hello", 2, profile=True))
loop.create_task(say("second hello", 1, profile=True))
loop.create_task(say("third hello", 3, profile=True))

loop.run_forever()
loop.close()
