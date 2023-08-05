# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
import typing_extensions

from ..core.datetime_utils import serialize_datetime


class SegmentIdentify(pydantic.BaseModel):
    type: typing_extensions.Literal["identify"]
    user_id: str = pydantic.Field(
        alias="userId", description=('<span style="white-space: nowrap">`non-empty`</span>\n')
    )
    traits: typing.Dict[str, typing.Any]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
