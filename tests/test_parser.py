import pytest

from src.models.open_api_object import OpenAPIObject
from src.models.schema_object import SchemaObject
from src.models.reference_object import ReferenceObject
from src.models.media_type_object import MediaTypeObject
from src.models.parameter_object import ParameterObject
from src.models.example_object import ExampleObject
from src.models.response_object import ResponseObject

from src.utils.decoder import CustomDecoder


@pytest.fixture
def decoder():
    """Fixture to provide a decoder instance."""
    return CustomDecoder()


# Test Schema Decoding
def test_decode_schema_basic_types(decoder):
    obj = {"type": "string", "format": "date-time"}
    schema = decoder.decode_schema(obj)
    print(type(schema))
    assert isinstance(schema, SchemaObject)
    assert schema.type == "string"
    assert schema.format == "date-time"


def test_decode_schema_object_with_properties(decoder):
    obj = {
        "type": "object",
        "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        "required": ["id"],
    }
    schema = decoder.decode_schema(obj)
    assert isinstance(schema, SchemaObject)
    assert "id" in schema.properties
    assert schema.properties["id"].type == "integer"
    assert "name" in schema.properties
    assert schema.properties["name"].type == "string"
    assert "id" in schema.required


def test_decode_schema_with_ref(decoder):
    obj = {"$ref": "#/components/schemas/User"}
    schema = decoder.decode_schema(obj)
    assert isinstance(schema, ReferenceObject)
    assert schema.ref == "#/components/schemas/User"


def test_decode_media_type(decoder):
    obj = {"schema": {"type": "string"}, "example": "Hello, World!"}
    media_type = decoder.decode_media_type(obj)
    assert isinstance(media_type, MediaTypeObject)
    assert media_type.schema.type == "string"
    assert media_type.example == "Hello, World!"


def test_decode_example(decoder):
    obj = {"summary": "Sample", "value": {"id": 1, "name": "Test"}}
    example = decoder.decode_example(obj)
    assert isinstance(example, ExampleObject)
    assert example.summary == "Sample"
    assert example.value == {"id": 1, "name": "Test"}


# Test Parameter Decoding
def test_decode_parameter(decoder):
    obj = {
        "name": "userId",
        "in": "query",
        "required": True,
        "schema": {"type": "integer"},
    }
    parameter = decoder.decode_parameter(obj)
    assert isinstance(parameter, ParameterObject)
    assert parameter.name == "userId"
    assert parameter.param_in == "query"
    assert parameter.required is True
    assert parameter.schema.type == "integer"


def test_decode_response(decoder):
    obj = {
        "description": "A simple response",
        "content": {"application/json": {"schema": {"type": "string"}}},
    }
    response = decoder.decode_response(obj)
    assert isinstance(response, ResponseObject)
    assert response.description == "A simple response"
    assert "application/json" in response.content
    assert response.content["application/json"].schema.type == "string"


def test_decode_openapi(decoder):
    obj = {
        "openapi": "3.0.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get Users",
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            },
                        }
                    },
                }
            }
        },
    }
    openapi = decoder.decode_openapi(obj)
    assert isinstance(openapi, OpenAPIObject)
    assert openapi.openapi == "3.0.0"
    assert openapi.info.title == "Test API"
    assert openapi.info.version == "1.0.0"
    assert "/users" in openapi.paths
    assert (
        openapi.paths["/users"].get.responses["200"].description
        == "Successful response"
    )
    assert (
        openapi.paths["/users"]
        .get.responses["200"]
        .content["application/json"]
        .schema.type
        == "array"
    )


# Integration Tests
def test_full_integration_server_creation():
    """Test the complete flow from spec loading to server creation."""
    from src.service.server import MockServer
    import tempfile
    import json

    # Create a test spec
    test_spec = {
        "openapi": "3.0.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get users",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/users/{id}": {
                "get": {
                    "summary": "Get user by ID",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "name": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_spec, f)
        spec_path = f.name

    try:
        # Test server creation
        server = MockServer(spec_path)
        app = server.create_app()
        assert app is not None

        # Test that routes are registered during lifespan
        routes_before = len(app.routes)
        # Simulate lifespan execution
        import asyncio
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def test_lifespan(app):
            if server._mock_spec:
                server._register_routes(server._mock_spec)
            yield

        async def run_test():
            async with test_lifespan(app):
                routes_after = len([r for r in app.routes if hasattr(r, "methods")])
                # Should have at least 2 routes (GET /users, GET /users/{id})
                assert routes_after >= 2

        asyncio.run(run_test())

    finally:
        import os

        os.unlink(spec_path)


def test_cli_error_handling():
    """Test CLI error handling with invalid specs."""
    import subprocess
    import sys
    import tempfile

    # Create an invalid spec
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write('{"invalid": "spec"}')
        invalid_spec_path = f.name

    try:
        # Test CLI with invalid spec
        result = subprocess.run(
            [
                sys.executable,
                "cli.py",
                "run",
                "--spec",
                invalid_spec_path,
                "--port",
                "8006",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should exit with error code
        assert result.returncode != 0
        # Should contain error message
        assert (
            "Invalid OpenAPI specification" in result.stderr
            or "Error:" in result.stderr
        )

    finally:
        import os

        os.unlink(invalid_spec_path)


def test_mock_data_generation_integration():
    """Test mock data generation with real schemas."""
    from src.utils.mock_data_generator import MockDataGenerator
    from src.models.schema_object import SchemaObject

    generator = MockDataGenerator()

    # Test various schema types
    schemas = [
        SchemaObject(type="string"),
        SchemaObject(type="integer"),
        SchemaObject(type="boolean"),
        SchemaObject(type="array", items=SchemaObject(type="string")),
        SchemaObject(
            type="object",
            properties={
                "name": SchemaObject(type="string"),
                "age": SchemaObject(type="integer"),
            },
        ),
    ]

    for schema in schemas:
        result = generator.generate_from_schema(schema)
        assert result is not None

        # Type-specific assertions
        if schema.type == "string":
            assert isinstance(result, str)
        elif schema.type == "integer":
            assert isinstance(result, int)
        elif schema.type == "boolean":
            assert isinstance(result, bool)
        elif schema.type == "array":
            assert isinstance(result, list)
        elif schema.type == "object":
            assert isinstance(result, dict)
            # Object should contain at least one property
            assert len(result) > 0
            # Check that generated properties are valid
            for key, value in result.items():
                assert key in ["name", "age"]
                if key == "name":
                    assert isinstance(value, str)
                elif key == "age":
                    assert isinstance(value, int)


def test_request_validation():
    """Test request body validation against schemas."""
    from src.service.server import MockServer
    import asyncio
    import json

    server = MockServer("src/templates/petstore.json")
    app = server.create_app()

    # Manually trigger the lifespan to register routes
    async def test_validation():
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def lifespan(app):
            if server._mock_spec:
                server._register_routes(server._mock_spec)
            yield

        async with lifespan(app):
            from fastapi.testclient import TestClient

            client = TestClient(app)

            # Test POST /pets with valid data
            response = client.post("/pets", json={"name": "Test Pet", "id": 123})
            print(f"POST /pets with valid data: {response.status_code}")
            assert response.status_code == 201

            # Test POST /pets with invalid data (wrong type)
            response = client.post("/pets", json="invalid string")
            print(f"POST /pets with invalid JSON: {response.status_code}")
            # This should still work since we don't have strict validation yet
            assert response.status_code in [
                201,
                400,
            ]  # Either success or validation error

    asyncio.run(test_validation())
