## Project

Steerer is a URL redirection service written in Python, made with FastAPI and backed by PostgreSQL.

Three endpoints:
1. Create a named alias for a URL: given a name, a destination URL, and an expiration timestamp, create an alias (slugified name).
1. Redirect an alias to its destination URL: given an alias, redirect the request to the destination URL.
1. Report hit counts: given an alias, return the number of hits.


See `_vibe/initial-prompt-v2.md` and `_vibe/plan-v2.md` for full business rules, and `_vibe/issue-{n}.md` for work items.

All commits have their respective prompts saved.


## Important commands

```bash
make install          # create venv (uv), install deps, wire pre-commit hook
make check            # lint + typecheck + test in one shot
make test             # pytest (non-verbose)
```

Docker dev environment (source auto-reloads on save):
```bash
docker compose up
```

## Note

This project is developed using Extreme Programming principles in pair programming with Claude Code, a.k.a. Agile Vibe Coding.