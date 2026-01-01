from typing import Any, Dict, Union

import msgspec

from src.models.open_api_object import OpenAPIObject
from src.utils.decoder import CustomDecoder


class OpenAPIParser:
    """Parser for OpenAPI Specification with improved interface."""

    def __init__(self):
        self.decoder = CustomDecoder()
        self.encoder = msgspec.json.Encoder()
        self.json_decoder = msgspec.json.Decoder()

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

            # Validate basic OpenAPI structure
            self._validate_openapi_structure(data)

            return self.decoder.decode_openapi(data)
        except Exception as e:
            raise ValueError(f"Failed to parse OpenAPI specification: {str(e)}") from e

    def _validate_openapi_structure(self, data: Dict) -> None:
        """Validate basic OpenAPI specification structure."""
        if "openapi" not in data:
            raise ValueError("Missing required 'openapi' field")

        if "info" not in data:
            raise ValueError("Missing required 'info' field")

        if "info" in data:
            info = data["info"]
            if not isinstance(info, dict):
                raise ValueError("'info' must be an object")
            if "title" not in info:
                raise ValueError("Missing required 'info.title' field")
            if "version" not in info:
                raise ValueError("Missing required 'info.version' field")

        if "paths" not in data:
            raise ValueError("Missing required 'paths' field")

        if "paths" in data and not isinstance(data["paths"], dict):
            raise ValueError("'paths' must be an object")

        # Validate OpenAPI version format (basic check)
        openapi_version = data.get("openapi", "")
        if not isinstance(openapi_version, str) or not openapi_version.startswith("3."):
            raise ValueError(
                f"Unsupported OpenAPI version: {openapi_version}. Only 3.x versions are supported."
            )

    def to_dict(self, spec: OpenAPIObject) -> Dict:
        """Convert OpenAPI specification to dictionary with validation."""
        if not isinstance(spec, OpenAPIObject):
            raise TypeError(f"Expected OpenAPIObject, got {type(spec).__name__}")
        return spec.to_dict()

    def _decode(self, data: Union[str, bytes], format: str) -> Any:
        if format == "json":
            return self.json_decoder.decode(data)
        elif format == "yaml":
            if not hasattr(msgspec, "yaml"):
                raise ValueError("YAML support is not available in msgspec.")
            ydata = msgspec.yaml.decode(data)
            jdata = msgspec.json.encode(ydata)
            return msgspec.json.decode(jdata)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'yaml'.")
