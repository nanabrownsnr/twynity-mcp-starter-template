"""Protect the JWT verifier contract and custom-route auth expectations.

Extend these tests when changing account-service authentication or route policy.
"""

import pytest
from fastmcp import FastMCP

from app.auth import get_auth_provider
from app.twynity import register_routes


@pytest.fixture
def authenticated_app():
    mcp = FastMCP("test_server", auth=get_auth_provider())
    register_routes(mcp)
    return mcp.http_app()


def test_auth_provider_uses_the_configured_jwks_endpoint():
    provider = get_auth_provider()

    assert provider.jwks_uri == "http://account.invalid/.well-known/jwks.json"
    assert provider.algorithm == "RS256"


def test_custom_health_route_is_not_implicitly_jwt_protected(authenticated_app):
    """Custom routes need explicit auth even when FastMCP has a JWT verifier."""
    from starlette.testclient import TestClient

    response = TestClient(authenticated_app).get("/api/v1/health")

    assert response.status_code == 200
