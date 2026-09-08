"""Register Twynity's well-known manifest and health HTTP routes.

FastMCP's JWT verifier protects its MCP transport, not custom routes by
default. These two routes are intentionally public; add explicit authorization
inside any new custom route that should be protected.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import settings


def register_routes(mcp):
    @mcp.custom_route("/api/v1/.well-known/mcp.json", methods=["GET"])
    async def manifest(request: Request) -> JSONResponse:
        return JSONResponse({
            "name": settings.APP_TITLE,
            "version": settings.APP_VERSION
        }, status_code=200) 

    @mcp.custom_route("/api/v1/health", methods=["GET"])
    async def health_status(request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"}, status_code=200)
