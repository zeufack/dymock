from typing import List, Mapping, Optional

from src.models.component_object import ComponentsObject
from src.models.external_document_object import ExternalDocumentObject
from src.models.info_object import InfoObject
from src.models.path_item_object import PathItemObject
from src.models.security_object import SecurityRequirementObject
from src.models.server_object import ServerObject
from src.models.tag_object import TagObject
from src.models.base_struc import BaseStruct


class OpenAPIObject(BaseStruct):
    """
    This is the root object of the OpenAPI document.
    """

    openapi: str
    info: InfoObject
    jsonSchemaDialect: Optional[str] = None
    servers: Optional[List[ServerObject]] = None
    paths: Optional[Mapping[str, PathItemObject]] = None
    webhooks: Optional[Mapping[str, str]] = None
    components: Optional[ComponentsObject] = None
    security: Optional[List[SecurityRequirementObject]] = None
    tags: Optional[List[TagObject]] = None
    externalDocs: Optional[ExternalDocumentObject] = None
