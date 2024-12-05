# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from ...credentials.types.aws_credential import AwsCredential
from ...credentials.types.aws_credential_id import AwsCredentialId

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class AwsSqsCredential_Aws(AwsCredential):
    type: typing.Literal["aws"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class AwsSqsCredential_AwsId(pydantic.BaseModel):
    type: typing.Literal["aws_id"]
    value: AwsCredentialId

    class Config:
        frozen = True
        smart_union = True


AwsSqsCredential = typing.Union[AwsSqsCredential_Aws, AwsSqsCredential_AwsId]
