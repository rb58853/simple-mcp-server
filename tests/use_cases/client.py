"""
TODO: Ingles
Cliente simple que se conecta a un MCP Server con protocolo httpstream sin usar sistema de Authorizacion
"""

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio


async def open_session():
    server_url: str = "http://127.0.0.1:8000/public-example-server/mcp"
    # Connect to a streamable HTTP server
    print("📡 Opening StreamableHTTP transport connection without auth...")
    async with streamablehttp_client(server_url) as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        print("🤝 Initializing MCP session...")
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("✨ Session initialization complete!")
            print(f"\n✅ Connected to MCP server at {server_url}")
            if get_session_id:
                session_id = get_session_id()
                if session_id:
                    print(f"Session ID: {session_id}")

            tools = await session.list_tools()
            print("\n⚙️  Aviable Tools")
            for tool in tools.tools:
                print(f"   • {tool.name}: {tool.description}")

            # List available resources
            resources = await session.list_resource_templates()
            # List available prompts
            promts = await session.list_prompts()

            # Call a tool
            tool_result = await session.call_tool(
                "set_user_profile",
                {
                    "data": {
                        "user_id": "1111",
                        "user_name": "Raul Beltran",
                        "email": "rb58853@gmail.com",
                    }
                },
            )

            # Read a resource
            resource_result = await session.read_resource("data://user-profile/14516")


def run():
    print("💻 Testing simple client server\n".upper())
    asyncio.run(open_session())
