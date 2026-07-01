# Architecture

`crashcourse-backend` is a Django 5 API with one first-party app, `core`.

## Project Layout

| Path | Responsibility |
|---|---|
| `backend/settings.py` | Django settings, environment loading, CORS, database, GraphQL and security flags. |
| `backend/env_adapter.py` | Platform detection for local vs Render runtime. |
| `backend/urls.py` | Root URL configuration for admin, GraphQL and REST routes. |
| `core/models.py` | Category and Course models. |
| `core/schema.py` | GraphQL schema and resolvers. |
| `core/api.py` | Django Ninja REST endpoints. |
| `core/fixtures/` | Seed data for categories and courses. |
| `Dockerfile` | Production-style container image. |
| `docker-compose.yml` | Local production simulation with PostgreSQL. |
| `render.yaml` | Render deployment configuration. |

## Runtime Modes

`RENDER` and `DEBUG` are independent flags.

| Mode | Trigger | Behavior |
|---|---|---|
| Local dev | `RENDER` unset/false | Loads `.env.local` when present, otherwise `.env`; DB SSL disabled. |
| Docker simulation | `RENDER=true` in compose | Uses production settings with local container services. |
| Render production | Render platform env | DB SSL enabled, WhiteNoise manifest storage enabled, platform hostname allowed. |

`DEBUG=True` enables GraphiQL, Django Ninja docs and Django debug pages. It does not decide production mode.

## Data Model

`Category` represents both categories and subcategories through a self-referential `parent` field.

`Course` stores pricing, discount, score, tutor username, user count and two category links:

- `category` with `related_name="courses"`
- `subcategory` with `related_name="subcourses"`

`Course.level` is an integer choice:

| Value | Label |
|---|---|
| `1` | `Introductorio` |
| `2` | `Intermedio` |
| `3` | `Avanzado` |
| `4` | `Completo` |

## API Boundaries

- GraphQL is the primary read API for frontend course/category data.
- REST is intentionally small and currently covers root, health and mock auth.
- REST routes are mounted at root.
- Django Ninja docs and OpenAPI output are hidden when `DEBUG=False`.

## Local Code Analysis

Use the local code analysis tool for structural discovery before broad text searches. Do not document index names, local paths or machine-specific details.
