import msgspec


class BaseStruct(msgspec.Struct):
    """Base class for all OpenAPI objects with common utilities"""

    def to_dict(self) -> dict:
        return msgspec.structs.asdict(self)
