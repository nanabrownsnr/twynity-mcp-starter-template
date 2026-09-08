# Builds the MCP App and production Python runtime. Update the UI COPY paths
# when renaming the example; generated dist/ files stay out of source control.
FROM node:22-alpine AS ui-builder

WORKDIR /ui

COPY app/ui/say_hello/package.json app/ui/say_hello/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY app/ui/say_hello/index.html app/ui/say_hello/vite.config.js ./
COPY app/ui/say_hello/src/ ./src/
RUN npm run build


FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY app/ ./app/
COPY --from=ui-builder /ui/dist/ ./app/ui/say_hello/dist/

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
