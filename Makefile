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

# -----------------POSTGRES----------------------------------------------------------------------------------------------------
# note: to use docker exec to acces the db first exit the devcontainer in the shell.
db-exec:
	docker exec -it laiive-postgres-db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Backup the entire laiive database (schema + data)
# Backup the entire laiive database (schema + data)
db-backup:
	docker exec laiive-postgres-db pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} > data/laiive_backup_$(shell date +%Y%m%d_%H%M%S).sql
# Backup only the schema (no data)
db-backup-schema:
	docker exec laiive-postgres-db pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} --schema-only > data/laiive_schema_backup.sql

# Backup only the data (no schema)
db-backup-data:
	docker exec laiive-postgres-db pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} --data-only > data/laiive_data_backup.sql

# Restore the laiive database from backup
db-restore:
	docker exec -i laiive-postgres-db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < data/laiive_backup.sql

# ---------------SHELL FOR DEV INSIDE EACH SERVICE CONTAINER ------------------------------------------------------------------
shell-backend:
	docker exec -it laiive-retriever-backend sh

shell-frontend:
	docker exec -it laiive-frontend sh

shell-db:
	docker exec -it laiive-postgres-db sh

shell-pusher:
	docker exec -it laiive-pusher sh

shell-workspace:
	docker exec -it global-workspace sh

all-services-up:
	cd services/frontend && uv run streamlit run main.py --server.address 0.0.0.0 --server.port 3000 & \
	cd services/retriever && uv run uvicorn retriever.api:app --host 0.0.0.0 --port 8000 --reload

# --------------------SERVICE STARTERS --------------------------------------------------------------------------------------------------
start-frontend:
	cd services/frontend && uv sync && uv run streamlit run main.py --server.address 0.0.0.0 --server.port 3000

start-retriever:
	cd services/retriever && uv sync && uv run uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload

start-pusher:
	cd services/pusher && uv sync && uv run python main.py

start-scraper:
	cd services/scraper && uv sync && cd event_scraper && uv run python main.py

start-parser:
	cd services/parser && uv sync && uv run python parser.py

# --------------------TESTS --------------------------------------------------------------------------------------------------
test-parser:
	pytest tests/test_parser.py -v -s --log-cli-level=INFO --capture=no --tb=short
