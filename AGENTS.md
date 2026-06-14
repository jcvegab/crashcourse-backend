# AGENTS.md

## Commands
- Install deps: `poetry install`
- Dev server: `poetry run ./manage.py runserver`
- Migrations: `poetry run ./manage.py makemigrations` / `poetry run ./manage.py migrate`
- Seed data: `./seed.sh` (loads `category` then `course` fixtures)
- No lint, typecheck, or test commands configured

## Architecture
- Django 5.0 + graphene-django (GraphQL API, not REST)
- Single app: `core` (models, schema, admin)
- GraphQL endpoint: `/graphql/` (GraphiQL enabled)
- GraphQL schema: `core/schema.py` → referenced in `GRAPHENE["SCHEMA"]` setting
- REST URL namespace: `v1` → `core/urls.py` (currently empty)

## Environment
- Requires `.env` with: `SECRET_KEY`, `DB_NAME`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
- DB connection requires SSL (`sslmode: require` in settings)
- Local DB runs in Docker container
- `DEBUG` is `True` when `RENDER` env var is absent

## Models
- `Category`: self-referential `parent` FK (tree structure — categories and subcategories share one table)
- `Course.level`: integer choices (1=Introductorio, 2=Intermedio, 3=Avanzado, 4=Completo), not strings
- `Course.category` / `Course.subcategory`: both FK to `Category` with different `related_name`

## Deployment
- Render (`render.yaml`): `build.sh` runs `poetry install`, `collectstatic`, `migrate`
- Production: `gunicorn backend.wsgi:application`
