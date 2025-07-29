from asyncio import sleep
from typing import Awaitable, Callable

from pyinstrument import Profiler

try:
    from aiohttp import web
except ImportError:
    print("This example requires aiohttp.")
    print("Install using `pip install aiohttp`.")
    exit(1)


@web.middleware
async def profiler_middleware(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:
    with Profiler() as p:
        await handler(request)
    return web.Response(text=p.output_html(), content_type="text/html")


routes = web.RouteTableDef()


@routes.get("/")
async def get_handler(request: web.Request) -> web.Response:
    y = 1
    for x in range(1, 10000):
        y *= x
    await sleep(0.1)
    return web.Response(text="Hello, world!")


def dev_init(argv):
    """Run: python3 -m aiohttp.web -H localhost aiohttp_hello:dev_init"""
    app = web.Application(middlewares=(profiler_middleware,))
    app.add_routes(routes)
    return app
