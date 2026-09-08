# Build the MCP App from source. The generated dist/ directory is deliberately
# not committed to the template repository.
FROM node:22-alpine AS ui-builder

WORKDIR /ui

COPY app/ui/say_hello/package.json app/ui/say_hello/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY app/ui/say_hello/index.html app/ui/say_hello/vite.config.js ./
COPY app/ui/say_hello/src/ ./src/
RUN npm run build


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY --from=ui-builder /ui/dist/ ./app/ui/say_hello/dist/

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
