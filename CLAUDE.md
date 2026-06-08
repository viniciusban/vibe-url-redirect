# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Standing Instructions

Save every prompt to `_vibe/prompts.md`. When committing changes, add prompts file too. Don't commit automatically. Ask for confirmation first.

## Project

Steerer is a URL redirection FastAPI service backed by PostgreSQL. Three endpoints: create a named alias for a URL, redirect an alias to its destination URL, and report hit counts. See `_vibe/plan-v2.md` for full business rules and `_vibe/issue-{n}.md` for work items.

## Commands

```bash
make install          # create venv (uv), install deps, wire pre-commit hook
make check            # lint + typecheck + test in one shot
make test             # pytest (non-verbose)
make test OPT="-k test_name"          # run a single test by name
make test OPT="tests/test_redirect.py" # run a single test file
make typecheck        # mypy on src/ only (never runs on tests/)
make lint             # ruff check src/ tests/
make format           # ruff import-sort + format src/ tests/
make migrations       # create Piccolo auto-migration
make migrate          # apply pending migrations
make migration-status # show applied migrations
```

Docker dev environment (source auto-reloads on save):
```bash
docker compose up
```

## Architecture

`src/steerer/` is the package root (installed via `uv` in editable mode).

- `main.py` — creates the FastAPI `app` and registers routers.
- `routers/routes.py` — handles both `POST /routes/` and `GET /routes/{alias}` (same resource, same table).
- `routers/redirect.py` — handles `GET /redirect/{alias}`.
- `tables.py` — Piccolo ORM table `url_route` (to be added in Issue 2).
- `schemas.py` — Pydantic request/response models.
- `logging.py` — structured JSON log helpers; all endpoints emit `{"action", "alias", "error_code"}` at INFO level.
- `piccolo_conf.py` — DB engine config (reads `DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT` env vars); exposes `DB` and `APP_REGISTRY` for Piccolo.
- `piccolo_app.py` — Piccolo `APP_CONFIG` pointing to `migrations/`.

Piccolo migration commands require `PICCOLO_CONF=steerer.piccolo_conf`; the Makefile sets this automatically.

All timestamps are UTC with no timezone stored in the DB (`TIMESTAMP`, not `TIMESTAMPTZ`).

## Testing

Tests use FastAPI's `TestClient`. No DB mocking — tests hit a real database configured via `DATABASE_URL`. Tables are truncated between tests via a pytest fixture in `conftest.py`. No type hints in test files.

## Code Style

- Return early; prefer flat code over nested conditions.
- Minimal logic in views — business logic belongs in service modules.
- No `__pycache__` directories (`PYTHONDONTWRITEBYTECODE=1` is exported by the Makefile).
- Pre-commit hook runs `lint → typecheck`.
