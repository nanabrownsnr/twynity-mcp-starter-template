"""Configure JWT verification for MCP requests.

Change the account-service/JWKS settings in ``config.py``; custom HTTP routes
registered in ``twynity.py`` are not automatically protected by this verifier.
"""

from fastmcp.server.auth.providers.jwt import JWTVerifier

from app.config import settings


def get_auth_provider() -> JWTVerifier:
    """Builds the auth checker FastMCP will run on every incoming request."""
    jwks_url = (
        f"{settings.ACCOUNT_SERVICE_URL.rstrip('/')}"
        f"/{settings.ACCOUNT_SERVICE_JWKS_ENDPOINT.lstrip('/')}"
    )
    return JWTVerifier(
        jwks_uri=jwks_url
    )
