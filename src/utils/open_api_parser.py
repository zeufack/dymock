from typing import Any, Dict, Union

import msgspec

from src.models.open_api_object import OpenAPIObject
from src.utils.docoder import CustomDecoder


class OpenAPIParser:
    """Parser for OpenAPI Specification with improved interface."""

    def __init__(self):
        self.decoder = CustomDecoder()
        self.encoder = msgspec.json.Encoder()
        self.json_encoder = msgspec.json.Decoder()

    def parse(
        self, data: Union[str, bytes, Dict], format: str = "json"
    ) -> OpenAPIObject:
        """Parse OpenAPI specification with proper type handling."""
        try:
            if isinstance(data, (str, bytes)):
                data = self._decode(data=data, format=format)
            if not isinstance(data, dict):
                raise TypeError(
                    f"Expected dict after decoding, got {type(data).__name__}"
                )
            return self.decoder.decode_openapi(data)
        except Exception as e:
            raise ValueError(f"Failed to parse OpenAPI specification: {str(e)}") from e

    def to_dict(self, spec: OpenAPIObject) -> Dict:
        """Convert OpenAPI specification to dictionary with validation."""
        if not isinstance(spec, OpenAPIObject):
            raise TypeError(f"Expected OpenAPIObject, got {type(spec).__name__}")
        return spec.to_dict()

    def _decode(self, data, format: str) -> Any:
        if format == "json":
            return self.json_encoder.decode(data)
        elif format == "yaml":
            print("test")
            if not hasattr(msgspec, "yaml"):
                raise ValueError("YAML support is not available in msgspec.")
            ydata = msgspec.yaml.decode(data)
            jdata = msgspec.json.encode(ydata)
            return msgspec.json.decode(jdata)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'yaml'.")
