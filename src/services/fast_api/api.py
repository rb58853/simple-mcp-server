import contextlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from .environment import EnvAPI
from ...config.logger import logger
from ._doc.html import base, end, server_info


def create_app():
    # Create a combined lifespan to manage both session managers
    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        async with contextlib.AsyncExitStack() as stack:
            for server in EnvAPI.SERVERS:
                await stack.enter_async_context(server.mcp.session_manager.run())
            yield

    app = FastAPI(lifespan=lifespan)
    for server in EnvAPI.SERVERS:
        app.mount(f"/{server.name}", server.mcp.streamable_http_app())

    @app.get("/", include_in_schema=False)
    async def redirect_to_help():
        return RedirectResponse(url="/help")

    @app.get("/help", include_in_schema=False)
    async def help():
        try:
            help_text: str = base + "\n<h1> Aviable Servers</h1>\n"
            for server in EnvAPI.SERVERS:
                help_text += (
                    server_info(
                        name=server.name,
                        description=server.instructions,
                        tools=server._tool_manager.list_tools(),
                    )
                    + "\n"
                )

            return HTMLResponse(content=help_text + end, status_code=200)

        except Exception as e:
            logger.error(f"Error al generar docs: {str(e)}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    return app


create_app()
