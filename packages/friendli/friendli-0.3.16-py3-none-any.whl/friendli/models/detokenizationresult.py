"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from friendli.types import BaseModel
from typing import Optional
from typing_extensions import NotRequired, TypedDict


class DetokenizationResultTypedDict(TypedDict):
    r"""Successfully detokenized the tokens."""

    text: NotRequired[str]
    r"""Detokenized text output."""


class DetokenizationResult(BaseModel):
    r"""Successfully detokenized the tokens."""

    text: Optional[str] = None
    r"""Detokenized text output."""
