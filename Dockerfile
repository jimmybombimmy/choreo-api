# ==========================================
# STAGE 1: Builder
# ==========================================
FROM ubuntu:24.04 AS builder-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
  apt-get install --no-install-recommends -y ca-certificates build-essential && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.11.12 /uv /uvx /bin/

# Force uv to use Python 3.13 and install it outside /root
ENV UV_PYTHON=python3.13
ENV UV_PYTHON_INSTALL_DIR=/opt/uv/python
ENV UV_COMPILE_BYTECODE=1

WORKDIR /build

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project


# ==========================================
# STAGE 2: Runner
# ==========================================
FROM ubuntu:24.04 AS runner-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
  apt-get install --no-install-recommends -y ca-certificates && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home myuser

# Copy Python runtime created by uv
COPY --from=builder-image /opt/uv/python /opt/uv/python

# Copy virtual environment
COPY --from=builder-image /build/.venv /build/.venv

# Give the user access
RUN chown -R myuser:myuser /build/.venv /opt/uv/python

USER myuser

WORKDIR /home/myuser/code

COPY --chown=myuser:myuser . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/build/.venv
ENV PATH="/build/.venv/bin:$PATH"

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

# Make some dependent logic so that you run the following if local:
# CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]

# If you weren't using kubernetes, using gunicorn would function as your runner.
# This would be way cheaper with Cloud Run vs GKE, for example.
# You would need to `uv add gunicorn` locally first if this was the approach
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]