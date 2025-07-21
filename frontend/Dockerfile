FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv/installer:latest /uv /uvx /bin/

ADD . /app 

WORKDIR /app

RUN uv sync --locked

CMD ["uv", "run", "main.py"]
