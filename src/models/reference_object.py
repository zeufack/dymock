from typing import Optional

from msgspec import field

from src.models.base_struc import BaseStruct


class ReferenceObject(BaseStruct):
    """A simple object to allow referencing other components in the OpenAPI document, internally and externally."""

    ref: str = field(name="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None
