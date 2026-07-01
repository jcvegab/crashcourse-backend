# API Reference

Base URL in production:

```text
https://api.crashcourse.jcvegab.dev
```

Local development default:

```text
http://localhost:8000
```

## GraphQL

Endpoint:

```text
/graphql/
```

GraphiQL is available only when `DEBUG=True`.

### Queries

| Query | Arguments | Returns |
|---|---|---|
| `course` | `id: Int` | One course or `null`. |
| `courses` | None | List of courses. |
| `category` | `id: Int` | Field is declared in schema; resolver is not implemented yet. |
| `categories` | None | List of categories. |

### Example

```graphql
query Courses {
  courses {
    id
    name
    price
    realPrice
    discount
    level
    score
    tutorUsername
    users
    category {
      id
      name
    }
    subcategory {
      id
      name
    }
  }
}
```

## REST

REST endpoints are mounted at root through Django Ninja. There is no `/v1` prefix.

| Endpoint | Method | Response | Notes |
|---|---|---|---|
| `/` | GET | `{ "message": "CrashCourse API", "version": "0.1.0" }` | API root. |
| `/health/` | GET | `{ "status": "ok", "db": "ok" }` | Returns `error` values when DB connection fails. |
| `/auth/login/` | POST | Mock access/refresh tokens and user object. | Not production auth. |
| `/auth/refresh/` | POST | Mock refreshed access token. | Not production auth. |
| `/docs` | GET | Swagger UI. | Only when `DEBUG=True`. |
| `/openapi.json` | GET | OpenAPI schema. | Only when `DEBUG=True`. |

### Login Payload

```json
{
  "username": "mock_user",
  "password": ""
}
```

### Login Response

```json
{
  "access": "mock-access-token",
  "refresh": "mock-refresh-token",
  "user": {
    "id": 1,
    "username": "mock_user"
  }
}
```

## Admin

Django admin is mounted at:

```text
/admin/
```
