# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class TAARecord(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    TAARecord - a model defined in OpenAPI
        digest: The digest of this TAARecord [Optional].
        text: The text of this TAARecord [Optional].
        version: The version of this TAARecord [Optional].
    """

    digest: Optional[str] = None
    text: Optional[str] = None
    version: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


TAARecord.update_forward_refs()
