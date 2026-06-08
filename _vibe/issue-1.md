# Issue 1 — Project scaffolding and development environment

Completed: 2026-06-08 05:55 UTC

Set up the full skeleton so development can start.

## Scope

- **Docker Compose**: `steerer` service + `postgres:18` container, database name `steerer_db`.
- **Dockerfile**: Python 3.14 image for the app.
- **`pyproject.toml`**: managed with uv, Python 3.14 pinned; deps include FastAPI, Piccolo, Pydantic, uvicorn.
- **FastAPI app skeleton**: no business routes; health check at `GET /` returning 200.
- **Piccolo config**: `piccolo_conf.py` (DB connection from env), `piccolo_app.py` (app registry).
- **All Makefile targets wired**: `install`, `format`, `lint`, `typecheck`, `test`, `migrations`, `migrate`, `migration-status`.
- **Pre-commit hook**: installed by `make install`; runs `make format && make lint && make typecheck`.

## Criteria of Done

- `make install` completes without error; pre-commit hook is present in `.git/hooks/pre-commit`.
- `docker compose up` starts both `steerer` and `postgres` services without error.
- `GET /` returns 200.
- `make test` passes (empty suite is acceptable).
- `make format`, `make lint`, `make typecheck` all exit 0.
- `make migrations`, `make migrate`, `make migration-status` are wired (may be no-ops at this stage).

## Tests

No business logic tests in this issue. The criteria of done verify the infrastructure directly.
