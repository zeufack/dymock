

from src.models.base_struct import BaseStruct


class ResponsesObject(BaseStruct):
    """
    A container for the expected responses of an operation. The container maps a HTTP response code to the expected response.
    """

    __extra__ = None
