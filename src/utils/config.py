import re
from pathlib import Path

from src.models.open_api_object import OpenAPIObject
from src.utils.open_api_parser import OpenAPIParser


class Config:
    def __init__(
        self, spec_path: str, host: str = "127.0.0.1", port: int = 8000
    ) -> None:
        self.spec = self.get_spec(spec_path=spec_path)
        self.host = host
        self.port = port

    @staticmethod
    def identify_spec_type(spec_path: str | Path) -> str:
        return Path(spec_path).suffix.replace(".", "")

    @classmethod
    def get_spec(cls, spec_path: str | Path) -> OpenAPIObject:
        """Load and parse the OpenAPI specification from a file.

        Args:
            spec_path: Path to the OpenAPI specification file

        Returns:
            Parsed OpenAPIObject

        Raises:
            ValueError: If the file cannot be found, read, or parsed
            FileNotFoundError: If the spec file doesn't exist
            PermissionError: If the file cannot be read
        """
        spec_path = Path(spec_path)

        if not spec_path.exists():
            raise FileNotFoundError(
                f"OpenAPI specification file not found: {spec_path}"
            )

        if not spec_path.is_file():
            raise ValueError(f"Path is not a file: {spec_path}")

        try:
            format = cls.identify_spec_type(spec_path=spec_path)
            format = format.lower()

            with open(spec_path, "r", encoding="utf-8") as file:
                spec_str = file.read()

            if not spec_str.strip():
                raise ValueError(f"OpenAPI specification file is empty: {spec_path}")

            parser = OpenAPIParser()
            return parser.parse(data=spec_str, format=format)

        except (IOError, OSError) as e:
            raise PermissionError(
                f"Cannot read OpenAPI specification file: {spec_path}. {e}"
            ) from e
        except UnicodeDecodeError as e:
            raise ValueError(
                f"OpenAPI specification file encoding error: {spec_path}. File must be UTF-8 encoded."
            ) from e

    @classmethod
    def convert_openapi_path_to_fastapi(self, openapi_path: str) -> str:
        """
        Converts OpenAPI path parameters {param} into FastAPI-compatible {param}.
        Example: "/users/{userId}" -> "/users/{userId}"
        """
        return re.sub(r"\{(\w+)\}", r"{\1}", openapi_path)
