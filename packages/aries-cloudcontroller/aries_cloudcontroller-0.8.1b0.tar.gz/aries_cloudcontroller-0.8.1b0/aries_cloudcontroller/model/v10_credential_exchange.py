# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Union, Literal  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, Extra  # noqa: F401
from aries_cloudcontroller.model.credential_offer import CredentialOffer
from aries_cloudcontroller.model.credential_proposal import CredentialProposal
from aries_cloudcontroller.model.indy_cred_abstract import IndyCredAbstract
from aries_cloudcontroller.model.indy_cred_info import IndyCredInfo
from aries_cloudcontroller.model.indy_cred_request import IndyCredRequest
from aries_cloudcontroller.model.indy_credential import IndyCredential


class V10CredentialExchange(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    V10CredentialExchange - a model defined in OpenAPI
        auto_issue: Issuer choice to issue to request in this credential exchange [Optional].
        auto_offer: Holder choice to accept offer in this credential exchange [Optional].
        auto_remove: Issuer choice to remove this credential exchange record when complete [Optional].
        connection_id: Connection identifier [Optional].
        created_at: Time of record creation [Optional].
        credential: Credential as stored [Optional].
        credential_definition_id: Credential definition identifier [Optional].
        credential_exchange_id: Credential exchange identifier [Optional].
        credential_id: Credential identifier [Optional].
        credential_offer: (Indy) credential offer [Optional].
        credential_offer_dict: Credential offer message [Optional].
        credential_proposal_dict: Credential proposal message [Optional].
        credential_request: (Indy) credential request [Optional].
        credential_request_metadata: (Indy) credential request metadata [Optional].
        error_msg: Error message [Optional].
        initiator: Issue-credential exchange initiator: self or external [Optional].
        parent_thread_id: Parent thread identifier [Optional].
        raw_credential: Credential as received, prior to storage in holder wallet [Optional].
        revoc_reg_id: Revocation registry identifier [Optional].
        revocation_id: Credential identifier within revocation registry [Optional].
        role: Issue-credential exchange role: holder or issuer [Optional].
        schema_id: Schema identifier [Optional].
        state: Issue-credential exchange state [Optional].
        thread_id: Thread identifier [Optional].
        trace: Record trace information, based on agent configuration [Optional].
        updated_at: Time of last record update [Optional].
    """

    auto_issue: Optional[bool] = None
    auto_offer: Optional[bool] = None
    auto_remove: Optional[bool] = None
    connection_id: Optional[str] = None
    created_at: Optional[str] = None
    credential: Optional[IndyCredInfo] = None
    credential_definition_id: Optional[str] = None
    credential_exchange_id: Optional[str] = None
    credential_id: Optional[str] = None
    credential_offer: Optional[IndyCredAbstract] = None
    credential_offer_dict: Optional[CredentialOffer] = None
    credential_proposal_dict: Optional[CredentialProposal] = None
    credential_request: Optional[IndyCredRequest] = None
    credential_request_metadata: Optional[Dict[str, Any]] = None
    error_msg: Optional[str] = None
    initiator: Optional[Literal["self", "external"]] = None
    parent_thread_id: Optional[str] = None
    raw_credential: Optional[IndyCredential] = None
    revoc_reg_id: Optional[str] = None
    revocation_id: Optional[str] = None
    role: Optional[Literal["holder", "issuer"]] = None
    schema_id: Optional[str] = None
    state: Optional[str] = None
    thread_id: Optional[str] = None
    trace: Optional[bool] = None
    updated_at: Optional[str] = None

    @validator("created_at")
    def created_at_pattern(cls, value):
        # Property is optional
        if value is None:
            return

        pattern = r"^\d{4}-\d\d-\d\d[T ]\d\d:\d\d(?:\:(?:\d\d(?:\.\d{1,6})?))?(?:[+-]\d\d:?\d\d|Z|)$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Value of created_at does not match regex pattern ('{pattern}')"
            )
        return value

    @validator("credential_definition_id")
    def credential_definition_id_pattern(cls, value):
        # Property is optional
        if value is None:
            return

        pattern = r"^([123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{21,22}):3:CL:(([1-9][0-9]*)|([123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{21,22}:2:.+:[0-9.]+)):(.+)?$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Value of credential_definition_id does not match regex pattern ('{pattern}')"
            )
        return value

    @validator("schema_id")
    def schema_id_pattern(cls, value):
        # Property is optional
        if value is None:
            return

        pattern = r"^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{21,22}:2:.+:[0-9.]+$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Value of schema_id does not match regex pattern ('{pattern}')"
            )
        return value

    @validator("updated_at")
    def updated_at_pattern(cls, value):
        # Property is optional
        if value is None:
            return

        pattern = r"^\d{4}-\d\d-\d\d[T ]\d\d:\d\d(?:\:(?:\d\d(?:\.\d{1,6})?))?(?:[+-]\d\d:?\d\d|Z|)$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Value of updated_at does not match regex pattern ('{pattern}')"
            )
        return value

    class Config:
        allow_population_by_field_name = True


V10CredentialExchange.update_forward_refs()
