from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP(
    name="example mcp server",
    # settings={"host": "127.0.0.1", "port": 8000, "path": "/mcp/example"},
)


@mcp.tool(description="Calcula el BMI dado un peso y una altura")
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(latitude: float, longitude: float) -> str:
    """Fetch current weather for a location using latitude and longitude"""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current_weather=true&"
        f"hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
