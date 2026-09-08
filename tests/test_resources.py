import pytest
from fastmcp import FastMCP

from app.ui.say_hello.resource import VIEW_PATH, VIEW_URI, register_resource


@pytest.mark.asyncio
async def test_hello_ui_resource_is_registered_and_bundled():
    assert VIEW_PATH.is_file(), "Build the UI before running the complete test suite"

    mcp = FastMCP("test-server")
    register_resource(mcp)

    resource = await mcp.get_resource(VIEW_URI)
    html = await resource.read()

    assert "Your UI goes here" in html
    assert "starter-mcp-ui" in html
