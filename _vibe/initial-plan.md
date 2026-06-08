# Steerer — Initial Plan

## Table Name Decision

**`route`**

Aligns with the REST endpoint naming (`/routes/`), so code reads consistently end-to-end.

---

## Overview

Steerer is a FastAPI service backed by PostgreSQL. Three capabilities: create named URL shortcuts, serve HTTP redirects, and report hit counts. Piccolo ORM handles DB access and migrations. Everything runs in Docker Compose for development.

---

## Business Rules

**Create route (POST `/routes/`)**
- Slugify `origin_name`: lowercase, replace spaces and non-alphanumeric chars with hyphens, collapse consecutive hyphens.
- Check `origin_slug` uniqueness → 400 + error body if duplicate.
- Store row with `hits=0`, `created_at=now()`.
- Respond 200 + `{"origin_slug": "..."}`.

**Redirect (GET `/redirect/{origin_slug}`)**
- 404 if slug not in DB.
- 410 if `now() >= expiration`.
- 301 + `Location: <destination_url>` on happy path; atomically increment `hits`.

**Hit count (GET `/routes/{origin_slug}`)**
- 404 if slug not in DB.
- 200 + `{"origin_slug": "...", "hits": N}`.

**Logging (all endpoints)**
Structured JSON on every request: `{"action": "...", "value": "...", "error_code": N}` + optional `"reason"`. Always INFO level.

---

## Tests

Each handler gets its own test file. Cover:
- Happy path (status code, response body, log message).
- Each error path (status code, response body, log message).

Use FastAPI's `TestClient`. DB isolation via a separate test database (set via env var `DATABASE_URL`); wipe tables between tests with a fixture.

No type hints in test files (per requirements). No mocking the database.

---

## API Endpoints

| Method | Path | Handler |
|--------|------|---------|
| `POST` | `/routes/` | Create route |
| `GET` | `/redirect/{origin_slug}` | Redirect |
| `GET` | `/routes/{origin_slug}` | Hit count |

All request/response bodies are JSON. Pydantic models for validation and serialization.

---

## Database

Table `route`:

| Column | Type | Notes |
|--------|------|-------|
| `id` | `SERIAL` | PK |
| `origin_name` | `VARCHAR(100)` | NOT NULL |
| `origin_slug` | `VARCHAR(100)` | NOT NULL, UNIQUE, indexed |
| `destination_url` | `TEXT` | NOT NULL |
| `expiration` | `TIMESTAMPTZ` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, default `now()` |
| `hits` | `INTEGER` | NOT NULL, default `0` |

Piccolo auto-migration manages the schema.

---

## Code & Directory Structure

```
steerer/
├── _vibe/
│   ├── initial-prompt.md
│   └── initial-plan.md
├── src/
│   └── steerer/
│       ├── __init__.py
│       ├── main.py           # FastAPI app, router registration
│       ├── piccolo_conf.py   # DB connection config
│       ├── piccolo_app.py    # Piccolo app registry
│       ├── tables.py         # ORM table definition
│       ├── schemas.py        # Pydantic request/response models
│       ├── logging.py        # Structured log helpers
│       └── routers/
│           ├── __init__.py
│           ├── routes.py     # POST /routes/ + GET /routes/{slug}
│           └── redirect.py   # GET /redirect/{slug}
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # TestClient, DB fixtures
│   ├── test_create_route.py
│   ├── test_redirect.py
│   └── test_hit_count.py
├── migrations/
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```

Note: `routers/routes.py` handles both `POST /routes/` and `GET /routes/{slug}` — they share the same resource prefix and table model, reducing jumping between files.

---

## Makefile Targets

| Target | Action |
|--------|--------|
| `make install` | Create venv with uv, install deps, set pre-commit hook |
| `make test [OPT=...]` | Run pytest (non-verbose; pass extra opts via `OPT`) |
| `make typecheck` | Run mypy on `src/` only |
| `make lint` | Run ruff check on `src/` |
| `make format` | Run ruff format + import sort on `src/` |
| `make migrations` | Create Piccolo auto-migration |
| `make migrate` | Apply pending migrations |
| `make migration-status` | Show current applied migration |

Pre-commit hook runs `make format && make lint && make typecheck` (format first so lint sees clean code).

---

## User Stories — Vertical Slices

### Issue 1 — Project scaffolding and development environment

Set up the full skeleton so the team can develop locally.

- Docker Compose: `steerer` service + `postgres:18` container, `steerer_db` database.
- Dockerfile for the app.
- `pyproject.toml` with uv; pin Python 3.14.
- FastAPI app skeleton (no routes yet) responding 200 at `/`.
- All Makefile targets working (`install`, `format`, `lint`, `typecheck`, `test`).
- Pre-commit hook installed by `make install`.

**Done when:** `make install && docker compose up` starts both services; `make test` passes (empty suite).

---

### Issue 2 — Create route endpoint

Implement `POST /routes/`.

- Piccolo table definition for `route`.
- `make migrations && make migrate` creates the table.
- Slugification logic (pure function, unit-tested).
- Handler: happy path (200) and duplicate slug (400).
- Structured logging for both cases.

**Done when:** all tests pass; mypy and ruff clean.

---

### Issue 3 — Redirect endpoint

Implement `GET /redirect/{origin_slug}`.

- Handler: 301 happy path (with `Location` header and hit increment), 410 expired, 404 not found.
- Hit counter increment is atomic (Piccolo atomic update).
- Structured logging for all three cases.

**Done when:** all tests pass; mypy and ruff clean.

---

### Issue 4 — Hit count endpoint

Implement `GET /routes/{origin_slug}`.

- Handler: 200 with `{"origin_slug": ..., "hits": N}`, 404 not found.
- Structured logging for both cases.

**Done when:** all tests pass; mypy and ruff clean.

---

### Issue 5 — Migration management Makefile targets

Wire up `make migrations`, `make migrate`, and `make migration-status` so they work inside the Docker environment.

**Done when:** running all three targets against the dev DB produces correct output.
