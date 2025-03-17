from typing import Optional

import msgspec

from src.models.external_documentation_object import ExternalDocumentationObject


class TagObject(msgspec.Struct):
    """A list of tags used by the document with additional metadata.
    The order of the tags can be used to reflect on their order by the parsing tools.
    Not all tags that are used by the Operation Object must be declared.
    The tags that are not declared MAY be organized randomly or based on the tools’ logic.
    Each tag name in the list MUST be unique.
    """

    name: str
    description: Optional[str]
    externalDocs: Optional[ExternalDocumentationObject] = None
