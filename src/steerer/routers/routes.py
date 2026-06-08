from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from steerer import logging as steerer_logging
from steerer.schemas import CreateRouteRequest, CreateRouteResponse, DuplicateRouteError
from steerer.tables import UrlRoute

router = APIRouter(prefix="/routes")


@router.post("/")
async def create_route(request: CreateRouteRequest) -> JSONResponse:
    count = await UrlRoute.count().where(UrlRoute.alias == request.alias).run()
    if count:
        steerer_logging.log_action("create route", request.alias, 1, "already exists")
        return JSONResponse(
            status_code=400,
            content=DuplicateRouteError(
                error_code=1, reason="already exists", alias=request.alias
            ).model_dump(),
        )

    await UrlRoute(
        name=request.name,
        alias=request.alias,
        destination_url=request.destination_url,
        expiration=request.expiration,
        created_at=datetime.utcnow(),
        hits=0,
    ).save().run()

    steerer_logging.log_action("create route", request.alias, 0)
    return JSONResponse(content=CreateRouteResponse(alias=request.alias).model_dump())
