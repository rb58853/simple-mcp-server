from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl

# from mcp.server.auth.provider import TokenVerifier, TokenInfo
from mcp.server.auth.provider import OAuthAuthorizationServerProvider
from pydantic_settings import BaseSettings


class SimpleSettings(BaseSettings):
    """Settings for the MCP Resource Server."""

    # Server settings
    server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8001")

    # Authorization Server settings
    auth_server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:9000")

    # MCP settings
    mcp_scope: str = "user"


settings = SimpleSettings()


def auth_server() -> FastMCP:
    # Create an MCP server
    mcp = FastMCP(
        name="private-example-server",
        instructions="This server specializes in private operations of user profiles data",
        stateless_http=True,
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
    async def set_user_profile(data: dict[str, any]) -> dict[str, any]:
        """Set the user profile information in database for user_id"""

        # TODO: Implement any logic here. Eg. database call or request profile
        # information from your user auth system.

        return {
            "status": "success",
            "message": "User added to dataset successfully",
            "data": data,
        }

    return mcp


mcp = auth_server()
