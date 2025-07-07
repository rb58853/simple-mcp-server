import os
from mcp_oauth import (
    OAuthServer,
    SimpleAuthSettings,
    AuthServerSettings,
)


OAUTH_HOST = "127.0.0.1"
OAUTH_PORT = 9000
OAUTH_SERVER_URL = f"http://{OAUTH_HOST}:{OAUTH_PORT}"


def run_oauth_server():
    server_settings: AuthServerSettings = AuthServerSettings(
        host=OAUTH_HOST,
        port=OAUTH_PORT,
        server_url=f"{OAUTH_SERVER_URL}",
        auth_callback_path=f"{OAUTH_SERVER_URL}/login",
    )
    auth_settings: SimpleAuthSettings = SimpleAuthSettings(
        superusername=os.getenv("SUPERUSERNAME"),
        superuserpassword=os.getenv("SUPERUSERPASSWORD"),
        mcp_scope="user",
    )
    oauth_server: OAuthServer = OAuthServer(
        server_settings=server_settings, auth_settings=auth_settings
    )
    oauth_server.run_starlette_server()


if __name__ == "__main__":
    run_oauth_server()
