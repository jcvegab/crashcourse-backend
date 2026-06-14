FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Improve startup performance
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first (cache layer)
COPY pyproject.toml uv.lock ./

# Runtime dependency for PostgreSQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies only
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY . .

# Simulate production environment
ENV RENDER=true
ENV PATH="/app/.venv/bin:$PATH"

# Collect static files
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} backend.wsgi:application"]
