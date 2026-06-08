Goal: Create Steerer, a URL redirection service.

## Overview

Steerer is a URL redirection service with 3 main functionalities:
1. Create a route from an origin name to a destination URL, resulting in a slug
2. Redirect a request to a slug to the destination URL
3. Show the hit count for a slug


## Functional Requirements

### 1 - Create a route from an origin name to a destination URL, resulting in a slug

Given an origin name, a destination URL, and an expiration timestamp (in datetime format), create a row in the database table `route` with these 3 fields, along with origin name slugified (named origin_slug), creation timestamp, and number of hits. I want your opinion about the best name for this table. Alternatives are: route, dispatch, rolodex, forward, map. Other suggestions are also welcome. Show the best fit, explain why, and ask me for decision. Destination URLs can be large. Origin names' max length is 100 chars. URL for this endpoint is POST `https://steerer.com/routes/`.

Example for the happy path (origin_slug doesn't exist in database). Request: POST `https://steerer.com/routes/`, body `{"origin_name": "Featured Hotsite", "destination_url": "https://steerer.com/products/incredible-product?code=517&in_stock=true&warranty=false&warehouse=main-branch&images=always"}`. Response: status code 200, body `{"origin_slug": "featured-hotsite"}`. Log message INFO `{"action": "create route", "value": "featured-hotsite", "error_code": 0}`.

Example for when origin_slug already exists. Request: POST `https://steerer.com/routes/`, body `{"origin_name": "Duplicate Hotsite", "destination_url": "https://steerer.com/products/duplicate-product?code=892"}`. Response: status code 400, body `{"error_code": 1, "reason": "already exists", "value": "duplicate-hotsite"}`. Log message INFO `{"action": "create route", "value": "duplicate-hotsite", "error_code": 1, reason: "already exists"}`.


### 2 - Redirect a request to a slug to the destination URL

Given an origin slug, access it in the database and redirect the request to the destination URL. Status code 301 (moved permanently) when current time is before the expiration timestamp (happy path). When the route is expired, return status code 410 (gone). If origin slug doesn't exist, return status code 404 (not found). No responses for this functionality have a body. When in the happy path, increment the hit counter by 1.

Example for the happy path. Request: GET `https://steerer.com/redirect/featured-hotsite`. Response: status code 301 (moved permanently). Header Location with value from destination_url. Log message: INFO `{"action": "redirect", "value": "featured-hotsite", "error_code": 0}`.

Example for expired route. Request: GET `https://steerer.com/redirect/some-expired-slug`. Response: status code 410 (gone). Log message: INFO `{"action": "redirect", "value": "some-expired-slug", "error_code": 2, "reason": "expired"}`.

Example for inexistent route. Request: GET `https://steerer.com/redirect/invalid-slug`. Response: status code 404 (not found). Log message: INFO `{"action": "redirect", "value": "invalid-slug", "error_code": 3, "reason": "not found"}`.


### 3 - Show the hit count for a slug

Given an origin slug, access it in the database and return the number of hits along with the origin slug (happy path). If it doesn't exist, return status code 404 (not found), following the same pattern as for previous example for inexistent route. URL mask is GET `https://steerer.com/routes/{origin-slug}`.

Show log messages for both cases following previous patterns for happy path and error paths.


## Technical aspects

### Requests and responses

All bodies are in JSON format. All requests must show structured log messages.


### Programming Language & Tools

* Python 3.14 with type hints, except in tests.
* FastAPI and Pydantic.
* [Piccolo](https://piccolo-orm.readthedocs.io/en/latest/index.html) for database access and migrations ([auto migrations](https://piccolo-orm.readthedocs.io/en/latest/piccolo/migrations/create.html#auto-migrations)).
* Mypy to check type hints.
* ruff to lint and format Python code.
* Pytest.
* uv to manage virtualenv and dependencies.
* Postgres 18.
* Docker

### Code quality

Run lint and check type hints in precommit hook. Don't run mypy in test code. Format code and sort imports in one step.

### Commands to manage the project

* Use makefile.
* install project locally + set precommit hook
* run tests with pytest in non-verbose mode (accept parameter OPT to pass further options)
* check type hints
* lint source code with `ruff`
* sort imports + format source code with `ruff`
* create db migrations
* apply migration onto the db
* show current applied migration

### Code style

Use early return as much as possible. Prefer flat code over nested conditions. Prefer readibility over performance (when in doubt, ask). Put as less logic as possible in views. Move business logic to services.

### Development environment

Run using Docker Compose: Steerer service + database. Set dbname to "steerer_db" to run in development environment.


## Prompting and Claude Code Behaviour

Save all my prompts to @vibe/PROMPTS.md along with every commit. Add relevant instructions to CLAUDE.md. Add both to the repository. Don't change CLAUDE.md without my permission. Don't mix CLAUDE.md changes with other modifications in the same commit. Assert tests pass before you show suggestions/results to me.

Make a plan and show it in topics. An overview first, followed by details about business rules, tests, API endpoints, database, code structure. After that, propose user stories in vertical slices as issues on Github. Include the criteria of done. Save the whole plan to @vibe/PRD.md. Don't change anything else.
