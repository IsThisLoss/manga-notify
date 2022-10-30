.PHONY: all

run-bot:
	python -m manga_notify bot

run-jobs:
	python -m manga_notify bot

run-docker:
	docker-compose up -d --build

start-dev-env:
	docker-compose up -d postgres redis

down-dev-env:
	docker-compose down

mypy-check:
	python -m mypy --ignore-missing-imports manga_notify	

flake8-check:
	python -m flake8 manga_notify	

tests:
	. ./tests/init_env.sh && python -m pytest tests
