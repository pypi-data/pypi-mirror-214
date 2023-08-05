# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.menu import Menu


class ActionMenuFetchResult(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ActionMenuFetchResult - a model defined in OpenAPI
        result: Action menu [Optional].
    """

    result: Optional[Menu] = None

    class Config:
        allow_population_by_field_name = True


ActionMenuFetchResult.update_forward_refs()
