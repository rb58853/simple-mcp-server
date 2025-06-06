from mcp.server.fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP(
    name="Server",
    instructions="This server specializes in operations with numbers, such as addition and text conversion.",
    stateless_http=True,
)


# Add an addition tool
@mcp.tool(description="Add two integer numbers")
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.resource(
    uri="data://user-profile/{user_id}",
    name="UserProfile",
    description="Gets the user profile information for user_id",
    mime_type="application/json",
)
async def get_user_profile(user_id: str) -> dict:
    """Gets the user profile information for user_id"""

    # TODO: Implement any logic here. Eg. database call or request profile
    # information from your user auth system.

    return {
        f"user_id": {user_id},
        "user_name": "Raul Beltran",
        "email": "rb58853.gmail.com",
    }
