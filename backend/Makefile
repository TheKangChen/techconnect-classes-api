.PHONY: up down initdb dev test local-run local-initdb

up:
	docker compose up --build -d

down:
	docker compose down

initdb:
	docker exec -it app uv run ./scripts/initdb.py --env=dev --drop-all

dev:
	docker compose up --build -d
	docker exec -it app uv run ./scripts/initdb.py --env=dev --drop-all

test:
	docker compose up --build -d app test-db
	docker exec -it --env-file .env.test app pytest tests/
	docker compose down app test-db

local-run:
	ENV=local uv run -m techconnect_classes_api.server

local-initdb: local-createdb
	ENV=local uv run -m scripts.initdb --drop-all

local-createdb:
	ENV=local uv run -m scripts.createdb --exist
