include .env
export

build:
	docker-compose build

up-dev:
	docker-compose up --build

up-prod:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

db-exec:
	docker exec -it laiive-postgres-db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

db-backup:
	docker exec laiive-postgres-db pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} > data/backup.sql

db-import:
	docker exec -i laiive-postgres-db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < data/backup.sql

shell-backend:
	docker exec -it laiive-rag-chat-backend sh

shell-frontend:
	docker exec -it laiive-frontend sh

shell-db:
	docker exec -it laiive-postgres-db sh

shell-pusher:
	docker exec -it laiive-pusher sh

shell-workspace:
	docker exec -it global-workspace sh
