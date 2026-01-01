from typing import Any, Mapping, Optional


from src.models.base_struct import BaseStruct


class MediaTypeObject(BaseStruct):
    example: Any = None
    schema: Optional[Mapping[str, "SchemaObject"]] = None
    examples: Optional[Mapping[str, "ReferenceObject | ExampleObject"]] = None
    encoding: Optional[Mapping[str, "EncodingObject"]] = None
