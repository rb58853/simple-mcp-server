from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio


async def open_session():
    # Connect to a streamable HTTP server
    async with streamablehttp_client(
        "http://0.0.0.0:8000/public-example-server/mcp"
    ) as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
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

            # # Get prompt
            # prompt = await session.get_prompt(
            #     "summarize_user_profile",
            #     {"user_name": "Raul Beltran", "email": "rb58853@gmail.com"},
            # )


def run():
    print("Testing simple client server")
    asyncio.run(open_session())
