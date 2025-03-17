import re
from pathlib import Path
from typing import Any

from src.models.open_api_object import OpenAPIObject
from src.utils.open_api_parser import OpenAPIParser


class Config:
    def __init__(
        self, spec_path: str, host: str = "127.0.0.1", port: int = 8000
    ) -> Any:
        self.spec = self.get_spec(spec_path=spec_path)
        self.host = host
        self.port = port

    def identify_spec_type(spec_path: str | Path) -> str:
        return Path(spec_path).suffix.replace(".", "")

    @classmethod
    def get_spec(self, spec_path: str | Path) -> OpenAPIObject:
        """Load and parse the OpenAPI specification from a file.

        Args:
            spec_path (str | Path):

        Returns:
            OpenAPIObject:

        """
        parser = OpenAPIParser()
        if not Path(spec_path).is_file:
            raise f"Cannoct locate file {spec_path}"
        format = self.identify_spec_type(spec_path=spec_path)
        format = format.lower()
        with open(spec_path, "r") as file:
            spec_str = file.read()
        return parser.parse(data=spec_str, format=format)

    @classmethod
    def convert_openapi_path_to_fastapi(self, openapi_path: str) -> str:
        """
        Converts OpenAPI path parameters {param} into FastAPI-compatible {param}.
        Example: "/users/{userId}" -> "/users/{userId}"
        """
        return re.sub(r"\{(\w+)\}", r"{\1}", openapi_path)
