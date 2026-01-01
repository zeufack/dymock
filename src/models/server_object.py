from typing import Mapping, Optional

from src.models.base_struct import BaseStruct
from src.models.server_variable_object import ServerVariableObject


class ServerObject(BaseStruct):
    """An object representing a Server."""

    url: str
    description: Optional[str] = None
    variables: Optional[Mapping[str, ServerVariableObject]] = None
