FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8001
CMD ["python", "-c", "import sys; sys.path.insert(0, '/app'); from app.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"]