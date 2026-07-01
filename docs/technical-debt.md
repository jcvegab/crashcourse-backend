# TODOs And Technical Debt

## TODOs

- Implement user registration mutation.
- Implement token auth (JWT) mutation.
- Implement account verification flow.
- Implement password reset flow.
- Register `graphql_auth` models in admin.

## Technical Debt

- Authentication is still incomplete and depends on future `graphql_auth` integration work.

## Follow-Ups

- Keep API docs aligned when auth mutations become active.

## Known Risks

- Auth endpoints are currently mock/minimal and should not be treated as production-ready.
