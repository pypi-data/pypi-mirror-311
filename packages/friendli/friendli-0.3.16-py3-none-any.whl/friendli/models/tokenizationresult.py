"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from friendli.types import BaseModel
from typing import List, Optional
from typing_extensions import NotRequired, TypedDict


class TokenizationResultTypedDict(TypedDict):
    r"""Successfully tokenized the text."""

    tokens: NotRequired[List[int]]
    r"""A list of token IDs."""


class TokenizationResult(BaseModel):
    r"""Successfully tokenized the text."""

    tokens: Optional[List[int]] = None
    r"""A list of token IDs."""
