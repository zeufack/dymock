from typing import Mapping, Optional

from src.models.base_struct import BaseStruct


class DiscriminatorObject(BaseStruct):
    propertyName: str
    mapping: Optional[Mapping[str, str]]
