# Steerer — Plan v2

## Overview

Steerer is a FastAPI service backed by PostgreSQL. Three capabilities: create named URL aliases, serve HTTP redirects, and report hit counts. Piccolo ORM handles DB access and auto-migrations. Everything runs in Docker Compose for development.

> **Improvement noted:** The functional spec states the create-route request accepts a name, destination URL, and expiration timestamp, but the example request body omits `expiration`. Since the spec is authoritative over the example, `expiration` is treated as a required request field.

---

## Business Rules

### Create route — POST `/routes/`

- `name`: required, strip leading/trailing whitespace; blank after strip → 400 (error_code 4, reason "name is required").
- `destination_url`: required, strip leading/trailing whitespace; blank after strip → 400 (error_code 4, reason "destination_url is required").
- `expiration`: required, format `YYYY-MM-DD HH:mm:ss`, treated as UTC, stored without timezone; invalid format → 400 (error_code 4, reason "invalid expiration").
- Slugify `name`: lowercase, replace non-alphanumeric chars with hyphens, collapse consecutive hyphens, strip edge hyphens → `alias` (computed field on request model).
- Empty `alias` after slugification → 400 (error_code 4, reason "Invalid name").
- Check `alias` uniqueness → 400 if duplicate (error_code 1, reason "already exists").
- Store row with `hits=0`, `created_at=utcnow()` (no tz stored).
- Respond 200 + `{"alias": "..."}`.

### Redirect — GET `/redirect/{alias}`

- 404 if alias not in DB (error_code 3, reason "not found").
- 410 if `now() >= expiration` (error_code 2, reason "expired").
- 301 + `Location: <destination_url>`, atomically increment `hits` (error_code 0).
- No response body in any case.

### Hit count — GET `/routes/{alias}`

- 404 if alias not in DB (error_code 3, reason "not found").
- 200 + `{"alias": "...", "hits": N}` (error_code 0).

### Logging (all endpoints)

Structured JSON, always INFO level. Keys: `action`, `error_code` (always), `alias` (happy path only), `reason` (error path only).

| Case | action | error_code | alias | reason |
|------|--------|------------|-------|--------|
| Create – happy path | "create route" | 0 | slugified name | — |
| Create – invalid field | "create route" | 4 | — | varies |
| Create – duplicate | "create route" | 1 | — | "already exists" |
| Redirect – happy path | "redirect" | 0 | alias | — |
| Redirect – expired | "redirect" | 2 | — | "expired" |
| Redirect – not found | "redirect" | 3 | — | "not found" |
| Hit count – happy path | "hit count" | 0 | alias | — |
| Hit count – not found | "hit count" | 3 | — | "not found" |

---

## Tests

Each endpoint has its own test file. Covers:
- Happy path: status code, response body/headers, log output.
- Each error path: status code, response body, log output.

Use FastAPI's `TestClient`. DB isolation via a separate test database (env var `DATABASE_URL`); truncate tables between tests with a pytest fixture. No type hints in test files. No mocking the database.

---

## API Endpoints

| Method | Path | Handler file |
|--------|------|--------------|
| `POST` | `/routes/` | `routers/routes.py` |
| `GET` | `/redirect/{alias}` | `routers/redirect.py` |
| `GET` | `/routes/{alias}` | `routers/routes.py` |

All request/response bodies are JSON. Pydantic models for validation and serialization.

---

## Database

Table `url_route`:

| Column | Type | Notes |
|--------|------|-------|
| `id` | `SERIAL` | PK |
| `name` | `VARCHAR(100)` | NOT NULL |
| `alias` | `VARCHAR(100)` | NOT NULL, UNIQUE, indexed |
| `destination_url` | `TEXT` | NOT NULL |
| `expiration` | `TIMESTAMP` | NOT NULL, UTC, no timezone stored |
| `created_at` | `TIMESTAMP` | NOT NULL, UTC, default now() |
| `hits` | `INTEGER` | NOT NULL, default 0 |

`TIMESTAMP` (not `TIMESTAMPTZ`) — requirement: no timezone saved. Piccolo auto-migration manages the schema.

---

## Code & Directory Structure

```
steerer/
├── _vibe/
│   ├── initial-prompt-v2.md
│   ├── plan-v2.md
│   └── issue-{n}.md
├── src/
│   └── steerer/
│       ├── __init__.py
│       ├── main.py           # FastAPI app, router registration
│       ├── engine.py         # PostgresEngine instance
│       ├── piccolo_conf.py   # DB connection config (re-exports DB for migration CLI)
│       ├── piccolo_app.py    # Piccolo app registry
│       ├── tables.py         # url_route table definition
│       ├── schemas.py        # Pydantic request/response models
│       ├── services.py       # slugify and other pure business logic
│       ├── logging.py        # Structured log helpers
│       └── routers/
│           ├── __init__.py
│           ├── routes.py     # POST /routes/ + GET /routes/{alias}
│           └── redirect.py   # GET /redirect/{alias}
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

`routers/routes.py` handles both `POST /routes/` and `GET /routes/{alias}` — same resource prefix and table, fewer files to jump between.

---

## Makefile Targets

| Target | Action |
|--------|--------|
| `make install` | Create venv with uv, install deps, set pre-commit hook |
| `make test [OPT=...]` | Run pytest non-verbose; extra opts via `OPT` |
| `make typecheck` | Run mypy on `src/` only |
| `make lint` | Run ruff check on `src/` |
| `make format` | Run ruff format + import sort on `src/` in one step |
| `make migrations` | Create Piccolo auto-migration |
| `make migrate` | Apply pending migrations |
| `make migration-status` | Show current applied migration |

Pre-commit hook: `make lint && make typecheck`.

---

## User Stories — Vertical Slices

- [Issue 1](issue-1.md) — Project scaffolding and development environment
- [Issue 2](issue-2.md) — Create route endpoint (POST /routes/)
- [Issue 3](issue-3.md) — Redirect endpoint (GET /redirect/{alias})
- [Issue 4](issue-4.md) — Hit count endpoint (GET /routes/{alias})
