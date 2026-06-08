Goal: Create Steerer, a URL redirection service.

## Overview

Steerer is a URL redirection service with 3 main functionalities:
1. Create a route from a name to a destination URL, resulting in an alias
2. Redirect a request to an alias to the destination URL
3. Show the hit count for a route


## Functional Requirements

### 1 - Create a route from a name to a destination URL, resulting in an alias

Given a name, a destination URL, and an expiration timestamp (format "YYYY-MM-DD HH:mm:ss"), create a row in the database table `url_route` with these 3 fields, along with the alias (slugified name), creation timestamp, and number of hits. Destination URLs can be large. Name's max length is 100 chars. URL for this endpoint is POST `https://steerer.com/routes/`.

Example for the happy path (alias doesn't exist in database). Request: POST `https://steerer.com/routes/`, body `{"name": "Featured Hotsite", "destination_url": "https://example.com/products/incredible-product?code=517&in_stock=true&warranty=false&warehouse=main-branch&images=always"}`. Response: status code 200, body `{"alias": "featured-hotsite"}`. Log message INFO `{"action": "create route", "alias": "featured-hotsite", "error_code": 0}`.

Example for when alias already exists. Request: POST `https://steerer.com/routes/`, body `{"name": "Duplicate Hotsite", "destination_url": "https://example.com/products/duplicate-product?code=892"}`. Response: status code 400, body `{"error_code": 1, "reason": "already exists", "alias": "duplicate-hotsite"}`. Log message INFO `{"action": "create route", "alias": "duplicate-hotsite", "error_code": 1, reason: "already exists"}`.


### 2 - Redirect a request to an alias to the destination URL

Given an alias, access its route and redirect the request to the destination URL. Status code 301 (moved permanently) when current time is before the expiration timestamp (happy path). When the route is expired, return status code 410 (gone). If alias doesn't exist, return status code 404 (not found). No responses for this functionality have a body. When in the happy path, increment the hit counter by 1.

Example for the happy path. Request: GET `https://steerer.com/redirect/featured-hotsite`. Response: status code 301 (moved permanently). Header Location with value from destination_url. Log message: INFO `{"action": "redirect", "alias": "featured-hotsite", "error_code": 0}`.

Example for expired route. Request: GET `https://steerer.com/redirect/some-expired-alias`. Response: status code 410 (gone). Log message: INFO `{"action": "redirect", "alias": "some-expired-alias", "error_code": 2, "reason": "expired"}`.

Example for inexistent route. Request: GET `https://steerer.com/redirect/invalid-alias`. Response: status code 404 (not found). Log message: INFO `{"action": "redirect", "alias": "invalid-alias", "error_code": 3, "reason": "not found"}`.


### 3 - Show the hit count for a route

Given an alias, access it in the database and return the number of hits along with the alias itself (happy path). If not found, return status code 404 (not found), following the same pattern as for previous example for inexistent route. URL mask is GET `https://steerer.com/routes/{alias}`.

Show log messages for both cases following previous patterns for happy path and error paths.


## Technical aspects

Timestamps: Don't expect time zone in user requests. All time zones are UTC. Don't save time zone to the database.

Requests and responses: all bodies are in JSON format. All requests must show structured log messages.


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

### Development environment

Run using Docker Compose: Steerer service + database. Set dbname to "steerer_db" to run in development environment.


## Planning

Make a plan and divide it in topics. An overview first, then details about business rules, tests, API endpoints, database, code and directory structure. After that, list user stories in vertical slices. Include the criteria of done in all of them and tests to accomplish it. Save each user story directly to their own file _vibe/issue-{number}.md. Feel free to iterate over these instructions as necessary and improve anything. When that's the case, highlight it and explain why. Don't show the plan, save it directly to @_vibe/plan-v2.md and tell me when it's done. Don't change anything else.
