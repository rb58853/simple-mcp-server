from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


async def main():
    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://0.0.0.0:8000/server/mcp") as (
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

            # Call a tool
            tool_result = await session.call_tool("add", {"a": 12, "b": 21})
            print(tool_result)
            
            resource_result = await session.read_resource("resource://number/text/1")
            print(resource_result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
