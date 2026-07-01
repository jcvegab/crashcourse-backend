# Crashcourse Backend

Backend de Crashcourse: API Django 5 para una plataforma de cursos, con GraphQL mediante `graphene-django`, endpoints REST con Django Ninja, PostgreSQL, Docker y despliegue en Render.

## Project Scope

- Catálogo de cursos y categorías jerárquicas.
- API GraphQL para consumo server-side desde [`crashcourse-frontend`](https://github.com/jcvegab/crashcourse-frontend).
- REST API mínima para health check y auth mock.
- Configuración productiva con `gunicorn`, WhiteNoise, PostgreSQL SSL y CORS para dominio principal/previews.
- Fixtures de seed para datos iniciales de categorías y cursos.

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) como package manager
- PostgreSQL local o vía Docker
- Docker + Docker Compose para simulación productiva

## Quick Start

```bash
# Copy environment file
cp .env.example .env.local

# Install dependencies
uv sync

# Apply pending migrations
uv run ./manage.py migrate

# Seed local data
./seed.sh

# Start dev server
uv run ./manage.py runserver
```

Open [http://localhost:8000/graphql/](http://localhost:8000/graphql/) when `DEBUG=True`.

## Docker

Docker simula producción: usa `gunicorn`, activa `RENDER=true`, corre con PostgreSQL en contenedor y no tiene hot reload.

```bash
# Uses .env.local for compose interpolation and container env
docker compose --env-file .env.local up --build -d

# Run migrations in container
docker compose exec web uv run python manage.py migrate

# Seed data
docker compose exec web bash seed.sh
```

To see code changes in Docker, rebuild the image with `docker compose --env-file .env.local up --build -d`.

## Environment Variables

Copy `.env.example` to `.env.local` for local development. `.env` is only fallback when `.env.local` is missing and `RENDER` is not active.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key. Required in production. |
| `DEBUG` | Enables GraphiQL, Ninja docs and Django debug pages when `True`. |
| `ALLOWED_HOSTS` | Comma-separated Django hosts. Render hostname is appended automatically. |
| `DB_NAME` | PostgreSQL database name. |
| `DB_HOST` | Database host. Use `localhost` locally and `db` in Docker. |
| `DB_USER` | PostgreSQL user. |
| `DB_PASSWORD` | PostgreSQL password. |
| `DB_PORT` | PostgreSQL port. |
| `CORS_ORIGIN_MAIN` | Production frontend origin. Default: `https://crashcourse.jcvegab.dev`. |
| `CORS_ORIGIN_REGEX` | Production preview origin regex. Default: `^https://.*-jcvegab\.vercel\.app$`. |
| `RENDER` | Platform flag. Enables production mode, SSL DB connections and WhiteNoise storage. |
| `RENDER_EXTERNAL_HOSTNAME` | Render hostname injected by platform and appended to `ALLOWED_HOSTS`. |
| `SECURE_SSL_REDIRECT` | Forces HTTPS redirect when `True`. |

## Available Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | REST API root with name/version. |
| `/graphql/` | GET/POST | GraphQL API. GraphiQL only when `DEBUG=True`. |
| `/health/` | GET | Health check with database connectivity status. |
| `/auth/login/` | POST | Mock token login. |
| `/auth/refresh/` | POST | Mock token refresh. |
| `/docs` | GET | Django Ninja Swagger docs only when `DEBUG=True`. |
| `/openapi.json` | GET | OpenAPI schema only when `DEBUG=True`. |
| `/admin/` | GET/POST | Django admin panel. |

## Development Commands

| Command | Description |
|---|---|
| `uv sync` | Install dependencies from `uv.lock`. |
| `uv run ./manage.py runserver` | Start local Django server. |
| `uv run ./manage.py makemigrations` | Create Django migrations. |
| `uv run ./manage.py migrate` | Apply Django migrations. |
| `./seed.sh` | Load category and course fixtures. |
| `uv run ruff check .` | Run lint checks. |
| `uv run ruff format .` | Format Python files. |
| `uv run ./manage.py test` | Run Django tests. |

## Architecture

- **Framework:** Django 5.0 with one first-party app, `core`.
- **GraphQL:** `core/schema.py` defines `CourseType`, `CategoryType` and read queries for courses/categories.
- **REST:** `core/api.py` exposes Django Ninja routes at root level.
- **Models:** `Category` is self-referential via `parent`; `Course` links to `category` and `subcategory` and stores integer `level` choices.
- **Settings:** `backend/env_adapter.py` centralizes platform detection; `backend/settings.py` derives production behavior from `RENDER`, not `DEBUG`.
- **Codebase memory:** indexed as `home-jcvegab-jcvegab-projects-crashcourse-backend` for graph-based discovery.

## Documentation

- `docs/documentation-update-plan.md` — applied plan for README, package metadata, docs and GitHub topics.
- `docs/architecture.md` — app structure, runtime modes and data model notes.
- `docs/api-reference.md` — GraphQL and REST endpoint reference.
- `docs/deployment.md` — local, Docker and Render deployment notes.

## Deployment

Target: [Render](https://render.com) with Docker runtime.

`render.yaml` points to `Dockerfile` and runs migrations through `preDeployCommand` before each deploy. The container starts `gunicorn --bind 0.0.0.0:${PORT:-8000} backend.wsgi:application`.

Production URL: https://api.crashcourse.jcvegab.dev

## Related

- [crashcourse-frontend](https://github.com/jcvegab/crashcourse-frontend) — Next.js client consuming this API.

## License

MIT

## Author

Joseph Vega — admin@jcvegab.dev
