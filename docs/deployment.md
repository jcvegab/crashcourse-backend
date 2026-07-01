# Deployment

## Local Development

```bash
cp .env.example .env.local
uv sync
uv run ./manage.py migrate
./seed.sh
uv run ./manage.py runserver
```

Use `DB_HOST=localhost` for a local PostgreSQL instance.

## Docker Production Simulation

`docker-compose.yml` starts PostgreSQL and the Django app using the project `Dockerfile`.

```bash
docker compose --env-file .env.local up --build -d
docker compose exec web uv run python manage.py migrate
docker compose exec web bash seed.sh
```

Use `DB_HOST=db` in `.env.local` when running through Docker Compose.

The web service sets:

```text
RENDER=true
PORT=8000
```

That makes local Docker behavior match production more closely: DB SSL mode follows production settings, static files use WhiteNoise and the app starts through `gunicorn`.

## Render

Render uses `render.yaml` with Docker runtime:

```yaml
runtime: docker
dockerfilePath: Dockerfile
preDeployCommand: python manage.py migrate
```

Required production env vars:

| Variable | Notes |
|---|---|
| `SECRET_KEY` | Required by Django. |
| `DB_NAME` | Render PostgreSQL database name. |
| `DB_HOST` | Render PostgreSQL host. |
| `DB_USER` | Render PostgreSQL user. |
| `DB_PASSWORD` | Render PostgreSQL password. |
| `DB_PORT` | Usually `5432`. |
| `ALLOWED_HOSTS` | Include custom API domain when needed. |
| `CORS_ORIGIN_MAIN` | Public frontend origin. |
| `CORS_ORIGIN_REGEX` | Vercel preview origin regex. |

Render injects `RENDER=true` and `RENDER_EXTERNAL_HOSTNAME` automatically.

## Release Checklist

- Run `uv run ruff check .`.
- Run `uv run ./manage.py test`.
- Confirm migrations are committed.
- Confirm Render env vars match `.env.example` plus production secrets.
- Deploy and verify `/health/` returns `status: ok` and `db: ok`.
