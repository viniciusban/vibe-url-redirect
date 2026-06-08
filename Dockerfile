FROM python:3.14-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml ./
RUN uv sync --no-dev

COPY src/ ./src/
COPY migrations/ ./migrations/

CMD ["uv", "run", "uvicorn", "steerer.main:app", "--host", "0.0.0.0", "--port", "8000"]
