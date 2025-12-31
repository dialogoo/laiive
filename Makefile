include .env
export

# -----------------BUILD DOCKER COMPOSE FOR DEV AND PROD----------------------------------------------------------------------
build:
	docker-compose build

up-dev:
	docker-compose up --build

up-prod:
	docker-compose -f docker-compose.yml up --build

down:
	docker-compose down

logs:
	docker-compose logs -f


# ---------------SHELL FOR DEV INSIDE EACH SERVICE CONTAINER ------------------------------------------------------------------

# Update shell commands:
shell-pusher:
	docker exec -it laiive-pusher sh

shell-retriever:
	docker exec -it laiive-retriever sh

# Update service starters:
start-retriever:
	cd services/retriever && uv sync && uv run uvicorn agent.api:app --host 0.0.0.0 --port 8000 --reload

start-pusher:
	cd services/pusher && uv sync && uv run uvicorn agent.api:app --host 0.0.0.0 --port 8001 --reload
