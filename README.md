# crashcourse-backend

Crashcourse | Django + GraphQL Backend

## Requirements

- Python ^3.13
- [uv](https://docs.astral.sh/uv/) (package manager)
- PostgreSQL (local or via Docker)

## Quick Start

### Local development

```bash
# Copy environment file
cp .env.example .env

# Install dependencies
uv sync

# Apply pending migrations
uv run ./manage.py migrate

# Start dev server
uv run ./manage.py runserver
```

### Docker (Production Simulation)

Docker is configured to simulate the production environment (Render) exactly. It uses `gunicorn`, disables `DEBUG` mode, and serves pre-compiled static files. It does **not** use hot-reload.

```bash
# Copy environment file
cp .env.example .env
# For Docker, edit DB_HOST to 'db' in .env

# Build and start services
docker compose up --build -d

# Run migrations in container
docker compose exec web uv run python manage.py migrate

# Seed data
docker compose exec web bash seed.sh
```

*Note: To see local code changes in Docker, you must rebuild the image using `docker compose up --build -d`.*

## Environment variables

Copy `.env.example` to `.env` and configure:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` | Database name |
| `DB_HOST` | Database host (use `db` for Docker, `localhost` for local) |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_PORT` | Database port |
| `CORS_ORIGIN_MAIN` | Production CORS origin (default: `https://crashcourse.jcvegab.dev`) |
| `CORS_ORIGIN_REGEX` | Production CORS regex for Vercel previews (default: `^https://.*-jcvegab\.vercel\.app$`) |

## Available endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/graphql/` | GET/POST | GraphQL API (GraphiQL enabled) |
| `/health/` | GET | Health check (returns DB status) |
| `/v1/auth/login/` | POST | Mock JWT login |
| `/v1/auth/refresh/` | POST | Mock JWT refresh |
| `/admin/` | GET/POST | Django admin panel |

## Development commands

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Run tests
uv run ./manage.py test

# Seed data
./seed.sh
```

## Deployment

Deployed on [Render](https://render.com). Build command uses `uv` for dependency installation.

Production URL: https://api.crashcourse.jcvegab.dev

## License

MIT

## Author

Joseph Vega — admin@jcvegab.dev
