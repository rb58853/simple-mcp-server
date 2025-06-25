from mcp.server.fastmcp import FastMCP


def auth_server() -> FastMCP:
    # Create an MCP server
    mcp = FastMCP(
        name="private-example-server",
        instructions="This server specializes in private operations of user profiles data",
        stateless_http=True,
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
