# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.transaction_record import TransactionRecord


class TxnOrRegisterLedgerNymResponse(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    TxnOrRegisterLedgerNymResponse - a model defined in OpenAPI
        success: Success of nym registration operation [Optional].
        txn: DID transaction to endorse [Optional].
    """

    success: Optional[bool] = None
    txn: Optional[TransactionRecord] = None

    class Config:
        allow_population_by_field_name = True


TxnOrRegisterLedgerNymResponse.update_forward_refs()
