#!/usr/bin/env bash
# exit on error
set -o errexit

uv sync --frozen --no-dev
uv run python manage.py collectstatic --no-input
uv run python manage.py migrate
