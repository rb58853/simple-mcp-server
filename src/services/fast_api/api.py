import contextlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from ...config.logger import logger
from ._doc.html import base, end, server_info
from ..fast_mcp.public_server.server import mcp as public_server
from ..fast_mcp.auth_server.server import mcp as auth_server
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP


class FastAppSettings(BaseModel):
    expose_url: str = "http://0.0.0.0:8000"
    """Public Expose IP"""
    dns: str | None = None
    """Public Expose DNS"""
    servers: list[FastMCP] = [public_server]
    """MCP server that will be add to app"""


class FastAPP:
    def __init__(
        self,
        fast_app_settings: FastAppSettings = FastAppSettings(),
    ):
        self.app_settings: FastAppSettings = fast_app_settings

    def create_app(self) -> FastAPI:
        servers: list[FastMCP] = self.app_settings.servers

        # Create a combined lifespan to manage both session managers
        @contextlib.asynccontextmanager
        async def lifespan(app: FastAPI):
            async with contextlib.AsyncExitStack() as stack:
                for server in servers:
                    await stack.enter_async_context(server.session_manager.run())
                yield

        app = FastAPI(lifespan=lifespan)
        for server in servers:
            app.mount(f"/{server.name}", server.streamable_http_app())

        @app.get("/", include_in_schema=False)
        async def redirect_to_help():
            return RedirectResponse(url="/help")

        @app.get("/help", include_in_schema=False)
        async def help():
            try:
                help_text: str = base + "\n<h1> Aviable Servers</h1>\n"
                for server in servers:
                    help_text += (
                        server_info(
                            name=server.name,
                            description=server.instructions,
                            tools=[
                                tool.name for tool in server._tool_manager.list_tools()
                            ],
                            expose_url=self.app_settings.expose_url,
                        )
                        + "\n"
                    )

                return HTMLResponse(content=help_text + end, status_code=200)

            except Exception as e:
                logger.error(f"Error al generar docs: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error interno del servidor"
                )

        return app
