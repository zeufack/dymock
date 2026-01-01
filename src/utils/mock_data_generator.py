from typing import Any, Dict, List
import random

from faker import Faker

from src.models.schema_object import SchemaObject
from src.models.reference_object import ReferenceObject


class MockDataGenerator:
    """Generates mock data based on OpenAPI schema definitions."""

    def __init__(self):
        self.faker = Faker()

    def generate_from_schema(self, schema: SchemaObject | ReferenceObject) -> Any:
        """Generate mock data based on the provided schema."""
        # Handle ReferenceObject - for now, return a placeholder
        if isinstance(schema, ReferenceObject):
            # Extract the referenced type from the $ref
            ref = schema.ref
            if "#/components/schemas/" in ref:
                schema_name = ref.split("/")[-1]
                # Return a placeholder object with the schema name
                return {
                    "$ref": schema_name,
                    "placeholder": True,
                    "description": f"Referenced schema: {schema_name}",
                }
            return {"$ref": ref, "placeholder": True}

        if schema.enum:
            return random.choice(schema.enum)

        if schema.type == "string":
            return self._generate_string(schema)
        elif schema.type == "integer":
            return self._generate_integer(schema)
        elif schema.type == "number":
            return self._generate_number(schema)
        elif schema.type == "boolean":
            return random.choice([True, False])
        elif schema.type == "object":
            return self._generate_object(schema)
        elif schema.type == "array":
            return self._generate_array(schema)
        elif schema.type == "null":
            return None
        else:
            # Default fallback
            return self.faker.word()

    def _generate_string(self, schema: SchemaObject) -> str:
        """Generate a mock string based on schema constraints."""
        format_type = schema.format

        if format_type == "date":
            return self.faker.date().isoformat()
        elif format_type == "date-time":
            return self.faker.date_time().isoformat()
        elif format_type == "email":
            return self.faker.email()
        elif format_type == "uri":
            return self.faker.url()
        elif format_type == "uuid":
            return str(self.faker.uuid4())
        elif format_type == "hostname":
            return self.faker.domain_name()
        elif format_type == "ipv4":
            return self.faker.ipv4()
        elif format_type == "ipv6":
            return self.faker.ipv6()
        else:
            # Regular string with length constraints
            min_len = schema.minLength or 1
            max_len = schema.maxLength or 50
            length = random.randint(min_len, min(max_len, 100))  # Cap at 100 chars

            if schema.pattern:
                # For now, just generate a random string if pattern is specified
                return self.faker.pystr(min_chars=length, max_chars=length)

            return self.faker.pystr(min_chars=length, max_chars=length)

    def _generate_integer(self, schema: SchemaObject) -> int:
        """Generate a mock integer."""
        # Note: OpenAPI spec has minimum/maximum, but we'll use reasonable defaults
        min_val = getattr(schema, "minimum", 0)
        max_val = getattr(schema, "maximum", 1000)
        return random.randint(min_val, max_val)

    def _generate_number(self, schema: SchemaObject) -> float:
        """Generate a mock number (float)."""
        min_val = getattr(schema, "minimum", 0.0)
        max_val = getattr(schema, "maximum", 1000.0)
        return random.uniform(min_val, max_val)

    def _generate_object(self, schema: SchemaObject) -> Dict[str, Any]:
        """Generate a mock object with properties."""
        result = {}

        if schema.properties:
            for prop_name, prop_schema in schema.properties.items():
                # Check if property is required
                is_required = schema.required and prop_name in schema.required
                if is_required or random.choice(
                    [True, False]
                ):  # 50% chance for optional
                    result[prop_name] = self.generate_from_schema(prop_schema)

        # If no properties were generated and we have a schema, generate at least one
        if not result and schema.properties:
            # Pick a random property to ensure we have some data
            prop_name = random.choice(list(schema.properties.keys()))
            prop_schema = schema.properties[prop_name]
            result[prop_name] = self.generate_from_schema(prop_schema)

        return result

    def _generate_array(self, schema: SchemaObject) -> List[Any]:
        """Generate a mock array."""
        if not schema.items:
            return []

        # Generate 1-5 items by default
        count = random.randint(1, 5)
        return [self.generate_from_schema(schema.items) for _ in range(count)]
