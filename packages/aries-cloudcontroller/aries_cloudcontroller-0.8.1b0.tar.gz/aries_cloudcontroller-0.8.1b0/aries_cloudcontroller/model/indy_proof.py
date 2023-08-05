# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.indy_proof_identifier import IndyProofIdentifier
from aries_cloudcontroller.model.indy_proof_proof import IndyProofProof
from aries_cloudcontroller.model.indy_proof_requested_proof import (
    IndyProofRequestedProof,
)


class IndyProof(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    IndyProof - a model defined in OpenAPI
        identifiers: Indy proof.identifiers content [Optional].
        proof: Indy proof.proof content [Optional].
        requested_proof: Indy proof.requested_proof content [Optional].
    """

    identifiers: Optional[List[IndyProofIdentifier]] = None
    proof: Optional[IndyProofProof] = None
    requested_proof: Optional[IndyProofRequestedProof] = None

    class Config:
        allow_population_by_field_name = True


IndyProof.update_forward_refs()
