# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class GetDIDEndpointResponse(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    GetDIDEndpointResponse - a model defined in OpenAPI
        endpoint: Full verification key [Optional].
    """

    endpoint: Optional[str] = None

    @validator("endpoint")
    def endpoint_pattern(cls, value):
        # Property is optional
        if value is None:
            return

        pattern = r"^[A-Za-z0-9\.\-\+]+:\/\/([A-Za-z0-9][.A-Za-z0-9-_]+[A-Za-z0-9])+(:[1-9][0-9]*)?(\/[^?&#]+)?$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Value of endpoint does not match regex pattern ('{pattern}')"
            )
        return value

    class Config:
        allow_population_by_field_name = True


GetDIDEndpointResponse.update_forward_refs()
