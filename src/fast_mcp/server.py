from mcp.server.fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP(
    name="Server",
    instructions="This server specializes in operations with numbers, such as addition and text conversion.",
    stateless_http=True,
)


# Add an addition tool
@mcp.tool(
    name="add",
    description="Add two integer numbers",
)
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.resource(
    uri="data://user-profile/{user_id}",
    name="user_profile",
    description="Gets the user profile information for user_id",
    mime_type="application/json",
)
async def get_user_profile(user_id: str):  # -> dict:
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
