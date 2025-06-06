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


# Add `get sample data`. Extrapolate to database, for example
@mcp.resource("resource://number/text/{number}")
async def get_text_from_number(number: int) -> str:
    """Return text number from an integer number"""
    my_numbers: dict[int, str] = {0: "zero", 1: "one", 2: "tow"}
    return (
        my_numbers[number]
        if my_numbers.keys().__contains__(number)
        else "Many large input"
    )
