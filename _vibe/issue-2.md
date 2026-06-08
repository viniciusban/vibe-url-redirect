# Issue 2 — Create route endpoint (POST /routes/)

Implement route creation with slugification, uniqueness check, and structured logging.

## Scope

- **Piccolo table** `url_route` in `tables.py` (all columns per plan).
- **`make migrations && make migrate`** creates the table in the dev DB.
- **Pydantic schemas** in `schemas.py`:
  - `CreateRouteRequest`: `name` (str), `destination_url` (str), `expiration` (str, parsed as `YYYY-MM-DD HH:mm:ss`). Computed field `alias` (slugified name). All validated via field/model validators.
  - `CreateRouteResponse`: `alias` (str).
  - `DuplicateRouteError`: `error_code` (int), `reason` (str).
  - `InvalidFieldError`: `error_code` (int), `reason` (str).
- **Validation rules** (enforced in schema, not in the route handler):
  - `name`: strip whitespace; blank → ValueError("name is required"); empty alias after slugification → ValueError("Invalid name").
  - `destination_url`: strip whitespace; blank → ValueError("destination_url is required").
  - `expiration`: parse with `strptime("%Y-%m-%d %H:%M:%S")`; invalid → ValueError("invalid expiration").
  - `RequestValidationError` handler in `main.py` converts all validation failures to 400 + `InvalidFieldError` body.
- **Slugification** pure function in `services.py`: lowercase, replace non-alphanumeric chars with hyphens, collapse consecutive hyphens, strip edge hyphens.
- **Handler** in `routers/routes.py` (no validation logic):
  - Check `alias` uniqueness → 400 + `DuplicateRouteError` body if duplicate.
  - Insert row with `hits=0`, `created_at=utcnow()`.
  - Respond 200 + `{"alias": "..."}`.
- **Structured logging**: `log_action(action, error_code=0, reason=None, alias=None)`.
  - Happy path: `{"action": "create route", "error_code": 0, "alias": "<slugified-name>"}`.
  - Errors: `{"action": "create route", "error_code": N, "reason": "..."}` (no alias).

## Criteria of Done

- `make migrations && make migrate` creates `url_route` without error.
- All tests pass.
- `make typecheck` and `make lint` exit 0.

## Tests (`tests/test_create_route.py` and `tests/test_slugify.py`)

- **Happy path**: POST with valid fields → 200, body `{"alias": "<slugified-name>"}`, log with alias and error_code 0.
- **Duplicate alias**: second POST with equivalent name → 400, body `{"error_code": 1, "reason": "already exists"}`, log with error_code 1.
- **Missing/blank name**: → 400, body `{"error_code": 4, "reason": "name is required"}`.
- **Name with only special chars**: → 400, body `{"error_code": 4, "reason": "Invalid name"}`.
- **Missing/blank destination_url**: → 400, body `{"error_code": 5, "reason": "destination_url is required"}`.
- **Invalid expiration**: → 400, body `{"error_code": 4, "reason": "invalid expiration"}`.
- **Slugification unit tests** in `test_slugify.py`: spaces, uppercase, consecutive hyphens, special chars, edge-dash stripping, all-special → empty.
