import {
    App,
    applyDocumentTheme,
    applyHostStyleVariables,
} from "@modelcontextprotocol/ext-apps";
import "./style.css";

const app = new App({ name: "starter-mcp-ui", version: "1.0.0" });
const messageElement = document.querySelector("#message");
const hintElement = document.querySelector("#hint");

function applyHostStyles(context) {
    if (context?.theme) {
        applyDocumentTheme(context.theme);
    }
    if (context?.styles?.variables) {
        applyHostStyleVariables(context.styles.variables);
    }
}

// MCP clients send the linked tool result to this handler. The `message`
// property comes from say_hello's structured_content dictionary.
app.ontoolresult = (result) => {
    const message = result.structuredContent?.message;
    if (typeof message !== "string") {
        messageElement.textContent = "The tool returned no greeting.";
        return;
    }

    // Use textContent for values returned by tools. Do not inject untrusted
    // tool data with innerHTML.
    messageElement.textContent = message;
    hintElement.textContent = "This content came from the say_hello tool.";
};

app.onhostcontextchanged = applyHostStyles;

await app.connect();
applyHostStyles(app.getHostContext());
