import contextlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from ...config.logger import logger
from ._doc.html import base, end, server_info
from ..oauth_server.oauth_server import OAuthServer
from ..fast_mcp.public_server.server import public_server
from ..fast_mcp.auth_server.server import auth_server
from pydantic import BaseModel


class FastAppSettings(BaseModel):
    EXPOSE_URL: str = "http://0.0.0.0:8000"
    """Public Expose IP"""
    DNS: str | None = None
    """Public Expose DNS"""


class FastAPP:
    def __init__(
        self,
        fast_app_settings: FastAppSettings = FastAppSettings(),
        oauth_server: OAuthServer = OAuthServer(),
    ):
        self.app_settings: FastAppSettings = fast_app_settings
        self.servers = [
            public_server(),
            auth_server(oauth_server=oauth_server),
        ]

    def create_app(self) -> FastAPI:
        servers = self.servers

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
                            expose_url=self.app_settings.EXPOSE_URL,
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
