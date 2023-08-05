# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401


class MediationGrant(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    MediationGrant - a model defined in OpenAPI
        id: Message identifier [Optional].
        type: Message type [Optional].
        endpoint: endpoint on which messages destined for the recipient are received. [Optional].
        routing_keys: The routing_keys of this MediationGrant [Optional].
    """

    id: Optional[str] = Field(None, alias="@id")
    type: Optional[str] = Field(None, alias="@type")
    endpoint: Optional[str] = None
    routing_keys: Optional[List[str]] = None

    class Config:
        allow_population_by_field_name = True


MediationGrant.update_forward_refs()
