# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class AttributeMimeTypesResult(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AttributeMimeTypesResult - a model defined in OpenAPI
        results: The results of this AttributeMimeTypesResult [Optional].
    """

    results: Optional[Dict[str, str]] = None

    class Config:
        allow_population_by_field_name = True


AttributeMimeTypesResult.update_forward_refs()
