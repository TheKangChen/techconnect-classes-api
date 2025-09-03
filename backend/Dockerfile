FROM python:3.13-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \


FROM python-base as builder
COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependancies without dev packages
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev


FROM builder as development
ENV ENV=test

WORKDIR /app
COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked

WORKDIR /app

EXPOSE 8000
ENTRYPOINT ["uvicorn", "techconnect_classes_api.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python-base as production
ENV ENV=dev

COPY --from=builder /app /app
COPY . /app
WORKDIR /app

ENTRYPOINT ["uvicorn", "techconnect_classes_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
