import logging
import time
from mcp.server.auth.provider import OAuthAuthorizationServerProvider
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from mcp.server.auth.routes import cors_middleware
from auth_provider.simple_auth_provider import SimpleAuthSettings, SimpleOAuthProvider

logger = logging.getLogger(__name__)


# Currently can use only one instance of this class
class ExtraFunctions:
    oauth_provider: OAuthAuthorizationServerProvider | None = None

    def __init__(self, oauth_provider: OAuthAuthorizationServerProvider):
        ExtraFunctions.oauth_provider: OAuthAuthorizationServerProvider = oauth_provider

    def append_functions(routes: list[Route]) -> None:
        routes.append(
            Route("/login", endpoint=ExtraFunctions.login_page_handler, methods=["GET"])
        )
        routes.append(
            Route(
                "/login/callback",
                endpoint=ExtraFunctions.login_callback_handler,
                methods=["POST"],
            )
        )
        routes.append(
            Route(
                "/introspect",
                endpoint=cors_middleware(
                    ExtraFunctions.introspect_handler, ["POST", "OPTIONS"]
                ),
                methods=["POST", "OPTIONS"],
            )
        )

    # Add login page route (GET)
    async def login_page_handler(request: Request) -> Response:
        """Show login form."""
        state = request.query_params.get("state")
        if not state:
            raise HTTPException(400, "Missing state parameter")
        return await ExtraFunctions.oauth_provider.get_login_page(state)

    # Add login callback route (POST)
    async def login_callback_handler(request: Request) -> Response:
        """Handle simple authentication callback."""
        return await ExtraFunctions.oauth_provider.handle_login_callback(request)

    # Add token introspection endpoint (RFC 7662) for Resource Servers
    async def introspect_handler(request: Request) -> Response:
        """
        Token introspection endpoint for Resource Servers.
        Resource Servers call this endpoint to validate tokens without
        needing direct access to token storage.
        """
        form = await request.form()
        token = form.get("token")
        if not token or not isinstance(token, str):
            return JSONResponse({"active": False}, status_code=400)
        # Look up token in provider
        access_token = await ExtraFunctions.oauth_provider.load_access_token(token)
        if not access_token:
            return JSONResponse({"active": False})
        return JSONResponse(
            {
                "active": True,
                "client_id": access_token.client_id,
                "scope": " ".join(access_token.scopes),
                "exp": access_token.expires_at,
                "iat": int(time.time()),
                "token_type": "Bearer",
                "aud": access_token.resource,  # RFC 8707 audience claim
            }
        )
