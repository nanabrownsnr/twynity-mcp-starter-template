import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import HelloApp from "./App.jsx";
import "./style.css";

createRoot(document.querySelector("#root")).render(
    <StrictMode>
        <HelloApp />
    </StrictMode>,
);
