import msgspec
from typing import Optional

from src.models.oauth_flows_object import OAuthFlowsObject
from src.models.base_struc import BaseStruct


class SecuritySchemeObject(BaseStruct):
    """Defines a security scheme that can be used by the operations."""

    description: Optional[str] = None
    name: Optional[str] = None
    in_: Optional[str] = msgspec.field(name="in", default=None)
    scheme: Optional[str] = None
    bearerFormat: Optional[str] = None
    flows: Optional[OAuthFlowsObject] = None
    openIdConnectUrl: Optional[str] = None
