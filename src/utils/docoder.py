from typing import Any, Dict, List, Union

import msgspec
from msgspec import Struct

from src.models.component_object import ComponentsObject
from src.models.contact_object import ContactObject
from src.models.example_object import ExampleObject
from src.models.external_documentation_object import ExternalDocumentationObject
from src.models.header_object import HeaderObject
from src.models.info_object import InfoObject
from src.models.license_object import LicenseObject
from src.models.media_type_object import MediaTypeObject
from src.models.open_api_object import OpenAPIObject
from src.models.operation_object import OperationObject
from src.models.parameter_object import ParameterObject
from src.models.path_item_object import PathItemObject
from src.models.reference_object import ReferenceObject
from src.models.request_body_body import RequestBodyObject
from src.models.response_object import ResponseObject
from src.models.schema_object import SchemaObject
from src.models.security_scheme_object import SecuritySchemeObject
from src.models.server_object import ServerObject
from src.models.tag_object import TagObject
from src.models.encoding_object import EncodingObject


class CustomDecoder:
    """As msgspec have limation to work we union type, this custome decoder will help us handle the union type."""

    def __init__(self):
        self._decoders = {
            "info": self.decode_info,
            "schema": self.decode_schema,
            "media_type": self.decode_media_type,
            "parameter": self.decode_parameter,
            "response": self.decode_response,
            "request_body": self.decode_request_body,
            "operation": self.decode_operation,
            "path_item": self.decode_path_item,
            "components": self.decode_components,
        }

    def _safe_decode(self, obj: Any, decoder_type: str) -> Any:
        if not isinstance(obj, dict):
            raise TypeError(
                f"Expected dict for {decoder_type}, got {type(obj).__name__}"
            )
        return self._decoders[decoder_type](obj)

    def _decode_reference_or_inline(
        self, obj: Dict[str, Any], inline_type: type, required_fields: List[str] = None
    ) -> Union[Struct, ReferenceObject]:
        """Helper to decode either a ReferenceObject or an inline object."""
        if "$ref" in obj:
            ref_kwargs = {"ref": obj["$ref"]}
            if "summary" in obj:
                ref_kwargs["summary"] = obj["summary"]
            if "description" in obj:
                ref_kwargs["description"] = obj["description"]
            return ReferenceObject(**ref_kwargs)

        kwargs = dict(obj)
        if required_fields:
            for field in required_fields:
                if field not in kwargs:
                    raise ValueError(
                        f"Missing required field '{field}' in {inline_type.__name__}"
                    )
        return inline_type(**kwargs)

    def decode_schema(
        self, obj: Dict[str, Any]
    ) -> Union[SchemaObject, ReferenceObject]:
        """Decode OpenAPI Schema object or Reference."""
        if "$ref" in obj:
            return ReferenceObject(ref=obj["$ref"])

        schema_type = obj.get("type")
        kwargs = dict(obj)

        if schema_type == "object":
            if "properties" in obj:
                kwargs["properties"] = {
                    k: self.decode_schema(v) for k, v in obj["properties"].items()
                }
            kwargs["required"] = obj.get("required", [])
        elif schema_type == "array" and "items" in obj:
            kwargs["items"] = self.decode_schema(obj["items"])
        elif any(k in obj for k in ("allOf", "anyOf", "oneOf")):
            for key in ("allOf", "anyOf", "oneOf"):
                if key in obj:
                    kwargs[key] = [self.decode_schema(s) for s in obj[key]]

        return SchemaObject(**kwargs)

    def decode_media_type(self, obj: Dict[str, Any]) -> MediaTypeObject:
        """Decode MediaType object."""
        kwargs = dict(obj)
        if "schema" in obj:
            kwargs["schema"] = self.decode_schema(obj["schema"])
        if "encoding" in obj:
            kwargs["encoding"] = {
                k: self.decode_encoding(v) for k, v in obj["encoding"].items()
            }
        return MediaTypeObject(**kwargs)

    def decode_encoding(self, obj: Dict[str, Any]) -> EncodingObject:
        """Decode Encoding object."""
        kwargs = dict(obj)
        if "headers" in obj:
            kwargs["headers"] = {
                k: self.decode_header(v) for k, v in obj["headers"].items()
            }
        return EncodingObject(**kwargs)

    def decode_parameter(
        self, obj: Dict[str, Any]
    ) -> Union[ParameterObject, ReferenceObject]:
        """Decode Parameter object or Reference."""
        if "$ref" in obj:
            return ReferenceObject(ref=obj["$ref"])

        if "in" not in obj:
            raise ValueError("Parameter object missing required 'in' field")

        kwargs = {
            k: v
            for k, v in obj.items()
            if k != "schema" and k != "content" and k != "in"
        }
        kwargs["schema"] = (
            self.decode_schema(obj["schema"]) if "schema" in obj else None
        )
        kwargs["content"] = {
            k: self.decode_media_type(v) for k, v in obj.get("content", {}).items()
        }
        kwargs["param_in"] = obj["in"]
        return ParameterObject(**kwargs)

    def decode_header(
        self, obj: Dict[str, Any]
    ) -> Union[HeaderObject, ReferenceObject]:
        """Decode Header object or Reference."""
        if "$ref" in obj:
            return ReferenceObject(ref=obj["$ref"])

        kwargs = dict(obj)
        # Handle schema or content (mutually exclusive)
        if "schema" in obj and "content" in obj:
            raise ValueError("Header object cannot have both 'schema' and 'content'")
        if "schema" in obj:
            kwargs["schema"] = self.decode_schema(obj["schema"])
        if "content" in obj:
            kwargs["content"] = {
                k: self.decode_media_type(v) for k, v in obj["content"].items()
            }
        # Capture extensions
        extensions = {k: v for k, v in obj.items() if k.startswith("x-")}
        if extensions:
            kwargs["extensions"] = extensions
        return HeaderObject(**kwargs)

    def decode_response(
        self, obj: Dict[str, Any]
    ) -> Union[ResponseObject, ReferenceObject]:
        """Decode Response object or Reference."""
        if "$ref" in obj:
            return ReferenceObject(ref=obj["$ref"])

        kwargs = dict({k: v for k, v in obj.items() if k != "headers"})
        if "content" in obj:
            kwargs["content"] = {
                k: self.decode_media_type(v) for k, v in obj["content"].items()
            }
        if "headers" in obj:
            kwargs["headers"] = {
                k: self.decode_header(v) for k, v in obj["headers"].items()
            }
        if "description" not in kwargs:
            raise ValueError("Response object missing required 'description' field")
        return ResponseObject(**kwargs)

    def decode_request_body(
        self, obj: Dict[str, Any]
    ) -> Union[RequestBodyObject, ReferenceObject]:
        """Decode RequestBody object or Reference."""
        if "$ref" in obj:
            return ReferenceObject(ref=obj["$ref"])

        return RequestBodyObject(
            content={
                k: self.decode_media_type(v) for k, v in obj.get("content", {}).items()
            },
            **{k: v for k, v in obj.items() if k != "content"},
        )

    def decode_operation(self, obj: Dict[str, Any]) -> OperationObject:
        """Decode Operation object."""
        return OperationObject(
            parameters=[self.decode_parameter(p) for p in obj.get("parameters", [])],
            responses={
                k: self.decode_response(v) for k, v in obj.get("responses", {}).items()
            }
            if "responses" in obj
            else None,
            requestBody=self.decode_request_body(obj["requestBody"])
            if "requestBody" in obj
            else None,
            **{
                k: v
                for k, v in obj.items()
                if k not in ("requestBody", "responses", "parameters")
            },
        )

    def decode_path_item(self, obj: Dict[str, Any]) -> PathItemObject:
        """Decode PathItem object."""
        return PathItemObject(
            **{
                method: self.decode_operation(obj[method])
                for method in {"get", "put", "post", "delete", "patch"}
                if method in obj
            }
        )

    def decode_components(self, obj: Dict[str, Any]) -> ComponentsObject:
        """Decode Components object."""
        return ComponentsObject(
            schemas={
                k: self.decode_schema(v) for k, v in obj.get("schemas", {}).items()
            },
            responses={
                k: self.decode_response(v) for k, v in obj.get("responses", {}).items()
            },
            parameters={
                k: self.decode_parameter(v)
                for k, v in obj.get("parameters", {}).items()
            },
            requestBodies={
                k: self.decode_request_body(v)
                for k, v in obj.get("requestBodies", {}).items()
            },
            **{
                k: v
                for k, v in obj.items()
                if k not in ("schemas", "responses", "parameters", "requestBodies")
            },
        )

    def decode_info(self, obj: Dict[str, Any]) -> InfoObject:
        return msgspec.json.decode(msgspec.json.encode(obj), type=InfoObject)

    def decode_contact(self, obj: Dict[str, Any]) -> ContactObject:
        return msgspec.json.decode(msgspec.json.encode(obj), type=ContactObject)

    def decode_license(self, obj: Dict[str, Any]) -> LicenseObject:
        return msgspec.json.decode(msgspec.json.encode(obj), type=LicenseObject)

    def decode_server(self, obj: Dict[str, Any]) -> ServerObject:
        return msgspec.json.decode(msgspec.json.encode(obj), type=ServerObject)

    def decode_security_scheme(self, obj: Dict[str, Any]) -> SecuritySchemeObject:
        return msgspec.json.decode(msgspec.json.encode(obj), type=SecuritySchemeObject)

    def decode_tag(self, obj: Dict[str, Any]) -> TagObject:
        return msgspec.json.decode(msgspec.json.encode(obj), type=TagObject)

    def decode_external_doc(self, obj: Dict[str, Any]) -> ExternalDocumentationObject:
        return msgspec.json.decode(
            msgspec.json.encode(obj), type=ExternalDocumentationObject
        )

    def decode_example(self, obj: Dict[str, Any]) -> ExampleObject:
        """Decode Example object."""
        return msgspec.json.decode(msgspec.json.encode(obj), type=ExampleObject)

    def decode_openapi(self, obj: Dict[str, Any]) -> OpenAPIObject:
        try:
            return OpenAPIObject(
                info=self._safe_decode(obj["info"], "info"),
                servers=[self.decode_server(s) for s in obj.get("servers", [])],
                paths={
                    k: self._safe_decode(v, "path_item")
                    for k, v in obj["paths"].items()
                },
                components=self._safe_decode(obj["components"], "components")
                if "components" in obj
                else None,
                security=[
                    self.decode_security_scheme(s) for s in obj.get("security", [])
                ],
                tags=[self.decode_tag(t) for t in obj.get("tags", [])],
                externalDocs=self.decode_external_doc(obj["externalDocs"])
                if "externalDocs" in obj
                else None,
                **{
                    k: v
                    for k, v in obj.items()
                    if k
                    not in (
                        "info",
                        "servers",
                        "paths",
                        "components",
                        "security",
                        "tags",
                        "externalDocs",
                    )
                },
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in OpenAPI spec: {e}")
