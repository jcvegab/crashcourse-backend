# crashcourse-backend

Crashcourse | Django + GraphQL Backend

## Requirements

- Python ^3.10
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

```bash
# Install dependencies
uv sync

# Apply pending migrations
uv run ./manage.py migrate

# Start dev server
uv run ./manage.py runserver
```

## Environment variables

Copy `.env.example` to `.env` and configure:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` | Database name |
| `DB_HOST` | Database host |
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

## Deployment

Deployed on Render. Build command uses `uv` for dependency installation.

Production URL: https://api.crashcourse.jcvegab.dev
