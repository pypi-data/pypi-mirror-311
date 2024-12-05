# This file was auto-generated from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .bulk_execution_status import BulkExecutionStatus
from .bulk_sync_schema_execution import BulkSyncSchemaExecution


class BulkSyncExecution(pydantic_v1.BaseModel):
    completed_at: typing.Optional[dt.datetime] = None
    created_at: typing.Optional[dt.datetime] = None
    id: typing.Optional[str] = None
    is_resync: typing.Optional[bool] = None
    is_test: typing.Optional[bool] = None
    schemas: typing.Optional[typing.List[BulkSyncSchemaExecution]] = None
    started_at: typing.Optional[dt.datetime] = None
    status: typing.Optional[BulkExecutionStatus] = None
    type: typing.Optional[str] = None

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
