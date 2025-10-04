.PHONY: dev up down logs api shell migrate seed fmt lint test

up:
	docker compose up -d --build

logs:
	docker compose logs -f --tail=200

down:
	docker compose down -v

api:
	docker compose exec api bash

worker:
	docker compose exec worker bash

web:
	docker compose exec web sh

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python -m app.scripts.seed

fmt:
	pnpm -r format || true

lint:
	pnpm -r lint || true

 test:
	docker compose exec api pytest -q
