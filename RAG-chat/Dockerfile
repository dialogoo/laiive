FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv/installer:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app

COPY pyproject.toml .

RUN uv sync --locked

COPY . .

CMD ["uv", "run", "main.py"]
