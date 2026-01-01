from typing import Optional

from src.models.base_struct import BaseStruct


class ExternalDocumentObject(BaseStruct):
    """Additional external documentation."""

    description: Optional[str]
    url: str
