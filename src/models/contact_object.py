from typing import Optional

from src.models.base_struct import BaseStruct


class ContactObject(BaseStruct):
    """The contact information for the exposed API."""

    name: Optional[str] = None
    url: Optional[str] = None
    email: Optional[str] = None
