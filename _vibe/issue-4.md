# Issue 4 — Hit count endpoint (GET /routes/{alias})

Implement the hit count query with structured logging.

## Scope

- **Handler** in `routers/routes.py` (alongside `POST /routes/`):
  - Look up `alias` → 404 if not found.
  - Respond 200 + `{"alias": "...", "hits": N}`.
- **Pydantic schema** in `schemas.py`: `HitCountResponse` with `alias` (str) and `hits` (int).
- **Structured logging**:
  - Happy path: `{"action": "hit count", "alias": "...", "error_code": 0}`.
  - Not found: `{"action": "hit count", "alias": "...", "error_code": 3, "reason": "not found"}`.

## Criteria of Done

- All tests pass.
- `make typecheck` and `make lint` exit 0.

## Tests (`tests/test_hit_count.py`)

1. **Happy path**: GET existing alias → 200, body `{"alias": "...", "hits": N}`, log `{"action": "hit count", "alias": "...", "error_code": 0}`.
2. **Not found**: GET non-existent alias → 404, log `{"action": "hit count", "alias": "...", "error_code": 3, "reason": "not found"}`.
