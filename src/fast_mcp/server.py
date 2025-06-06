from mcp.server.fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP(name="Server", stateless_http=True)


# Add an addition tool
@mcp.tool(description="Suma dos numeros, a y b, pasados por parametros")
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
