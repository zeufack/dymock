# AGENTS.md - Development Guidelines for dymock

## Overview
dymock is a Python-based service that generates mock APIs dynamically from OpenAPI specifications. It uses FastAPI for the web framework, msgspec for high-performance serialization, and provides a CLI interface for easy operation.

## Build, Lint, and Test Commands

### Running Tests
```bash
# Run all tests
pytest

# Run tests in verbose mode
pytest -v

# Run a specific test file
pytest tests/test_parser.py

# Run a single test function
pytest tests/test_parser.py::test_decode_schema_basic_types -v

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### Linting and Code Quality
```bash
# Run ruff linter (includes formatting and import sorting)
ruff check .

# Auto-fix ruff violations
ruff check . --fix

# Format code with ruff
ruff format .

# Run both linting and formatting
ruff check . --fix && ruff format .
```

### Development Server
```bash
# Run the server directly with Python
python main.py

# Run via CLI (when implemented)
python cli.py run --spec src/templates/petstore.json --host 127.0.0.1 --port 8000

# Run with uvicorn directly
uvicorn src.service.server:app --host 127.0.0.1 --port 8000
```

### Dependencies
```bash
# Install dependencies (using uv)
uv sync

# Add a new dependency
uv add package-name

# Update dependencies
uv lock --upgrade
```

## Code Style Guidelines

### Import Organization
```python
# Standard library imports first
import re
from pathlib import Path
from typing import Any, Dict, Optional

# Third-party imports (alphabetically sorted)
import msgspec
from fastapi import FastAPI
import pytest

# Local imports (use relative imports within src/)
from src.models.base_struct import BaseStruct
from src.utils.config import Config
```

### Type Hints
- Use type hints for all function parameters and return values
- Use `Union` types when multiple types are acceptable
- Use `Optional` for nullable types
- Use `|` syntax for Python 3.10+ union types when appropriate

```python
from typing import Optional, Union

def process_data(data: Union[str, bytes], format: str = "json") -> Optional[dict]:
    # Implementation
    pass
```

### Class Definitions
- Use `msgspec.Struct` as base class for data models
- Use PascalCase for class names
- Include docstrings for all classes

```python
import msgspec

class InfoObject(msgspec.Struct):
    """Provides metadata about the API."""

    title: str
    version: str
    summary: Optional[str] = None
    description: Optional[str] = None
```

### Method Definitions
- Use snake_case for method names
- Include docstrings with Args and Returns sections
- Use type hints for parameters and return values

```python
def parse_spec(self, spec_path: str | Path) -> OpenAPIObject:
    """Parse OpenAPI specification from file.

    Args:
        spec_path: Path to the OpenAPI specification file

    Returns:
        Parsed OpenAPI object
    """
    pass
```

### Error Handling
- Use specific exception types
- Include descriptive error messages
- Use `raise ... from e` for exception chaining
- Validate inputs early

```python
def load_file(file_path: str) -> str:
    """Load content from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Specification file not found: {file_path}") from e
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid encoding in file {file_path}") from e
```

### Async/Await Patterns
- Use async context managers for resource management
- Use async functions for I/O operations
- Follow FastAPI async patterns

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    # Setup code
    yield
    # Cleanup code
```

### Path Handling
- Use `pathlib.Path` for all file operations
- Validate file existence before operations
- Use absolute paths when necessary

```python
from pathlib import Path

def get_spec(spec_path: str | Path) -> OpenAPIObject:
    """Load OpenAPI spec from file."""
    path = Path(spec_path)
    if not path.is_file():
        raise ValueError(f"Cannot locate file: {spec_path}")
    # Process file
```

### Naming Conventions
- **Variables/Functions**: snake_case (`user_id`, `parse_spec`)
- **Classes**: PascalCase (`OpenAPIObject`, `MockServer`)
- **Constants**: UPPER_CASE (`DEFAULT_PORT = 8000`)
- **Private methods**: leading underscore (`_register_routes`)

### String Formatting
- Use f-strings for string interpolation
- Use descriptive format strings

```python
operation_id = operation.operationId or f"{method}_{path}".replace("/", "_")
error_msg = f"Failed to parse specification: {str(e)}"
```

### JSON/YAML Handling
- Use msgspec for high-performance serialization
- Handle both JSON and YAML formats consistently
- Validate data types after parsing

```python
import msgspec

def parse_data(data: str | bytes, format: str) -> dict:
    """Parse JSON or YAML data."""
    if format == "json":
        return msgspec.json.decode(data)
    elif format == "yaml":
        # Handle YAML parsing
        pass
    else:
        raise ValueError(f"Unsupported format: {format}")
```

### Testing Patterns
- Use descriptive test function names
- Use pytest fixtures for setup/teardown
- Test both success and error cases
- Use parametrized tests for multiple scenarios

```python
import pytest

@pytest.fixture
def decoder():
    """Provide a decoder instance for tests."""
    return CustomDecoder()

def test_decode_schema_basic_types(decoder):
    """Test decoding basic schema types."""
    obj = {"type": "string", "format": "date-time"}
    schema = decoder.decode_schema(obj)
    assert isinstance(schema, SchemaObject)
    assert schema.type == "string"
```

### CLI Commands
- Use click for CLI interfaces
- Provide helpful option descriptions
- Validate required parameters

```python
import click

@click.command()
@click.option(
    "--spec",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="Path to the OpenAPI specification file."
)
@click.option("--host", "-h", default="127.0.0.1", help="Host to run the server on.")
def run(spec, host, port):
    """Run the mock server."""
    pass
```

### Logging
- Use Python's logging module
- Configure appropriate log levels
- Include contextual information in log messages

```python
import logging

logger = logging.getLogger(__name__)

def process_request(path: str, method: str):
    """Process API request."""
    logger.info(f"Processing {method} request for path: {path}")
    # Implementation
```

### Configuration Management
- Centralize configuration in dedicated classes
- Use environment variables for sensitive data
- Provide sensible defaults

```python
class Config:
    """Application configuration."""

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8000

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
```

### Documentation
- Write comprehensive docstrings for public APIs
- Include usage examples in module docstrings
- Document CLI commands and options

### Performance Considerations
- Use msgspec.Struct for performance-critical data structures
- Minimize object creation in hot paths
- Use async operations for I/O bound tasks
- Profile code when optimizing

### Security Best Practices
- Validate all input data
- Avoid exposing sensitive information in logs
- Use secure defaults for network configuration
- Sanitize file paths to prevent directory traversal

## File Structure
```
src/
├── models/          # Data models (msgspec structs)
├── service/         # Core business logic
├── utils/           # Utility functions
└── templates/       # Sample OpenAPI specs

tests/               # Test files
├── conftest.py      # Pytest configuration
└── test_*.py        # Individual test files

pyproject.toml       # Project configuration
pytest.ini          # Test configuration
README.md           # Project documentation
```

## Common Patterns
- Use `msgspec.Struct` for all data models
- Implement `to_dict()` method for serialization
- Use async context managers for resource lifecycle
- Follow FastAPI patterns for web endpoints
- Use pathlib for file operations
- Include comprehensive error handling
- Write tests for all public functions</content>
<parameter name="filePath">/Users/patrick/project/dymock/AGENTS.md