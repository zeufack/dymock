from typing import Any, Mapping, Optional


from src.models.base_struc import BaseStruct
from src.models.encoding_object import EncodingObject
from src.models.example_object import ExampleObject
from src.models.reference_object import ReferenceObject
from src.models.schema_object import SchemaObject


class MediaTypeObject(BaseStruct):
    example: Any = None
    schema: Optional[Mapping[str, "SchemaObject"]] = None
    examples: Optional[Mapping[str, "ReferenceObject | ExampleObject"]] = None
    encoding: Optional[Mapping[str, "EncodingObject"]] = None
