"""
TODO: Ingles
Cliente simple que se conecta a un MCP Server con protocolo httpstream usando sistema de Authorizacion
"""

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio
import os

from mcp.client.session import ClientSession
from mcp_oauth import OAuthClient
import asyncio
from datetime import timedelta
from mcp.client.streamable_http import streamablehttp_client


def sample_mcp_client():
    # Es necesario tener un servidor MCP corriendo en la direccion http://127.0.0.1:8000//example-server/mcp por httpstream
    server_url: str = "http://127.0.0.1:8000/private-example-server/mcp"

    # Es necesario tener un servidor OAuth corriendo en la direccion http://localhost:9000
    oauth_server_url: str = "http://127.0.0.1:9000"

    user: str = os.getenv("SUPERUSERNAME")
    password: str = os.getenv("SUPERUSERPASSWORD")

    # Puedes pasarle los credenciales opcionalmente para login automatico, en caso de no pasarle los credenciales, se abrira una pagina en el navegador para hacer el login manual
    oauth_client: OAuthClient = OAuthClient(
        client_name="sample_client",
        server_url=oauth_server_url,
        # authorized_username=user,
        # authorized_username_password=password,
    )

    async def open_session():
        print("📡 Opening StreamableHTTP transport connection without auth...")
        async with streamablehttp_client(
            url=server_url,
            auth=oauth_client.oauth,
            timeout=timedelta(seconds=60),
        ) as (read_stream, write_stream, get_session_id):
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

    asyncio.run(open_session())


def run():
    print("💻 Testing auth client server".upper())
    sample_mcp_client()
