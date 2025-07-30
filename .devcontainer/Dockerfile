FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install git and other dev tools
RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pre-commit
RUN pip install pre-commit

# Set working directory
WORKDIR /workspace

# Keep container running
CMD ["sleep", "infinity"]
