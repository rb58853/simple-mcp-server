from mcp.server.fastmcp import FastMCP
from ..fast_mcp.public_server.server import mcp as public_server
from ..fast_mcp.auth_server.server import mcp as private_server


class EnvAPI:
    SERVERS: list[FastMCP] = [public_server, private_server]
    """List of MCP servers to use"""

    BASE_IP: str = "http://0.0.0.0:8000"
    """Public Expose IP"""

    DNS: str | None = None
    """Public Expose DNS"""
