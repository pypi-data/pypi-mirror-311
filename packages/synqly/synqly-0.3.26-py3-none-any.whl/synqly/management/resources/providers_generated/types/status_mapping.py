# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ....core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class StatusMapping(pydantic.BaseModel):
    closed: typing.Optional[str] = pydantic.Field(default=None)
    """
    Custom value for the "Closed" status.
    """

    done: typing.Optional[str] = pydantic.Field(default=None)
    """
    Custom value for the "Done" status.
    """

    in_progress: typing.Optional[str] = pydantic.Field(default=None)
    """
    Custom value for the "In Progress" status.
    """

    on_hold: typing.Optional[str] = pydantic.Field(default=None)
    """
    Custom value for the "On Hold" status.
    """

    open: typing.Optional[str] = pydantic.Field(default=None)
    """
    Custom value for the "Open" status.
    """

    todo: typing.Optional[str] = pydantic.Field(default=None)
    """
    Custom value for the "To Do" status.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
