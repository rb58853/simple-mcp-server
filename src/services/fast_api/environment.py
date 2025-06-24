from mcp.server.fastmcp import FastMCP
from ..fast_mcp.public_server import server as public_server


class EnvAPI:
    SERVERS: list[FastMCP] = [public_server]
