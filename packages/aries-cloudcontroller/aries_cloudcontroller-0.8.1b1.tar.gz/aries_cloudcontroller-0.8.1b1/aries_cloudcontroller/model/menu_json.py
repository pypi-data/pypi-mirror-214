# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.menu_option import MenuOption


class MenuJson(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    MenuJson - a model defined in OpenAPI
        options: List of menu options.
        description: Introductory text for the menu [Optional].
        errormsg: Optional error message to display in menu header [Optional].
        title: Menu title [Optional].
    """

    options: List[MenuOption]
    description: Optional[str] = None
    errormsg: Optional[str] = None
    title: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


MenuJson.update_forward_refs()
