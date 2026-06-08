from pydantic import BaseModel


class CreateRouteRequest(BaseModel):
    name: str
    destination_url: str
    expiration: str


class CreateRouteResponse(BaseModel):
    alias: str


class DuplicateRouteError(BaseModel):
    error_code: int
    reason: str
    alias: str


class InvalidFieldError(BaseModel):
    error_code: int
    reason: str
    alias: str
