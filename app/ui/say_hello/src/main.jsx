// React browser entry point. Change the root component import when you rename
// the example UI, and keep the target ID aligned with index.html.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import HelloApp from "./App.jsx";
import "./style.css";

createRoot(document.querySelector("#root")).render(
    <StrictMode>
        <HelloApp />
    </StrictMode>,
);
