from typing import Optional, Union

from msgspec import field

from src.models.base_struc import BaseStruct
from src.models.operation_object import OperationObject
from src.models.parameter_object import ParameterObject
from src.models.reference_object import ReferenceObject
from src.models.server_object import ServerObject


class PathItemObject(BaseStruct):
    """Describes the operations available on a single path.
    A Path Item MAY be empty due to ACL constraints.
    The path itself is still exposed to the documentation viewer,
    but users will not know which operations and parameters are available.
    """

    ref: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[OperationObject] = None
    put: Optional[OperationObject] = None
    post: Optional[OperationObject] = None
    delete: Optional[OperationObject] = None
    patch: Optional[OperationObject] = None
    options: Optional[OperationObject] = None
    head: Optional[OperationObject] = None
    trace: Optional[OperationObject] = None
    servers: list[ServerObject] = field(default_factory=list)
    parameters: list[Union[ParameterObject, ReferenceObject]] = field(
        default_factory=list
    )
