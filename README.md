# textkit

Учебный проект: маленький API «текстовые утилиты» со всеми современными практиками —
git, тесты, линтеры, Docker, CI/CD на GitHub Actions и serverless-деплой на Vercel.

## API

| Метод | Путь       | Что делает                                   |
|-------|------------|----------------------------------------------|
| GET   | `/health`  | Проверка работоспособности и версия          |
| POST  | `/slugify` | `{"text": "Привет, мир"}` → `{"slug": "privet-mir"}` |
| POST  | `/stats`   | Символы, слова, строки и частые слова        |
| GET   | `/docs`    | Интерактивная документация (Swagger UI)      |

## Локальная разработка

Нужны [uv](https://docs.astral.sh/uv/) и Docker.

```bash
make install   # зависимости + pre-commit хуки
make dev       # http://localhost:8000/docs
make check     # линтер, mypy, тесты — то же, что в CI
make up        # запуск в Docker
```

## Стек и практики

- **Python 3.13 + FastAPI**, зависимости и lock-файл через **uv**
- **pytest** + покрытие (порог 90%), **ruff** (линтер и форматтер), **mypy --strict**
- **pre-commit**: проверки перед каждым коммитом
- **Docker**: multi-stage сборка, non-root пользователь, healthcheck
- **GitHub Actions**: lint → tests → сборка образа в GHCR → деплой на Vercel → smoke-тест
- **Dependabot**: еженедельные обновления зависимостей, actions и базового образа

## CI/CD

```
push / PR ─┬─ Lint & types ─┐
           └─ Tests ────────┴─ Docker image ── (main) Deploy to Vercel ── smoke-тест
```

В pull request образ только собирается; при пуше в `main` он публикуется в
`ghcr.io/<owner>/<repo>`, а приложение деплоится на Vercel.

Для деплоя нужны секреты репозитория: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
