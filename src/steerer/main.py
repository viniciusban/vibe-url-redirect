from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from steerer import logging as steerer_logging
from steerer.routers.routes import router as routes_router
from steerer.schemas import InvalidFieldError
from steerer.services import slugify

app = FastAPI()
app.include_router(routes_router)

_ACTION_BY_PATH = {"/routes/": "create route"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    field = str(errors[0]["loc"][-1]) if errors else "field"
    reason = f"invalid {field}"

    alias = ""
    try:
        body = await request.json()
        if isinstance(body, dict) and "name" in body:
            alias = slugify(str(body["name"]))
    except Exception:
        pass

    action = _ACTION_BY_PATH.get(request.url.path, "unknown")
    steerer_logging.log_action(action, alias, 4, reason)
    return JSONResponse(
        status_code=400,
        content=InvalidFieldError(
            error_code=4, reason=reason, alias=alias
        ).model_dump(),
    )


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"datetime": datetime.utcnow().isoformat()}
