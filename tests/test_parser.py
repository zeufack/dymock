import pytest

from src.models.open_api_object import OpenAPIObject
from src.models.schema_object import SchemaObject
from src.models.reference_object import ReferenceObject
from src.models.media_type_object import MediaTypeObject
from src.models.parameter_object import ParameterObject
from src.models.example_object import ExampleObject
from src.models.response_object import ResponseObject

from src.utils.docoder import CustomDecoder


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
