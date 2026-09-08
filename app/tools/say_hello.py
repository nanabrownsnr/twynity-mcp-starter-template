from fastmcp.apps import AppConfig
from fastmcp.tools import ToolResult

from app.ui.say_hello.resource import VIEW_URI


def register_tool(mcp):
    # AppConfig links this tool to the ui:// resource registered in
    # app/ui/say_hello/resource.py. An MCP Apps-capable client reads that
    # resource and delivers this tool's result to the UI.
    @mcp.tool(
        app=AppConfig(
            resource_uri=VIEW_URI,
            visibility=["model", "app"],
        )
    )
    def say_hello(name: str = "World") -> ToolResult:
        """Create a personalised greeting and display it in the example UI.

        Use this tool when the user asks to be greeted, says hello, or wants to
        verify that the starter MCP server and its MCP App UI are connected.

        Args:
            name: The person or audience to greet. Use "World" when the user
                does not provide a name.

        Returns:
            A ToolResult containing a short text response for the model and a
            ``message`` field in structured content for the MCP App UI.

        Examples:
            ``say_hello(name="Ada")`` returns the message ``Hello, Ada!``.
        """
        clean_name = name.strip() or "World"
        message = f"Hello, {clean_name}!"

        # `content` gives the model and non-App clients a useful response.
        # `structured_content` is the stable JSON contract consumed by the UI.
        return ToolResult(
            content=message,
            structured_content={"message": message},
            meta={"ui": {"resourceUri": VIEW_URI}, "ui/resourceUri": VIEW_URI},
        )
