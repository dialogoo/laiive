FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    uv sync --locked

# Copy the rest of the application
COPY . .

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

CMD [ "uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]
