"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .serverlesstoolassistedchatstreambody import (
    ServerlessToolAssistedChatStreamBody,
    ServerlessToolAssistedChatStreamBodyTypedDict,
)
from friendli.types import BaseModel
from friendli.utils import FieldMetadata, HeaderMetadata, RequestMetadata
import pydantic
from typing import Optional
from typing_extensions import Annotated, NotRequired, TypedDict


class ServerlessToolAssistedChatStreamRequestTypedDict(TypedDict):
    serverless_tool_assisted_chat_stream_body: (
        ServerlessToolAssistedChatStreamBodyTypedDict
    )
    x_friendli_team: NotRequired[str]
    r"""ID of team to run requests as (optional parameter)."""


class ServerlessToolAssistedChatStreamRequest(BaseModel):
    serverless_tool_assisted_chat_stream_body: Annotated[
        ServerlessToolAssistedChatStreamBody,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]

    x_friendli_team: Annotated[
        Optional[str],
        pydantic.Field(alias="X-Friendli-Team"),
        FieldMetadata(header=HeaderMetadata(style="simple", explode=False)),
    ] = None
    r"""ID of team to run requests as (optional parameter)."""
