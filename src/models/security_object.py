from typing import Optional

from src.models.base_struct import BaseStruct


class SecurityRequirementObject(BaseStruct):
    """A declaration of which security mechanisms can be used across the API.
    The list of values includes alternative security requirement objects that can be used.
    Only one of the security requirement objects need to be satisfied to authorize a request.
    Individual operations can override this definition.
    To make security optional, an empty security requirement ({}) can be included in the array.
    """

    names: Optional[list[str]] = None
