# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from ...credentials.types.basic_credential import BasicCredential
from ...credentials.types.basic_credential_id import BasicCredentialId
from ...credentials.types.o_auth_client_credential import OAuthClientCredential
from ...credentials.types.o_auth_client_credential_id import OAuthClientCredentialId
from ...credentials.types.token_credential import TokenCredential
from ...credentials.types.token_credential_id import TokenCredentialId
from .elasticsearch_bridge_credentials import ElasticsearchBridgeCredentials

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class ElasticsearchCredential_Basic(BasicCredential):
    type: typing.Literal["basic"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ElasticsearchCredential_BasicId(pydantic.BaseModel):
    type: typing.Literal["basic_id"]
    value: BasicCredentialId

    class Config:
        frozen = True
        smart_union = True


class ElasticsearchCredential_Bridge(pydantic.BaseModel):
    type: typing.Literal["bridge"]
    value: ElasticsearchBridgeCredentials

    class Config:
        frozen = True
        smart_union = True


class ElasticsearchCredential_OAuthClient(OAuthClientCredential):
    type: typing.Literal["o_auth_client"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ElasticsearchCredential_OAuthClientId(pydantic.BaseModel):
    type: typing.Literal["o_auth_client_id"]
    value: OAuthClientCredentialId

    class Config:
        frozen = True
        smart_union = True


class ElasticsearchCredential_Token(TokenCredential):
    type: typing.Literal["token"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ElasticsearchCredential_TokenId(pydantic.BaseModel):
    type: typing.Literal["token_id"]
    value: TokenCredentialId

    class Config:
        frozen = True
        smart_union = True


ElasticsearchCredential = typing.Union[
    ElasticsearchCredential_Basic,
    ElasticsearchCredential_BasicId,
    ElasticsearchCredential_Bridge,
    ElasticsearchCredential_OAuthClient,
    ElasticsearchCredential_OAuthClientId,
    ElasticsearchCredential_Token,
    ElasticsearchCredential_TokenId,
]
