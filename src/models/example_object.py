from typing import Optional, Any

from src.models.base_struct import BaseStruct


class ExampleObject(BaseStruct):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Any] = None
    externalValue: Optional[str] = None
