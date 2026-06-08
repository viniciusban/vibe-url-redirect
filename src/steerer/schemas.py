from datetime import datetime

from pydantic import BaseModel


class CreateRouteRequest(BaseModel):
    name: str
    destination_url: str
    expiration: datetime


class CreateRouteResponse(BaseModel):
    alias: str


class DuplicateRouteError(BaseModel):
    error_code: int
    reason: str
    alias: str
