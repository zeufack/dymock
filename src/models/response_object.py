from typing import Dict, Optional, Union, Mapping

from src.models.base_struct import BaseStruct
from src.models.header_object import HeaderObject
from src.models.link_object import LinkObject
from src.models.media_type_object import MediaTypeObject
from src.models.reference_object import ReferenceObject


class ResponseObject(BaseStruct):
    """Describes a single response from an API Operation, including design-time,
    static links to operations based on the response.
    """

    description: str
    headers: Optional[Dict[str, Union[HeaderObject, ReferenceObject]]] = None
    content: Optional[Mapping[str, MediaTypeObject]] = None
    link: Optional[Mapping[str, LinkObject | ReferenceObject]] = None
