from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional

import msgspec
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.models.open_api_object import OpenAPIObject
from src.utils.config import Config


class MockServer:
    def __init__(self, spec_path: str):
        self._spec_path = spec_path
        self._mock_spec: Optional[OpenAPIObject] = Config.get_spec(self._spec_path)
        self._app = FastAPI(lifespan=self._lifespan)

    def create_app(self) -> FastAPI:
        """Returns the FastAPI application instance."""
        return self._app

    def _create_handler(self, method: str, path: str, operation):
        async def handler(**path_params: Dict[str, Any]):
            return JSONResponse(
                content={
                    "mock": True,
                    "path": path,
                    "method": method.upper(),
                    "params": path_params,
                    "description": operation.summary or "No description provided",
                }
            )

        return handler

    def _register_routes(self, spec: OpenAPIObject):
        """Dynamically registers routes based on OpenAPI specification."""
        for path, methods in spec.paths.items():
            fast_api_path = Config.convert_openapi_path_to_fastapi(openapi_path=path)
            path_item_dict = msgspec.structs.asdict(methods)

            for method, operation in path_item_dict.items():
                if not operation:
                    continue
                print(operation)
                operation_id = operation.operationId or f"{method}_{path}".replace(
                    "/", "_"
                )
                handler = self._create_handler(method, path, operation)
                self._app.add_api_route(
                    fast_api_path,
                    handler,
                    methods=[method.upper()],
                    name=operation_id,
                )

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
        """Initializes the mock server by loading the spec and registering routes."""
        if self._mock_spec:
            self._register_routes(self._mock_spec)
        yield
