PICCOLO_CONF := steerer.piccolo_conf

.PHONY: install test typecheck lint format check migrations migrate migration-status

install:
	uv sync
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	uv run pytest -q $(OPT); status=$$?; [ $$status -eq 5 ] && exit 0 || exit $$status

typecheck:
	uv run mypy src/

lint:
	uv run ruff check src/

check: lint typecheck test

format:
	uv run ruff check --select I --fix src/ && uv run ruff format src/

migrations:
	PICCOLO_CONF=$(PICCOLO_CONF) uv run piccolo migrations new steerer --auto

migrate:
	PICCOLO_CONF=$(PICCOLO_CONF) uv run piccolo migrations forward steerer

migration-status:
	PICCOLO_CONF=$(PICCOLO_CONF) uv run piccolo migrations check steerer
