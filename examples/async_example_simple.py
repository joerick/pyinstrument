import asyncio

from pyinstrument import Profiler


async def main():
    p = Profiler()
    with p:
        print("Hello ...")
        await asyncio.sleep(1)
        print("... World!")
    p.print()


asyncio.run(main())
