from pathlib import Path

from fastmcp.apps import AppConfig

VIEW_URI = "ui://starter/hello.html"
VIEW_PATH = Path(__file__).parent / "dist" / "index.html"


def load_view_html() -> str:
    """Load the compiled UI and explain how to create it when it is missing."""
    if not VIEW_PATH.is_file():
        raise RuntimeError(
            "The MCP App UI has not been built. Run `npm ci` and `npm run build` "
            "inside app/ui/say_hello before starting the server."
        )
    return VIEW_PATH.read_text(encoding="utf-8")


def register_resource(mcp):
    # This ui:// resource is the HTML document an MCP Apps-capable client
    # renders when it sees the same URI in a tool's AppConfig.
    @mcp.resource(VIEW_URI, app=AppConfig())
    def hello_view():
        """Return the bundled MCP App UI for the hello example."""
        return load_view_html()
