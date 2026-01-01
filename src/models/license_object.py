from typing import Optional

from src.models.base_struct import BaseStruct


class LicenseObject(BaseStruct):
    """License information for the exposed API."""

    name: str
    identifier: Optional[str] = None
    url: Optional[str] = None
