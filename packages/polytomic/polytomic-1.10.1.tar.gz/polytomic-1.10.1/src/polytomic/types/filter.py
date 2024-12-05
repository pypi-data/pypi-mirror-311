# This file was auto-generated from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .filter_field_reference_type import FilterFieldReferenceType
from .filter_function import FilterFunction
from .source import Source


class Filter(pydantic_v1.BaseModel):
    """
    Either `field` or `field_id` must be provided. If `field` is provided, `field_id` is ignored.
    """

    field: typing.Optional[Source] = None
    field_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Model or Target field name to filter on.
    """

    field_type: typing.Optional[FilterFieldReferenceType] = None
    function: FilterFunction
    label: typing.Optional[str] = None
    value: typing.Optional[typing.Any] = None

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
