from typing import Optional, Union, Mapping


from src.models.reference_object import ReferenceObject
from src.models.response_object import ResponseObject
from src.models.base_struc import BaseStruct


class ResponsesObject(BaseStruct):
    """
    A container for the expected responses of an operation. The container maps a HTTP response code to the expected response.
    """

    __extra__ = None
