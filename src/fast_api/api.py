import contextlib
from fastapi import FastAPI
from ..fast_mcp.public_server import server
from fastapi.responses import RedirectResponse


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(server.mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/server", server.mcp.streamable_http_app())


@app.get("/", include_in_schema=False)
async def redirect_to_help():
    return RedirectResponse(url="/help")


@app.get("/help", include_in_schema=False)
async def redirect_to_docs():
    help = {
        "mcp root": {
            "path": "/server/mcp",
            "description": "Example mcp server root path",
        }
    }
    return help
