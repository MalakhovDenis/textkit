# syntax=docker/dockerfile:1

# --- сборка: ставим зависимости через uv ---
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project
COPY textkit ./textkit

# --- рантайм: только Python, venv и код, без uv и dev-зависимостей ---
FROM python:3.14-slim-bookworm
ARG APP_VERSION=dev
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 APP_VERSION=$APP_VERSION
RUN useradd --create-home --uid 1000 app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "textkit.main:app", "--host", "0.0.0.0", "--port", "8000"]
