import pytest
from fastmcp import FastMCP

from app.tools.say_hello import register_tool
from app.ui.say_hello.resource import VIEW_URI


@pytest.fixture
def mcp_instance():
    """Create an isolated MCP server containing the example tool."""
    mcp = FastMCP("test-server")
    register_tool(mcp)
    return mcp


@pytest.mark.asyncio
async def test_say_hello_returns_text_and_ui_data(mcp_instance, greeting_name):
    tool = await mcp_instance.get_tool("say_hello")

    result = await tool.run({"name": greeting_name})

    assert tool.meta["ui"]["resourceUri"] == VIEW_URI
    assert tool.meta["ui"]["visibility"] == ["model", "app"]
    assert result.content[0].text == "Hello, Ada!"
    assert result.structured_content == {"message": "Hello, Ada!"}
    assert result.meta == {
        "ui": {"resourceUri": VIEW_URI},
        "ui/resourceUri": VIEW_URI,
    }


@pytest.mark.asyncio
async def test_say_hello_uses_world_for_blank_names(mcp_instance):
    tool = await mcp_instance.get_tool("say_hello")

    result = await tool.run({"name": "   "})

    assert result.structured_content == {"message": "Hello, World!"}

