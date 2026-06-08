# Issue 3 — Redirect endpoint (GET /redirect/{alias})

Implement the redirect handler with expiry check, atomic hit increment, and structured logging.

## Scope

- **Handler** in `routers/redirect.py`:
  - Look up `alias` → 404 (no body) if not found.
  - Check `expiration`: 410 (no body) if `now() >= expiration`.
  - Atomically increment `hits` via Piccolo atomic update.
  - Respond 301 + `Location: <destination_url>` header (no body).
- **Structured logging** for all three cases:
  - Happy path: `{"action": "redirect", "alias": "...", "error_code": 0}`.
  - Expired: `{"action": "redirect", "alias": "...", "error_code": 2, "reason": "expired"}`.
  - Not found: `{"action": "redirect", "alias": "...", "error_code": 3, "reason": "not found"}`.

## Criteria of Done

- All tests pass.
- `make typecheck` and `make lint` exit 0.

## Tests (`tests/test_redirect.py`)

1. **Happy path**: GET existing, non-expired alias → 301, `Location` header equals `destination_url`, log `error_code: 0`, `hits` incremented by 1 in DB.
2. **Expired route**: GET alias where `expiration` is in the past → 410, no body, log `{"action": "redirect", "alias": "...", "error_code": 2, "reason": "expired"}`.
3. **Not found**: GET non-existent alias → 404, no body, log `{"action": "redirect", "alias": "...", "error_code": 3, "reason": "not found"}`.
