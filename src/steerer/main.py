from datetime import datetime

from fastapi import FastAPI

from steerer.routers.routes import router as routes_router

app = FastAPI()
app.include_router(routes_router)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"datetime": datetime.utcnow().isoformat()}
