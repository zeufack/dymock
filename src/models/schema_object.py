from typing import Optional, Any, Dict, List

from src.models.base_struc import BaseStruct
from src.models.discriminator_object import DiscriminatorObject
from src.models.external_documentation_object import ExternalDocumentationObject


class SchemaObject(BaseStruct):
    """_summary_"""

    type: Optional[str] = None
    properties: Optional[Dict[str, "SchemaObject"]] = None
    items: Optional["SchemaObject"] = None
    required: Optional[List[str]] = None

    description: Optional[str] = None
    enum: Optional[List[Any]] = None
    allOf: Optional[List["SchemaObject"]] = None
    anyOf: Optional[List["SchemaObject"]] = None
    oneOf: Optional[List["SchemaObject"]] = None
    additionalProperties: Optional[bool] = None
    default: Optional[Any] = None
    pattern: Optional[str] = None
    maxLength: Optional[int] = None
    minLength: Optional[int] = None
    format: Optional[str] = None
