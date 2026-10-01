.PHONY: install dev lint fmt test check docker up

install:  ## Установить зависимости и git-хуки
	uv sync
	uv run pre-commit install

dev:      ## Запустить API локально с автоперезагрузкой
	uv run uvicorn textkit.main:app --reload

fmt:      ## Отформатировать код
	uv run ruff format .
	uv run ruff check --fix .

lint:     ## Линтер и проверка типов
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy

test:     ## Тесты с покрытием
	uv run pytest

check: lint test  ## Всё, что проверяет CI

docker:   ## Собрать Docker-образ
	docker build -t textkit:local .

up:       ## Запустить в Docker Compose
	docker compose up --build
