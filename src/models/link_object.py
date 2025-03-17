from typing import Any, Mapping, Optional

from msgspec import field

from src.models.base_struc import BaseStruct
from src.models.server_object import ServerObject


class LinkObject(BaseStruct):
    operationRef: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[list[Mapping[str, Any]]] = field(default_factory=list)
    requestBody: Optional[Any] = None
    description: Optional[str] = None
    server: Optional[ServerObject] = None
