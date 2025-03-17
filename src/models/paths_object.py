from typing import Mapping

import msgspec

from src.models.path_item_object import PathItemObject


class PathsObject(msgspec.Struct, tag="paths_object"):
    """
    Represents OpenAPI paths as a dictionary where:
    - Keys are **path strings** (e.g., "/users/{userId}")
    - Values are **PathItemObject** instances defining available HTTP methods
    """

    __root__: Mapping[str, PathItemObject]  # Now paths are dynamically mapped

    def __post_init__(self):
        for path in self.__root__:
            if not path.startswith("/"):
                raise ValueError(f"Invalid path '{path}': Paths must start with '/'")
