# --- Python Base ---
FROM python:3.13-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV PATH="/app/.venv/bin:$PATH"


# --- Builder Stage: Install dependencies ---
FROM python-base as builder

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

WORKDIR /app
COPY . .

# Install dependancies without dev packages
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev


# --- Development Stage: Install dev dependencies & run server ---
FROM builder as development
ENV ENV=test

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked

EXPOSE 8000
ENTRYPOINT ["uv", "run", "-m", "techconnect_classes_api.server"]
# ENTRYPOINT ["ls", "-la"]


# --- Production Stage ---
FROM python-base as production
ENV ENV=dev

COPY --from=builder /app /app

WORKDIR /app

ENTRYPOINT ["uv", "run", "-m", "techconnect_classes_api.server"]
