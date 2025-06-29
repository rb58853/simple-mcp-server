"""
Authorization Server for MCP Split Demo.

This server handles OAuth flows, client registration, and token issuance.
Can be replaced with enterprise authorization servers like Auth0, Entra ID, etc.

NOTE: this is a simplified example for demonstration purposes.
This is not a production-ready implementation.

"""

import asyncio
import logging

from fastapi import FastAPI
from pydantic import AnyHttpUrl, BaseModel
from starlette.applications import Starlette
from starlette.routing import Route
from uvicorn import Config, Server

from mcp.server.auth.routes import create_auth_routes
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions
from mcp.server.auth.provider import OAuthAuthorizationServerProvider

from .auth_provider.simple_auth_provider import SimpleAuthSettings, SimpleOAuthProvider
from .features.functions import ExtraFunctions

logger = logging.getLogger(__name__)


class AuthServerSettings(BaseModel):
    """Settings for the Authorization Server."""

    # Server settings
    host: str = "localhost"
    port: int = 9000
    server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:9000")
    auth_callback_path: str = "http://localhost:9000/login/callback"


class SimpleAuthProvider(SimpleOAuthProvider):
    """
    Authorization Server provider with simple demo authentication.

    This provider:
    1. Issues MCP tokens after simple credential authentication
    2. Stores token state for introspection by Resource Servers
    """

    def __init__(
        self,
        auth_settings: SimpleAuthSettings,
        auth_callback_path: str,
        server_url: str,
    ):
        super().__init__(auth_settings, auth_callback_path, server_url)


class OAuthServer:
    def __init__(
        self,
        auth_settings: SimpleAuthSettings = SimpleAuthSettings(),
        server_settings: AuthServerSettings = AuthServerSettings(),
    ):
        self.auth_settings: SimpleAuthSettings = auth_settings
        self.server_settings: AuthServerSettings = server_settings

        self.oauth_provider: OAuthAuthorizationServerProvider = SimpleAuthProvider(
            auth_settings,
            server_settings.auth_callback_path,
            str(self.server_settings.server_url),
        )
        self.__routes: list[Route] | None = None

    @property
    def routes(self) -> list[Route]:
        """Create Routes"""
        if self.__routes is None:
            # Create Settings
            mcp_auth_settings = AuthSettings(
                issuer_url=self.server_settings.server_url,
                client_registration_options=ClientRegistrationOptions(
                    enabled=True,
                    valid_scopes=[self.auth_settings.mcp_scope],
                    default_scopes=[self.auth_settings.mcp_scope],
                ),
                required_scopes=[self.auth_settings.mcp_scope],
                resource_server_url=None,
            )

            # Create OAuth routes
            routes: list[Route] = create_auth_routes(
                provider=self.oauth_provider,
                issuer_url=mcp_auth_settings.issuer_url,
                service_documentation_url=mcp_auth_settings.service_documentation_url,
                client_registration_options=mcp_auth_settings.client_registration_options,
                revocation_options=mcp_auth_settings.revocation_options,
            )

            # Append extra functions to routes
            ExtraFunctions(oauth_provider=self.oauth_provider).append_functions(
                routes=routes
            )
            self.__routes = routes

        return self.__routes

    def append_new_function(function):
        raise NotImplementedError()

    def run_starlette_server(self) -> None:
        """Run the Authorization Starlette Server."""

        async def run_server() -> None:
            starlette_server = Starlette(routes=self.routes)

            config = Config(
                starlette_server,
                host=self.server_settings.host,
                port=self.server_settings.port,
                log_level="info",
            )
            server = Server(config)

            logger.info(
                f"🚀 MCP Authorization Starlette Server running on {self.server_settings.server_url}"
            )
            await server.serve()

        asyncio.run(run_server())
