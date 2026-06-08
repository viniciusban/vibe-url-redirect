from datetime import datetime

from pydantic import BaseModel, computed_field, field_validator, model_validator

from steerer.services import slugify


class CreateRouteRequest(BaseModel):
    name: str
    destination_url: str
    expiration: datetime

    @computed_field  # type: ignore[prop-decorator]
    @property
    def alias(self) -> str:
        return slugify(self.name)

    @model_validator(mode="after")
    def validate_alias(self) -> "CreateRouteRequest":
        if not self.alias:
            raise ValueError("Invalid name")
        return self

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name is required")
        return v

    @field_validator("destination_url", mode="before")
    @classmethod
    def strip_destination_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("destination_url is required")
        return v

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
