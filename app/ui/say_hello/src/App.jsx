import { useCallback, useState } from "react";
import {
    useApp,
    useDocumentTheme,
    useHostFonts,
    useHostStyleVariables,
} from "@modelcontextprotocol/ext-apps/react";

export default function HelloApp() {
    const [name, setName] = useState("");
    const [message, setMessage] = useState("Your UI goes here");
    const [hasResult, setHasResult] = useState(false);
    const [isUpdating, setIsUpdating] = useState(false);
    const [actionError, setActionError] = useState(null);

    const onAppCreated = useCallback((createdApp) => {
        // MCP clients deliver the linked tool result to this handler. The
        // `message` field comes from say_hello's structured_content dictionary.
        createdApp.ontoolresult = (result) => {
            const nextMessage = result.structuredContent?.message;
            setMessage(
                typeof nextMessage === "string"
                    ? nextMessage
                    : "The tool returned no greeting.",
            );
            setHasResult(true);
        };
    }, []);

    const { app, isConnected, error } = useApp({
        appInfo: { name: "starter-mcp-ui", version: "1.0.0" },
        capabilities: {},
        onAppCreated,
    });

    // These hooks keep the app in sync with the MCP client's theme, CSS
    // variables, and font definitions. Always keep CSS fallbacks as well.
    useHostStyleVariables(app, app?.getHostContext());
    useHostFonts(app, app?.getHostContext());
    const theme = useDocumentTheme();

    async function updateGreeting(event) {
        event.preventDefault();
        if (!app || isUpdating) return;

        setIsUpdating(true);
        setActionError(null);

        try {
            // Calling the server from the UI uses the same tool contract as a
            // model-initiated call. The tool is visible to both model and app.
            const result = await app.callServerTool({
                name: "say_hello",
                arguments: { name },
            });
            const nextMessage = result.structuredContent?.message;
            setMessage(
                typeof nextMessage === "string"
                    ? nextMessage
                    : "The tool returned no greeting.",
            );
            setHasResult(true);
        } catch (nextError) {
            setActionError(
                nextError instanceof Error ? nextError.message : "Unable to update the greeting.",
            );
        } finally {
            setIsUpdating(false);
        }
    }

    return (
        <main className="card" aria-live="polite" data-host-theme={theme}>
            <p className="eyebrow">MCP App starter</p>
            <h1>{message}</h1>
            <form className="greeting-form" onSubmit={updateGreeting}>
                <label htmlFor="name">Name</label>
                <div className="form-row">
                    <input
                        id="name"
                        name="name"
                        type="text"
                        value={name}
                        placeholder="Ada"
                        autoComplete="name"
                        onChange={(event) => setName(event.target.value)}
                    />
                    <button type="submit" disabled={!isConnected || isUpdating}>
                        {isUpdating ? "Updating…" : "Update"}
                    </button>
                </div>
            </form>
            <p className="hint">
                {error || actionError
                    ? error
                        ? `Unable to connect to the MCP client: ${error.message}`
                        : actionError
                    : hasResult
                      ? "This content came from the say_hello tool."
                      : isConnected
                        ? "Call the say_hello tool to render its result."
                        : "Connecting to the MCP client…"}
            </p>
        </main>
    );
}
