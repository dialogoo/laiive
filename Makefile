include .env
export

build:
	docker-compose build

up:
	docker-compose up --build

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
