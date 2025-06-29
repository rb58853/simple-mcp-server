from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio


async def open_session():
    # Connect to a streamable HTTP server
    async with streamablehttp_client(
        url="http://0.0.0.0:8000/private-example-server/mcp",
        headers=None,
        auth=None,
    ) as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            ping = await session.send_ping()
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

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


def run():
    print("Testing auth client server")
    asyncio.run(open_session())
