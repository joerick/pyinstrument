from __future__ import annotations

from asyncio import sleep

from litestar import Litestar, get
from litestar.middleware import MiddlewareProtocol
from litestar.types import ASGIApp, Message, Receive, Scope, Send

from pyinstrument import Profiler


class ProfilingMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)  # type: ignore
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        profiler = Profiler(interval=0.001, async_mode="enabled")
        profiler.start()
        profile_html: str | None = None

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                profiler.stop()
                nonlocal profile_html
                profile_html = profiler.output_html()
                message["headers"] = [
                    (b"content-type", b"text/html; charset=utf-8"),
                    (b"content-length", str(len(profile_html)).encode()),
                ]
            elif message["type"] == "http.response.body":
                assert profile_html is not None
                message["body"] = profile_html.encode()
            await send(message)

        await self.app(scope, receive, send_wrapper)


@get("/")
async def index() -> str:
    await sleep(1)
    return "Hello, world!"


app = Litestar(
    route_handlers=[index],
    middleware=[ProfilingMiddleware],
)
