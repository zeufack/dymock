from typing import Mapping, Optional

from src.models.base_struct import BaseStruct


class OAuthFlowsObject(BaseStruct):
    """Configuration details for a supported OAuth Flow"""

    authorizationUrl: str
    tokenUrl: str
    refreshUrl: Optional[str] = None
    scopes: Optional[Mapping[str, str]] = None
