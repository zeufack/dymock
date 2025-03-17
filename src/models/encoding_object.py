from typing import Mapping, Optional

from src.models.base_struc import BaseStruct
from src.models.header_object import HeaderObject
from src.models.reference_object import ReferenceObject


class EncodingObject(BaseStruct):
    """A single encoding definition applied to a single schema property."""

    contentType: Optional[str] = None
    headers: Optional[Mapping[str, "HeaderObject | ReferenceObject"]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
