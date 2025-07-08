from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from mcp_oauth import IntrospectionTokenVerifier
from .oauth_server import OAUTH_HOST, OAUTH_SERVER_URL, OAUTH_PORT


class ServerSettings(BaseSettings):
    """Settings for the MCP Server."""

    model_config = SettingsConfigDict(env_prefix="MCP_RESOURCE_")

    # Server settings
    host: str = "localhost"
    port: int = 8000
    server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")

    # Authorization Server settings
    auth_server_url: AnyHttpUrl = AnyHttpUrl(f"{OAUTH_SERVER_URL}")
    auth_server_introspection_endpoint: str = f"{OAUTH_SERVER_URL}/introspect"

    # MCP settings
    mcp_scope: str = "user"

    # RFC 8707 resource validation
    oauth_strict: bool = False


def create_private_server(settings: ServerSettings = ServerSettings()) -> FastMCP:

    token_verifier = IntrospectionTokenVerifier(
        introspection_endpoint=settings.auth_server_introspection_endpoint,
        server_url=str(settings.server_url),
        validate_resource=settings.oauth_strict,  # Only validate when --oauth-strict is set
    )

    mcp: FastMCP = FastMCP(
        name="private-example-server",
        instructions="This server specializes in private operations of user profiles data",
        debug=True,
        # Auth configuration for RS mode
        token_verifier=token_verifier,
        auth=AuthSettings(
            issuer_url=settings.auth_server_url,
            required_scopes=[settings.mcp_scope],
            resource_server_url=settings.server_url,
        ),
    )

    @mcp.tool(
        name="set_user_profile",
        description="Set the user profile information in database from user data",
    )
    async def set_user_profile(data: dict) -> dict:
        """Set the user profile information in database for user_id"""

        # TODO: Implement any logic here. Eg. database call or request profile
        # information from your user auth system.

        return {
            "status": "success",
            "message": "User added to dataset successfully",
            "data": data,
        }

    return mcp


mcp: FastMCP = create_private_server()
