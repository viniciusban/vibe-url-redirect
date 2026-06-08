import os

from piccolo.engine.postgres import PostgresEngine

DB = PostgresEngine(
    config={
        "host": os.environ.get("DB_HOST", "localhost"),
        "database": os.environ.get("DB_NAME", "steerer_db"),
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", "postgres"),
        "port": int(os.environ.get("DB_PORT", "5432")),
    }
)
