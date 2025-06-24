from mcp.server.fastmcp import FastMCP
import httpx


def public_server() -> FastMCP:
    # Create an MCP server
    mcp = FastMCP(
        name="public-example-server",
        instructions="This server specializes in operations with numbers, such as addition and text conversion.",
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

    @mcp.resource(
        uri="data://user-profile/{user_id}",
        name="user_profile",
        description="Gets the user profile information for user_id",
        mime_type="application/json",
    )
    async def get_user_profile(user_id: str) -> dict[str, any]:
        """Gets the user profile information for user_id"""

        # TODO: Implement any logic here. Eg. database call or request profile
        # information from your user auth system.

        return {
            "user_id": str(user_id),
            "user_name": "Raul Beltran",
            "email": "rb58853.gmail.com",
        }

    @mcp.prompt(
        name="points_data_analyze",
        description="Creates a prompt asking for analysis of numerical data",
    )
    def analyze_data(data_points: str) -> str:
        """creates a prompt asking for analysis of numerical data"""
        return f"analyze these data points: {data_points[1:-1]}"

    return mcp


mcp = public_server()
