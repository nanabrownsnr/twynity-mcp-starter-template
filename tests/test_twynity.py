"""Verify Twynity's public manifest and health custom routes.

Extend this module when adding or changing custom HTTP routes in twynity.py.
"""

import pytest
from fastmcp import FastMCP
from starlette.testclient import TestClient

from app.twynity import register_routes


@pytest.fixture
def unauthenticated_app():
    """No auth attached — manifest/health should work without a token."""
    mcp = FastMCP("test_server")
    register_routes(mcp)
    return mcp.http_app()


def test_manifest_returns_expected_shape(unauthenticated_app):
    client = TestClient(unauthenticated_app)
    response = client.get("/api/v1/.well-known/mcp.json")

    assert response.status_code == 200
    body = response.json()
    assert "name" in body
    assert "version" in body

def test_health_endpoint_returns_ok(unauthenticated_app):
    client = TestClient(unauthenticated_app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
