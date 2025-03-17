from typing import Optional

from src.models.base_struc import BaseStruct


class ExternalDocumentObject(BaseStruct):
    """Additional external documentation."""

    description: Optional[str]
    url: str
