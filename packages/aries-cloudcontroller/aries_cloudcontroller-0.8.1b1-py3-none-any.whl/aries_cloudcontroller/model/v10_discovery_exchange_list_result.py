# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.v10_discovery_record import V10DiscoveryRecord


class V10DiscoveryExchangeListResult(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    V10DiscoveryExchangeListResult - a model defined in OpenAPI
        results: The results of this V10DiscoveryExchangeListResult [Optional].
    """

    results: Optional[List[V10DiscoveryRecord]] = None

    class Config:
        allow_population_by_field_name = True


V10DiscoveryExchangeListResult.update_forward_refs()
