include .env
export

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

db-exec:
	docker exec -it laiive-postgres-db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Backup the entire laiive database (schema + data)
db-backup:
	docker exec laiive-postgres-db pg_dump -U oscar -d laiive > data/laiive_backup.sql

# Backup only the schema (no data)
db-backup-schema:
	docker exec laiive-postgres-db pg_dump -U oscar -d laiive --schema-only > data/laiive_schema_backup.sql

# Backup only the data (no schema)
db-backup-data:
	docker exec laiive-postgres-db pg_dump -U oscar -d laiive --data-only > data/laiive_data_backup.sql

# Restore the laiive database from backup
db-restore:
	docker exec -i laiive-postgres-db psql -U oscar -d laiive < data/laiive_backup.sql

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
