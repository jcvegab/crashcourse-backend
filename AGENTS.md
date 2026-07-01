# AGENTS.md

## Commands

### Local development
- Install deps: `uv sync`
- Dev server: `uv run ./manage.py runserver`
- Migrations: `uv run ./manage.py makemigrations` / `uv run ./manage.py migrate`
- Seed data: `./seed.sh` (loads `category` then `course` fixtures)
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Tests: `uv run ./manage.py test`

### Docker (Production Simulation)
- Start & Build: `docker compose --env-file .env.local up --build -d`
- Note: Docker uses `gunicorn` and `RENDER=true` to simulate production. Code is copied into the image during build. Hot-reload is disabled.
- Variables are passed via `env_file: .env.local` in `docker-compose.yml`; use `--env-file .env.local` for compose-level variable interpolation (`${DB_NAME}`, etc.)
- Migrations: `docker compose exec web uv run python manage.py migrate`
- Shell: `docker compose exec web uv run python manage.py shell`
- Seed: `docker compose exec web bash seed.sh`

## Style & Tooling
- `ruff` line-length: 120, target Python: 3.13, first-party packages: `backend`, `core` (see `pyproject.toml`)
- `ruff` lint selects: `E`, `F`, `I`, `UP`, `B`, `SIM`

## Architecture
- Django 5.0 + graphene-django (GraphQL API) + Django-Ninja (REST API)
- Single app: `core` (models, schema, admin, API)
- GraphQL endpoint: `/graphql/` (GraphiQL enabled when `DEBUG=True`)
- REST API: `core/api.py` → Django-Ninja (Swagger `/docs` only when `DEBUG=True`)
- GraphQL schema: `core/schema.py` → referenced in `GRAPHENE["SCHEMA"]` setting
- REST URL namespace: `api-0.1.0` → `core/urls.py` (all endpoints at root, no prefix)
- REST routes: `/`, `/health/`, `/auth/login/`, `/auth/refresh/`
- `core/urls.py` explicitly strips Ninja docs (`/docs`, `/openapi.json`) when `DEBUG=False`.

## Environment
- Local dev requires `.env.local` with: `SECRET_KEY`, `DB_NAME`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
- `.env` is fallback if `.env.local` is missing (loaded only when not on Render)
- Production (Render) uses platform env vars; `.env` is fallback
- Also supports: `DEBUG`, `CORS_ORIGIN_MAIN`, `CORS_ORIGIN_REGEX`, `RENDER_EXTERNAL_HOSTNAME`, `SECURE_SSL_REDIRECT`
- `DEBUG` is user-controlled, editable in `.env.local` or platform env; controls Swagger docs, GraphiQL, Django error pages
- `RENDER` is platform-controlled (auto-set by Render), determines SSL mode, WhiteNoise, CORS origins
- The two flags are independent: `DEBUG=True` can coexist with `RENDER=true` (debugging on production)
- DB SSL (`sslmode: require`) is enabled when `IS_PROD=True` (derived from `RENDER=true`), not by `DEBUG`

## Models
- `Category`: self-referential `parent` FK (tree structure — categories and subcategories share one table)
- `Course.level`: integer choices (1=Introductorio, 2=Intermedio, 3=Avanzado, 4=Completo), not strings
- `Course.category` / `Course.subcategory`: both FK to `Category` with different `related_name`

## Deployment
- Render (`render.yaml`): Docker runtime using the project `Dockerfile`
- Production: `gunicorn --bind 0.0.0.0:${PORT:-8000} backend.wsgi:application` (container CMD; Render sets `PORT=10000`)
- Migrations run automatically via Render `preDeployCommand` before each deploy
- `Dockerfile` hardcodes `RENDER=true` and `SECRET_KEY` during `collectstatic` to simulate production locally;
