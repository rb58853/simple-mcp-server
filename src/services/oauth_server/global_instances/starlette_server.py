from ..oauth_server import (
    OAuthServer,
    AuthServerSettings,
    SimpleAuthSettings,
)

# Create OAuthServer Global Instance
OAUTH_SERVER: OAuthServer | None = None


def run_starlette_global_instance(
    server_settings: AuthServerSettings = AuthServerSettings(),
    auth_settings: SimpleAuthSettings = SimpleAuthSettings(),
) -> OAuthServer:
    global OAUTH_SERVER
    if OAUTH_SERVER is None:
        OAUTH_SERVER = OAuthServer(
            server_settings=server_settings, auth_settings=auth_settings
        )
        OAUTH_SERVER.run()
    return OAUTH_SERVER
