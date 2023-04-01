.PHONY: tests

run-bot:
	python -m manga_notify bot

run-jobs:
	python -m manga_notify jobs

run-docker:
	docker-compose up -d --build

start-dev-env:
	docker-compose up -d postgres redis

down-dev-env:
	docker-compose down

mypy-check:
	python -m mypy manga_notify tests

flake8-check:
	python -m flake8 manga_notify	tests

tests:
	. ./tests/init_env.sh && python -m pytest tests
