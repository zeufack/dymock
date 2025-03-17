from typing import Optional

from src.models.base_struc import BaseStruct
from src.models.path_item_object import PathItemObject
from src.models.reference_object import ReferenceObject


class CalbackObject(BaseStruct):
    """A map of possible out-of band callbacks related to the parent operation."""

    path: str
    content: Optional[PathItemObject | ReferenceObject]
