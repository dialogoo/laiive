# installs the dependencies
deps:
	rm -rf .venv || true # remove the venv if it exists
	uv sync --locked

# runs the server
run:
	uv run uvicorn rag_chat.api:app --host 0.0.0.0 --port 8000

# adds reload so that the server restarts when the code changes
run-dev:
	uv run uvicorn rag_chat.api:app --host 0.0.0.0 --port 8000 --reload

# opens a shell in the container to work from inside the container
shell:
	uv run sh
