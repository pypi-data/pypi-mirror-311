"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from friendli.types import BaseModel
from typing import Literal
from typing_extensions import TypedDict


OtherBuiltInToolType = Literal[
    "math:calculator",
    "math:statistics",
    "math:calendar",
    "web:search",
    "web:url",
    "code:python-interpreter",
]
r"""The type of the built-in tool."""


class OtherBuiltInToolTypedDict(TypedDict):
    type: OtherBuiltInToolType
    r"""The type of the built-in tool."""


class OtherBuiltInTool(BaseModel):
    type: OtherBuiltInToolType
    r"""The type of the built-in tool."""
