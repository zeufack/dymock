from typing import Mapping, Optional

from src.models.base_struct import BaseStruct


class EncodingObject(BaseStruct):
    """A single encoding definition applied to a single schema property."""

    contentType: Optional[str] = None
    headers: Optional[Mapping[str, "HeaderObject | ReferenceObject"]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
