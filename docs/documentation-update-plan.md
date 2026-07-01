# Documentation Update Plan

Plan aplicado para dejar la documentación y metadata del repositorio alineadas con el stack real de `crashcourse-backend`.

## Goals

- Actualizar `README.md` con scope, setup, endpoints reales, comandos, arquitectura y despliegue.
- Usar metadata canónica Python en `pyproject.toml` en lugar de crear un `package.json` Node no usado por el backend.
- Crear documentación adicional en `docs/` para arquitectura, API y deployment.
- Añadir topics de GitHub relacionados con Django, GraphQL, REST, PostgreSQL, Docker, Render y plataforma de cursos.
- Cerrar el trabajo con validación y commit dedicado.

## Repository Metadata

Este repositorio no usa Node.js ni npm. Por eso no se añadió `package.json`; la metadata equivalente vive en `pyproject.toml`, que es el manifiesto estándar del proyecto Python.

Actualizaciones aplicadas:

- `description` describe el producto y stack real.
- `keywords` incluye framework, API, base de datos, deployment y dominio funcional.
- `README.md` enlaza el frontend relacionado y el índice de docs.

## Documentation Files

| File | Purpose |
|---|---|
| `README.md` | Entrada principal para setup, comandos, endpoints y despliegue. |
| `docs/architecture.md` | Estructura, runtime modes, data model y convenciones. |
| `docs/api-reference.md` | Referencia GraphQL y REST. |
| `docs/deployment.md` | Desarrollo local, Docker y Render. |
| `docs/documentation-update-plan.md` | Plan aplicado y cierre del trabajo. |

## GitHub Topics

Topics objetivo:

- `api`
- `course-platform`
- `django`
- `django-ninja`
- `docker`
- `graphene-django`
- `graphql`
- `postgresql`
- `python`
- `render`
- `rest-api`

## Verification

- Run `uv run ruff check .`.
- Run `uv run ./manage.py test`.
- Review `git diff` before commit.
- Commit with a docs-focused conventional commit message.
