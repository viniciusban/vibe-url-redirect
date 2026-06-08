# Issue 2 — Create route endpoint (POST /routes/)

Implement route creation with slugification, uniqueness check, and structured logging.

## Scope

- **Piccolo table** `url_route` in `tables.py` (all columns per plan).
- **`make migrations && make migrate`** creates the table in the dev DB.
- **Pydantic schemas** in `schemas.py`:
  - `CreateRouteRequest`: `name` (str, max 100), `destination_url` (str), `expiration` (datetime, format `YYYY-MM-DD HH:mm:ss`).
  - `CreateRouteResponse`: `alias` (str).
  - `DuplicateRouteError`: `error_code` (int), `reason` (str), `alias` (str).
- **Slugification** pure function in a service module: lowercase, replace non-alphanumeric chars with hyphens, collapse consecutive hyphens.
- **Handler** in `routers/routes.py`:
  - Generate `alias` from `name`.
  - Check `alias` uniqueness → 400 + `DuplicateRouteError` body if duplicate.
  - Insert row with `hits=0`, `created_at=utcnow()`.
  - Respond 200 + `{"alias": "..."}`.
- **Structured logging**: `{"action": "create route", "alias": "...", "error_code": N}` + `"reason"` on error.

## Criteria of Done

- `make migrations && make migrate` creates `url_route` without error.
- All tests pass.
- `make typecheck` and `make lint` exit 0.

## Tests (`tests/test_create_route.py`)

1. **Happy path**: POST with valid `name`, `destination_url`, `expiration` → 200, body `{"alias": "<slugified-name>"}`, log `{"action": "create route", "alias": "...", "error_code": 0}`.
2. **Duplicate alias**: second POST with same (or equivalent) name → 400, body `{"error_code": 1, "reason": "already exists", "alias": "..."}`, log with `error_code: 1` and `reason`.
3. **Slugification unit tests** (no DB): spaces → hyphens, uppercase → lowercase, consecutive hyphens collapsed, special chars stripped.
