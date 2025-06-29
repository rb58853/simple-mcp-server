from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from ...oauth_server.oauth_server import OAuthServer


def auth_server(oauth_server: OAuthServer | None = None) -> FastMCP:
    # Create an MCP server
    mcp = FastMCP(
        name="private-example-server",
        instructions="This server specializes in private operations of user profiles data",
        stateless_http=True,
        auth_server_provider=oauth_server.oauth_provider,
        auth=AuthSettings(
            issuer_url=oauth_server.server_settings.server_url,
            required_scopes=[oauth_server.auth_settings.mcp_scope],
            # resource_server_url=settings.server_url,
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