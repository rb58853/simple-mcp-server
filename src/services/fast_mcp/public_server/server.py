from mcp.server.fastmcp import FastMCP


def public_server() -> FastMCP:
    # Create an MCP server
    mcp = FastMCP(
        name="public-example-server",
        instructions="This server specializes in public operations of user profiles data",
        stateless_http=True,
    )

    @mcp.tool(
        name="set_user_profile",
        description="Set the user profile information in database from user data",
    )
    async def set_user_profile(data: dict) -> dict:
        """Set the user profile information in database for user_id"""

        # TODO: Implement any logic here. Eg. database call or request profile
        # information from your user auth system.

        return {
            "status": "success",
            "message": "User added to dataset successfully",
            "data": data,
        }

    @mcp.resource(
        uri="data://user-profile/{user_id}",
        name="user_profile",
        description="Gets the user profile information for user_id",
        mime_type="application/json",
    )
    async def get_user_profile(user_id: str) -> dict:
        """Gets the user profile information for user_id"""

        # TODO: Implement any logic here. Eg. database call or request profile
        # information from your user auth system.

        return {
            "user_id": str(user_id),
            "user_name": "Raul Beltran",
            "email": "rb58853@gmail.com",
        }

    @mcp.prompt(
        name="summarize_user_profile",
        description="Summarizes the user profile based on the provided data.",
    )
    async def summarize_user_profile(user_name: str, email: str):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Summarize the following user profile:\nName: {user_name}\nEmail: {email}",
                    },
                }
            ]
        }

    return mcp


mcp: FastMCP = public_server()
