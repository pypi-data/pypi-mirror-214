# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.indy_pres_attr_spec import IndyPresAttrSpec
from aries_cloudcontroller.model.indy_pres_pred_spec import IndyPresPredSpec


class IndyPresPreview(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    IndyPresPreview - a model defined in OpenAPI
        attributes: The attributes of this IndyPresPreview.
        predicates: The predicates of this IndyPresPreview.
        type: Message type identifier [Optional].
    """

    attributes: List[IndyPresAttrSpec]
    predicates: List[IndyPresPredSpec]
    type: Optional[str] = Field(None, alias="@type")

    class Config:
        allow_population_by_field_name = True


IndyPresPreview.update_forward_refs()
