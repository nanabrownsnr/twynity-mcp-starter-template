import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
    // Use React's automatic JSX runtime for every source module. This prevents
    // compiled JSX from depending on a global `React` variable in MCP sandboxes.
    esbuild: { jsx: "automatic" },
    plugins: [viteSingleFile()],
    build: { outDir: "dist" },
});
