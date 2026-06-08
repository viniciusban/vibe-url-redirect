from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"datetime": datetime.now(timezone.utc).isoformat()}
