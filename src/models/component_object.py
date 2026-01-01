from typing import Mapping, Optional

from src.models.callback_object import CallbackObject
from src.models.example_object import ExampleObject
from src.models.header_object import HeaderObject
from src.models.link_object import LinkObject
from src.models.parameter_object import ParameterObject
from src.models.path_item_object import PathItemObject
from src.models.reference_object import ReferenceObject
from src.models.request_body_object import RequestBodyObject
from src.models.response_object import ResponseObject
from src.models.schema_object import SchemaObject
from src.models.security_scheme_object import SecuritySchemeObject
from src.models.base_struct import BaseStruct


class ComponentsObject(BaseStruct):
    """
    Holds a set of reusable objects for different aspects of the OAS.
    All objects defined within the components object will have no effect on the API unless they are explicitly referenced from properties outside the components object.
    """

    schemas: Optional[Mapping[str, SchemaObject]] = None
    responses: Optional[Mapping[str, ResponseObject | ReferenceObject]] = None
    parameters: Optional[Mapping[str, ParameterObject | ReferenceObject]] = None
    examples: Optional[Mapping[str, ExampleObject | ReferenceObject]] = None
    requestBodies: Optional[Mapping[str, RequestBodyObject | ReferenceObject]] = None
    headers: Optional[Mapping[str, HeaderObject | ReferenceObject]] = None
    securitySchemes: Optional[Mapping[str, SecuritySchemeObject | ReferenceObject]] = (
        None
    )
    links: Optional[Mapping[str, LinkObject]] = None
    callbacks: Optional[Mapping[str, CallbackObject | ReferenceObject]] = None
    pathItems: Optional[Mapping[str, PathItemObject | ReferenceObject]] = None
