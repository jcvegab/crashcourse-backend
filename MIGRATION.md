# Migration Plan

## Step 1: Update dependencies

Review and update all dependencies to their latest compatible versions.

**Current dependencies:**

| Package | Current | Action |
|---|---|---|
| python | ^3.10 | Pin to `3.13` |
| Django | ^5.0 | Bump to latest 5.x patch |
| graphene-django | ^3.1.5 | Bump to latest 3.x |
| django-cors-headers | ^4.3.1 | Bump to latest |
| django-environ | ^0.11.2 | Bump to latest |
| whitenoise[brotli] | ^6.6.0 | Bump to latest |
| gunicorn | ^21.2.0 | Bump to latest |
| psycopg | ^3.1.16 | Bump to latest 3.x |

**Tasks:**

- [ ] Check latest versions on PyPI for each dependency
- [ ] Update `pyproject.toml` with new version constraints
- [ ] Verify `python manage.py runserver` starts without errors
- [ ] Verify GraphQL endpoint (`/graphql/`) responds correctly

---

## Step 2: Migration to uv

Replace Poetry with [uv](https://docs.astral.sh/uv/) as the package manager.

**Tasks:**

- [ ] Install uv globally (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] Create `.python-version` file with the target Python version
- [ ] Convert `pyproject.toml` from Poetry format to PEP 621:
  - Move `[tool.poetry.dependencies]` → `[project.dependencies]`
  - Replace `poetry-core` build-system with `hatchling` or `setuptools`
  - Remove `[tool.poetry]` section, add `[project]` with name/version/description/authors
- [ ] Generate `uv.lock` via `uv lock` y commitear al repo (Render lo detecta automáticamente)
- [ ] Remove `poetry.lock`
- [ ] Update `.gitignore`: ensure `uv.lock` is tracked, `.venv/` ignored
- [ ] Create `.env.example`:
  ```
  SECRET_KEY=
  DB_NAME=
  DB_HOST=
  DB_USER=
  DB_PASSWORD=
  DB_PORT=
  CORS_ORIGIN_MAIN=https://crashcourse.jcvegab.dev
  CORS_ORIGIN_REGEX=^https://.*-jcvegab\.vercel\.app$
  ```
- [ ] Create `.env` from `.env.example` before running any `uv run` commands
- [ ] Update `AGENTS.md` commands:
  - Install: `uv sync`
  - Dev server: `uv run ./manage.py runserver`
  - Migrations: `uv run ./manage.py makemigrations` / `uv run ./manage.py migrate`
- [ ] Verify full workflow: `uv sync` → `uv run ./manage.py runserver`

---

## Step 3: Setup formatting and linting

Add **Ruff** as the single tool for linting and formatting (replaces flake8 + isort + black).

**Tasks:**

- [ ] Add ruff as a dev dependency: `uv add --dev ruff`
- [ ] Add Ruff configuration to `pyproject.toml`:
  ```toml
  [tool.ruff]
  target-version = "py313"
  line-length = 120

  [tool.ruff.lint]
  select = ["E", "F", "I", "UP", "B", "SIM"]

  [tool.ruff.lint.isort]
  known-first-party = ["backend", "core"]
  ```
- [ ] Run `uv run ruff format .` to auto-format all files
- [ ] Run `uv run ruff check . --fix` to auto-fix lint issues
- [ ] Manually resolve any remaining lint warnings
- [ ] Update `AGENTS.md` with lint/format commands:
  - Lint: `uv run ruff check .`
  - Format: `uv run ruff format .`

---

## Step 4: Analyze codebase for improvements

Audit the entire codebase for issues, dead code, inconsistencies, and missing best practices.

**Issues identified:**

### settings.py

- [ ] `CORS_ALLOW_ALL_ORIGINS = True` contradicts `CORS_ALLOWED_ORIGINS` list — decide one approach
- [ ] `STATICFILES_STORAGE` is deprecated in Django 5.0 — migrate to `STORAGES` setting
- [ ] `CORS_ALLOWED_ORIGINS` contains wildcard `"https://*-jcvegab.vercel.app"` which is not supported — use `CORS_ALLOWED_ORIGIN_REGEXES` instead
- [ ] Inconsistent env var access: mixes `os.environ.get()` and `environ.Env()` — standardize to `django-environ`
- [ ] `SECRET_KEY` uses `os.environ.get()` which returns `None` silently — should fail fast or provide dev fallback

### schema.py

- [ ] Commented-out `graphql_auth` mutations and imports — dead code from unfinished auth feature
- [ ] `resolve_course` uses `Course.objects.get(pk=id)` which raises `DoesNotExist` instead of returning `None` gracefully
- [ ] No pagination on `courses` and `categories` list queries

### admin.py

- [ ] Commented-out `graphql_auth` model registration — dead code

### Boilerplate files

- [ ] `core/tests.py` — empty (only boilerplate comment)
- [ ] `backend/urls.py` — contains Django boilerplate comments

### General

- [ ] No tests written (`core/tests.py` is empty)
- [ ] `seed.sh` needs update to use `uv run` (tracked here, fixed in Step 6)

---

## Step 5: Refactor code

Clean up the codebase based on findings from Step 4.

**Tasks:**

### Code cleanup

- [x] Create `health` endpoint (Done)
- [x] Create mock JWT endpoints (`/v1/auth/login`, `/v1/auth/refresh`) (Done)
- [ ] Remove commented-out auth code from `core/schema.py`
- [ ] Remove commented-out code from `core/admin.py`
- [ ] Remove boilerplate comments from `core/tests.py` and `backend/urls.py`

### Technical debt tracking

- [ ] Create `TODO.md` in project root:
  ```markdown
  # Technical Debt

  ## Authentication (from graphql_auth)
  - [ ] Implement user registration mutation
  - [ ] Implement token auth (JWT) mutation
  - [ ] Implement account verification flow
  - [ ] Implement password reset flow
  - [ ] Register graphql_auth models in admin
  ```

### Bug fixes & improvements

- [ ] Fix `resolve_course` to use `filter().first()` instead of `.get()`
- [ ] Fix CORS: use `CORS_ALLOWED_ORIGINS` for localhost and `CORS_ALLOWED_ORIGIN_REGEXES` for Vercel domains via env vars
- [ ] Migrate `STATICFILES_STORAGE` to `STORAGES` dict (Django 5.0+)
- [ ] Standardize env var access to `django-environ` in `settings.py`
- [ ] Add `SECRET_KEY` fail-fast or dev fallback

---

## Step 6: Docker setup for local development

Containerize the application with Docker for a reproducible local development environment con PostgreSQL integrado.

**Tasks:**

- [ ] Create `Dockerfile`:
  ```dockerfile
  FROM python:3.13-slim

  # Install uv
  COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

  WORKDIR /app

  # Copy dependency files first (cache layer)
  COPY pyproject.toml uv.lock ./
  RUN uv sync --frozen --no-dev

  # Copy source code
  COPY . .

  EXPOSE 8000

  CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
  ```

- [ ] Create `docker-compose.yml`:
  ```yaml
  services:
    db:
      image: postgres:17-alpine
      restart: unless-stopped
      environment:
        POSTGRES_DB: ${DB_NAME}
        POSTGRES_USER: ${DB_USER}
        POSTGRES_PASSWORD: ${DB_PASSWORD}
      ports:
        - "5432:5432"
      volumes:
        - postgres_data:/var/lib/postgresql/data
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
        interval: 5s
        timeout: 5s
        retries: 5

    web:
      build: .
      command: uv run python manage.py runserver 0.0.0.0:8000
      volumes:
        - .:/app
      ports:
        - "8000:8000"
      env_file:
        - .env
      depends_on:
        db:
          condition: service_healthy

  volumes:
    postgres_data:
  ```

- [ ] Update `.env.example` con valores para desarrollo local:
  ```
  SECRET_KEY=dev-secret-key-change-in-production
  DB_NAME=crashcourse
  DB_HOST=db
  DB_USER=postgres
  DB_PASSWORD=postgres
  DB_PORT=5432
  CORS_ORIGIN_MAIN=http://localhost:3000
  CORS_ORIGIN_REGEX=^https://.*-jcvegab\.vercel\.app$
  ```
  > **Nota:** `DB_HOST=db` hace referencia al nombre del servicio en docker-compose, no a `localhost`.

- [ ] Add to `.gitignore`:
  ```
  .env
  ```

- [ ] Update `AGENTS.md` con comandos Docker:
  - Start: `docker compose up`
  - Build: `docker compose up --build`
  - Migrations: `docker compose exec web uv run python manage.py migrate`
  - Shell: `docker compose exec web uv run python manage.py shell`
  - Seed: `docker compose exec web bash seed.sh`

- [ ] Verify full local workflow:
  1. `cp .env.example .env`
  2. `docker compose up --build`
  3. `docker compose exec web uv run python manage.py migrate`
  4. Verify `http://localhost:8000/health/` responds correctly
  5. Verify `http://localhost:8000/graphql/` responds correctly

---

## Step 7: Standardize deployment to Render

Update deployment configuration to use `uv`. Render detecta `uv` automáticamente si `uv.lock` está commiteado — no se requiere instalación manual.

**Tasks:**

- [ ] Update `build.sh`:
  ```bash
  #!/usr/bin/env bash
  set -o errexit

  uv sync --frozen --no-dev
  uv run python manage.py collectstatic --no-input
  uv run python manage.py migrate
  ```

- [ ] Update `render.yaml`:
  ```yaml
  services:
    - type: web
      name: core
      runtime: python
      buildCommand: "./build.sh"
      startCommand: "uv run gunicorn backend.wsgi:application"
      envVars:
        - key: SECRET_KEY
          generateValue: true
        - key: WEB_CONCURRENCY
          value: 4
  ```

- [ ] Update `seed.sh`:
  ```bash
  #!/usr/bin/env bash
  set -o errexit

  uv run python manage.py loaddata category
  uv run python manage.py loaddata course
  ```

- [ ] Test full deployment pipeline: build → collectstatic → migrate → gunicorn start
- [ ] Update `AGENTS.md` deployment section

---

## Step 8: Finalize documentation

**Tasks:**

### Update `pyproject.toml`

- [ ] Update author: `authors = [{name = "Joseph Vega", email = "admin@jcvegab.dev"}]`
- [ ] Add repository URL: `urls = {Repository = "https://github.com/jcvegab/crashcourse-backend"}`
- [ ] Confirm file is fully migrated to PEP 621

### Update `README.md`

- [ ] Replace `poetry` commands with `uv` equivalents
- [ ] Add documentation for environment variables (referencing `.env.example`)
- [ ] Add Docker quickstart section:
  ```bash
  cp .env.example .env
  docker compose up --build
  docker compose exec web uv run python manage.py migrate
  ```
- [ ] Document available endpoints:
  - GraphQL API: `https://api.crashcourse.jcvegab.dev/graphql/`
  - Health Check: `GET /health/`
  - Mock Auth Login: `POST /v1/auth/login/`
  - Mock Auth Refresh: `POST /v1/auth/refresh/`