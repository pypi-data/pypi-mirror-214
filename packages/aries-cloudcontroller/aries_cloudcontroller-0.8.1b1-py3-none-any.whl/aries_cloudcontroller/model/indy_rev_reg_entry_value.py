# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class IndyRevRegEntryValue(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    IndyRevRegEntryValue - a model defined in OpenAPI
        accum: Accumulator value [Optional].
        prev_accum: Previous accumulator value [Optional].
        revoked: Revoked credential revocation identifiers [Optional].
    """

    accum: Optional[str] = None
    prev_accum: Optional[str] = Field(None, alias="prevAccum")
    revoked: Optional[List[int]] = None

    class Config:
        allow_population_by_field_name = True


IndyRevRegEntryValue.update_forward_refs()
