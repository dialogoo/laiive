
build:
	docker-compose build

run:
	docker-compose up --build

stop:
	docker-compose down

logs:
	docker-compose logs -f
