from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.models.open_api_object import OpenAPIObject
from src.utils.config import Config
from src.utils.mock_data_generator import MockDataGenerator


class MockServer:
    def __init__(self, spec_path: str):
        self._spec_path = spec_path
        try:
            self._mock_spec: Optional[OpenAPIObject] = Config.get_spec(self._spec_path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            raise ValueError(f"Failed to load OpenAPI specification: {e}") from e

        self._app = FastAPI(lifespan=self._lifespan)
        self._data_generator = MockDataGenerator()

    def create_app(self) -> FastAPI:
        """Returns the FastAPI application instance."""
        return self._app

    def _create_handler(self, method: str, path: str, operation):
        # Methods that may have request bodies
        body_methods = {"post", "put", "patch"}

        if method.lower() in body_methods:

            async def handler(request: Request):
                # Validate request body against operation's requestBody schema
                await self._validate_request_body(request, operation)

                # Generate appropriate response based on status codes
                status_code, mock_data = self._generate_mock_response(method, operation)

                return JSONResponse(content=mock_data, status_code=status_code)
        else:

            async def handler():
                # Generate appropriate response based on status codes
                status_code, mock_data = self._generate_mock_response(method, operation)

                return JSONResponse(content=mock_data, status_code=status_code)

        return handler

    def _generate_mock_response(self, method: str, operation) -> tuple[int, Any]:
        """Generate mock response data based on operation's response schemas."""
        # Determine which response to use based on method and available responses
        status_code, response_obj = self._select_response(method, operation)

        if not response_obj:
            # Fallback to basic mock response
            return 200, {
                "mock": True,
                "description": operation.summary or "No description provided",
            }

        # Try to get JSON content
        if hasattr(response_obj, "content") and response_obj.content:
            json_media = response_obj.content.get("application/json")
            if json_media and hasattr(json_media, "schema") and json_media.schema:
                # Generate data from schema
                mock_data = self._data_generator.generate_from_schema(json_media.schema)
                return status_code, mock_data

        # Fallback if no schema available
        return status_code, {
            "mock": True,
            "description": operation.summary or "No description provided",
            "message": f"Mock response for {operation.operationId or 'operation'}",
        }

    def _select_response(self, method: str, operation) -> tuple[int, Any]:
        """Select appropriate response based on operation method and available responses."""
        if not operation.responses:
            return 200, None

        # Method-specific response selection
        method = method.lower()

        # For POST, prefer 201 Created
        if method == "post":
            response_obj = operation.responses.get("201") or operation.responses.get(
                "200"
            )
            status_code = 201 if operation.responses.get("201") else 200
        # For PUT/PATCH, prefer 200 OK
        elif method in ["put", "patch"]:
            response_obj = operation.responses.get("200") or operation.responses.get(
                "204"
            )
            status_code = 200 if operation.responses.get("200") else 204
        # For DELETE, prefer 204 No Content or 200 OK
        elif method == "delete":
            response_obj = operation.responses.get("204") or operation.responses.get(
                "200"
            )
            status_code = 204 if operation.responses.get("204") else 200
        else:
            # For GET/HEAD/OPTIONS, prefer 200 OK
            response_obj = operation.responses.get("200")
            status_code = 200

        if response_obj:
            return status_code, response_obj

        # Fallback: use first available response
        for status_str, resp in operation.responses.items():
            if resp:
                return int(status_str), resp

        return 200, None

    def _register_routes(self, spec: OpenAPIObject):
        """Dynamically registers routes based on OpenAPI specification."""
        if not spec or not spec.paths:
            raise ValueError("OpenAPI specification must contain paths")

        # HTTP methods that should be registered
        http_methods = {
            "get",
            "post",
            "put",
            "delete",
            "patch",
            "options",
            "head",
            "trace",
        }
        registered_routes = 0

        for path, path_item in spec.paths.items():
            if not path.startswith("/"):
                # Warn about invalid paths but continue
                print(f"Warning: Path '{path}' does not start with '/'. Skipping.")
                continue

            fast_api_path = Config.convert_openapi_path_to_fastapi(openapi_path=path)

            for method in http_methods:
                operation = getattr(path_item, method, None)
                if not operation:
                    continue

                # Validate operation has required fields
                if not hasattr(operation, "responses") or not operation.responses:
                    print(
                        f"Warning: Operation {method.upper()} {path} has no responses defined. Skipping."
                    )
                    continue

                operation_id = operation.operationId or f"{method}_{path}".replace(
                    "/", "_"
                )

                try:
                    handler = self._create_handler(method, path, operation)
                    self._app.add_api_route(
                        fast_api_path,
                        handler,
                        methods=[method.upper()],
                        name=operation_id,
                    )
                    registered_routes += 1
                except Exception as e:
                    print(
                        f"Warning: Failed to register route {method.upper()} {path}: {e}"
                    )
                    continue

        if registered_routes == 0:
            raise ValueError(
                "No valid routes could be registered from the OpenAPI specification"
            )

        print(f"Successfully registered {registered_routes} routes")

    async def _validate_request_body(self, request: Request, operation):
        """Validate request body against operation's requestBody schema."""
        if not hasattr(operation, "requestBody") or not operation.requestBody:
            return

        # Handle ReferenceObject case
        from src.models.reference_object import ReferenceObject

        if isinstance(operation.requestBody, ReferenceObject):
            # For now, skip validation of referenced request bodies
            return

        request_body = operation.requestBody

        # Check if request body is required
        if getattr(request_body, "required", False):
            try:
                body_data = await request.json()
                if not body_data:
                    raise HTTPException(
                        status_code=400, detail="Request body is required but empty"
                    )
            except Exception:
                raise HTTPException(
                    status_code=400,
                    detail="Request body is required but not provided or invalid JSON",
                )

        # Try to validate against schema if available
        if hasattr(request_body, "content") and request_body.content:
            json_media = request_body.content.get("application/json")
            if json_media and hasattr(json_media, "schema") and json_media.schema:
                try:
                    body_data = await request.json()
                    self._validate_data_against_schema(body_data, json_media.schema)
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Request body validation failed: {str(e)}",
                    )

    def _validate_data_against_schema(self, data: Any, schema) -> None:
        """Basic validation of data against schema."""
        from src.models.reference_object import ReferenceObject

        # Handle ReferenceObject
        if isinstance(schema, ReferenceObject):
            # Skip validation for referenced schemas for now
            return

        # Basic type validation
        if hasattr(schema, "type") and schema.type:
            expected_type = schema.type
            if expected_type == "object" and not isinstance(data, dict):
                raise ValueError(f"Expected object, got {type(data).__name__}")
            elif expected_type == "array" and not isinstance(data, list):
                raise ValueError(f"Expected array, got {type(data).__name__}")
            elif expected_type == "string" and not isinstance(data, str):
                raise ValueError(f"Expected string, got {type(data).__name__}")
            elif expected_type == "integer" and not isinstance(data, int):
                raise ValueError(f"Expected integer, got {type(data).__name__}")
            elif expected_type == "boolean" and not isinstance(data, bool):
                raise ValueError(f"Expected boolean, got {type(data).__name__}")

        # For objects, check required properties
        if hasattr(schema, "required") and schema.required and isinstance(data, dict):
            for required_prop in schema.required:
                if required_prop not in data:
                    raise ValueError(f"Missing required property: {required_prop}")

        # For arrays, validate items if schema provided
        if hasattr(schema, "items") and schema.items and isinstance(data, list):
            for item in data:
                try:
                    self._validate_data_against_schema(item, schema.items)
                except ValueError as e:
                    raise ValueError(f"Array item validation failed: {e}")

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
        """Initializes the mock server by loading the spec and registering routes."""
        if self._mock_spec:
            self._register_routes(self._mock_spec)
        yield
