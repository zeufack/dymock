from typing import Optional, Union, Dict, Any

from msgspec import field


from src.models.base_struc import BaseStruct

# from src.models.external_documentation_object import ExternalDocumentationObject
from src.models.reference_object import ReferenceObject
from src.models.schema_object import SchemaObject
# from src.models.media_type_object import MediaTypeObject


class HeaderObject(BaseStruct, kw_only=True):
    description: str | None = None
    required: bool = False
    deprecated: bool = False
    style: str | None = None
    explode: bool | None = None
    schema: Optional[Union["SchemaObject", "ReferenceObject"]] = None
    content: Optional[Dict[str, "MediaTypeObject"]] = None
    extensions: Optional[Dict[str, Any]] = field(default_factory=dict)
