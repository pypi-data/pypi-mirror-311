# This file was auto-generated from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .source import Source


class ModelSyncField(pydantic_v1.BaseModel):
    new: typing.Optional[bool] = pydantic_v1.Field(default=None)
    """
    New is set to true if the target field should be created by Polytomic. This is not supported by all backends.
    """

    override_value: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Value to set in the target field; if provided, 'source' is ignored.
    """

    source: typing.Optional[Source] = None
    sync_mode: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Sync mode for the field; defaults to 'updateOrCreate'. If set to 'create', the field will not be synced if it already has a value. This is not supported by all backends.
    """

    target: str = pydantic_v1.Field()
    """
    Target field ID the source field value will be written to.
    """

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
