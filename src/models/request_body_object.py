from typing import Optional, Mapping

from src.models.base_struct import BaseStruct
from src.models.media_type_object import MediaTypeObject


class RequestBodyObject(BaseStruct):
    """Describes a single request body."""

    description: Optional[str] = None
    content: Optional[Mapping[str, MediaTypeObject]] = None
    required: Optional[bool] = False
