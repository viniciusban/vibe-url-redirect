from datetime import datetime

from pydantic import BaseModel, field_validator


class CreateRouteRequest(BaseModel):
    name: str
    destination_url: str
    expiration: datetime

    @field_validator("expiration", mode="before")
    @classmethod
    def parse_expiration(cls, v: object) -> object:
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("invalid expiration")
        return v


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
