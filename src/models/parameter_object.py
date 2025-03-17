from typing import Any, Mapping, Optional

from msgspec import field

from src.models.base_struc import BaseStruct
from src.models.example_object import ExampleObject
from src.models.media_type_object import MediaTypeObject
from src.models.reference_object import ReferenceObject
from src.models.schema_object import SchemaObject


class ParameterObject(BaseStruct):
    """There are four possible parameter locations specified by the in field"""

    param_in: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allowEmptyValue: Optional[bool] = None
    style: Optional[str] = None
    explode: Optional[str] = None
    allowReserved: Optional[str] = None
    schema: Optional[SchemaObject] = None
    example: Optional[Any] = None
    examples: Optional[list[Mapping[str, ExampleObject | ReferenceObject]]] = field(
        default_factory=list
    )
    content: Optional[MediaTypeObject] = None
