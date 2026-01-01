from typing import Optional

from src.models.base_struct import BaseStruct


class ServerVariableObject(BaseStruct):
    """An object representing a Server Variable for server URL template substitution."""

    enum: Optional[list[str]]
    default: str
    description: Optional[str]
