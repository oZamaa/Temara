# syntax=docker/dockerfile:1

# Images de base épinglées par digest (mises à jour par Renovate à l'étape 3).
ARG NODE_IMAGE=node:22-slim@sha256:e9f565d32859f0cbfb52125eafe8be39390f24dac302dc3cdf566e8ba3ab21ee
ARG PYTHON_IMAGE=python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.13.9@sha256:d3b601f0c7b118bc1753febf7c41cc80981df678445e0254284eecf84db79a7d

# ---- 1. Frontend : build statique ------------------------------------------
FROM ${NODE_IMAGE} AS frontend
RUN npm install --global pnpm@12.21.0
WORKDIR /build
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend/ ./
RUN pnpm build

# ---- 2. Backend : environnement virtuel uv ---------------------------------
FROM ${UV_IMAGE} AS uv

FROM ${PYTHON_IMAGE} AS backend
COPY --from=uv /uv /usr/local/bin/uv
ENV UV_PYTHON_DOWNLOADS=never UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ---- 3. Image finale -------------------------------------------------------
FROM ${PYTHON_IMAGE} AS final
RUN groupadd --gid 10001 jobtrack \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin jobtrack \
    && mkdir /data \
    && chown 10001:10001 /data

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    JOBTRACK_DATA_DIR=/data \
    JOBTRACK_STATIC_DIR=/app/static

WORKDIR /app
COPY --from=backend /app/.venv /app/.venv
COPY backend/app /app/app
COPY --from=frontend /build/dist /app/static

USER 10001:10001
VOLUME ["/data"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3)"]

# Un seul worker : suffisant pour quelques comptes et requis par SQLite.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
