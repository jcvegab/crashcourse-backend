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
- Start & Build: `docker compose up --build -d`
- Note: Docker uses `gunicorn` and `RENDER=true` to simulate production. Code is copied into the image during build. Hot-reload is disabled.
- Migrations: `docker compose exec web uv run python manage.py migrate`
- Shell: `docker compose exec web uv run python manage.py shell`
- Seed: `docker compose exec web bash seed.sh`

## Architecture
- Django 5.1 + graphene-django (GraphQL API, not REST)
- Single app: `core` (models, schema, admin)
- GraphQL endpoint: `/graphql/` (GraphiQL enabled)
- GraphQL schema: `core/schema.py` → referenced in `GRAPHENE["SCHEMA"]` setting
- REST URL namespace: `v1` → `core/urls.py` (health, auth endpoints)

## Environment
- Requires `.env` with: `SECRET_KEY`, `DB_NAME`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
- Also supports: `CORS_ORIGIN_MAIN`, `CORS_ORIGIN_REGEX`, `RENDER_EXTERNAL_HOSTNAME`
- DB connection requires SSL (`sslmode: require` in settings)
- `DEBUG` is `True` when `RENDER` env var is absent

## Models
- `Category`: self-referential `parent` FK (tree structure — categories and subcategories share one table)
- `Course.level`: integer choices (1=Introductorio, 2=Intermedio, 3=Avanzado, 4=Completo), not strings
- `Course.category` / `Course.subcategory`: both FK to `Category` with different `related_name`

## Deployment
- Render (`render.yaml`): `build.sh` runs `uv sync`, `collectstatic`, `migrate`
- Production: `uv run gunicorn backend.wsgi:application`
