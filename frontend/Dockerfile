FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/0.8.0/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

ADD . /app

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends make \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN uv sync --locked

COPY . .

CMD ["uv", "run", "main.py"]
