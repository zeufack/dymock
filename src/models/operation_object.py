from __future__ import annotations

from typing import Mapping, Optional, Union

from msgspec import field

from src.models.base_struct import BaseStruct
from src.models.external_documentation_object import ExternalDocumentationObject
from src.models.parameter_object import ParameterObject
from src.models.reference_object import ReferenceObject
from src.models.request_body_object import RequestBodyObject
from src.models.response_object import ResponseObject
from src.models.security_object import SecurityRequirementObject
from src.models.server_object import ServerObject


class OperationObject(BaseStruct):
    """Describes a single API operation on a path."""

    tags: Optional[list[str]] = field(default_factory=list)
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentationObject] = None
    operationId: Optional[str] = None
    parameters: Optional[list[Union[ParameterObject, ReferenceObject]]] = field(
        default_factory=list
    )
    requestBody: Optional[Union[RequestBodyObject, ReferenceObject]] = None
    responses: Optional[Mapping[str, Union[ResponseObject, ReferenceObject]]] = None
    callbacks: Optional[
        Mapping[str, Mapping[str, Union[ReferenceObject, OperationObject]]]
    ] = field(default_factory=dict)
    deprecated: bool = False
    security: Optional[list[SecurityRequirementObject]] = field(default_factory=list)
    servers: Optional[list[ServerObject]] = field(default_factory=list)
