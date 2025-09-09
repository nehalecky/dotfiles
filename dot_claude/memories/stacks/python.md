# Python Development Stack

## Core Toolchain

### Package Management with UV
**UV is the preferred Python package manager** - ultra-fast, modern replacement for pip/poetry/virtualenv.

```bash
# Project initialization
uv init project-name          # Create new Python project
cd project-name
uv venv                       # Create virtual environment (if not auto-created)

# Dependency management
uv add package-name           # Add runtime dependency
uv add --dev pytest          # Add development dependency
uv add "package>=1.0,<2.0"   # Add with version constraints

# Environment management
uv run script.py              # Run in managed environment
uv run pytest                # Run tests in environment
uv sync                       # Sync dependencies to match lock file
```

### Project Structure Convention
```
project-name/
├── pyproject.toml            # Project configuration and dependencies
├── uv.lock                   # Locked dependency versions
├── README.md                 # Project documentation
├── src/                      # Source code (preferred layout)
│   └── package_name/         # Main package
│       ├── __init__.py
│       ├── main.py          # CLI entry point
│       └── core/            # Core modules
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py          # Pytest configuration
└── docs/                     # Documentation (if needed)
```

## Code Quality Tools

### Ruff (Linting and Formatting)
**Ruff is the preferred linter and formatter** - extremely fast Rust-based tool.

```bash
# Installation (usually in dev dependencies)
uv add --dev ruff

# Linting
uv run ruff check .           # Check for issues
uv run ruff check --fix .     # Auto-fix issues
uv run ruff check --diff .    # Show what would be fixed

# Formatting  
uv run ruff format .          # Format all files
uv run ruff format --diff .   # Show formatting changes
```

### Type Checking with MyPy
```bash
# Installation
uv add --dev mypy

# Type checking
uv run mypy src/              # Check source directory
uv run mypy --strict src/     # Strict type checking
uv run mypy --install-types   # Install missing type stubs
```

### Configuration in pyproject.toml
```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings  
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
```

## Testing Framework

### Pytest Setup
```bash
# Installation
uv add --dev pytest pytest-cov pytest-xdist

# Running tests
uv run pytest                 # Run all tests
uv run pytest -v              # Verbose output
uv run pytest -x              # Stop on first failure
uv run pytest --cov=src       # Coverage report
uv run pytest -n auto         # Parallel execution
```

### Test Structure and Conventions
```python
# tests/conftest.py - Shared fixtures
import pytest
from src.package_name.main import create_app

@pytest.fixture
def app():
    """Create test application instance."""
    return create_app(test_mode=True)

# tests/test_main.py - Test module
import pytest
from src.package_name.main import main_function

def test_main_function_success():
    """Test main function with valid input."""
    result = main_function("valid_input")
    assert result == "expected_output"

def test_main_function_error():
    """Test main function error handling."""
    with pytest.raises(ValueError, match="expected error message"):
        main_function("invalid_input")
```

## Development Workflow

### Daily Development Commands
```bash
# Start development session
cd project-directory
uv sync                       # Ensure dependencies are current

# Development cycle
uv run ruff format . && uv run ruff check . --fix  # Format and lint
uv run mypy src/              # Type check
uv run pytest                # Run tests
uv run python -m package_name # Run application

# Before committing
uv run ruff format .          # Format code
uv run ruff check .           # Final lint check
uv run pytest --cov=src      # Test with coverage
```

### Virtual Environment Best Practices
```bash
# UV automatically manages virtual environments
# No need for manual venv activation

# Check environment status
uv run python --version      # Python version in environment
uv pip list                  # Installed packages

# Clean environment
rm -rf .venv                 # Remove virtual environment
uv sync                      # Recreate from lock file
```

## CLI Application Patterns

### Using Click for CLI
```bash
# Add Click dependency
uv add click

# Entry point in pyproject.toml
[project.scripts]
app-name = "package_name.main:cli"
```

```python
# src/package_name/main.py
import click

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.argument('input_file', type=click.Path(exists=True))
def cli(verbose: bool, input_file: str) -> None:
    """Main CLI application entry point."""
    if verbose:
        click.echo(f"Processing file: {input_file}")
    # Application logic here

if __name__ == '__main__':
    cli()
```

### Rich for Terminal UI
```bash
# Add Rich for beautiful terminal output
uv add rich

# Example usage
from rich.console import Console
from rich.table import Table

console = Console()

def display_results(data):
    """Display results with Rich formatting."""
    table = Table(title="Results")
    table.add_column("Name", style="cyan")
    table.add_column("Value", style="green")
    
    for item in data:
        table.add_row(item.name, str(item.value))
    
    console.print(table)
```

## Performance and Optimization

### Python Version Requirements
- **Python 3.12+** - Use modern Python features and performance improvements
- **Type hints required** - Use Python 3.12 type syntax (`list[str]` not `List[str]`)
- **Async when appropriate** - Use `asyncio` for I/O-bound operations

### Memory and Startup Optimization
```python
# Lazy imports for faster startup
def expensive_function():
    import heavy_library  # Import only when needed
    return heavy_library.process()

# Use __slots__ for data classes with many instances
from dataclasses import dataclass

@dataclass
class Point:
    __slots__ = ('x', 'y')
    x: float
    y: float
```

### Performance Monitoring
```bash
# Add development profiling tools
uv add --dev py-spy line_profiler memory_profiler

# Profile application
py-spy top --pid <python-process-id>    # Live profiling
py-spy record -o profile.svg -- python app.py  # Record profile
```

## Integration Patterns

### Environment Variables
```python
# Use pydantic-settings for configuration
uv add pydantic-settings

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///app.db"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Logging Configuration
```python
import logging
from rich.logging import RichHandler

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger(__name__)
```

### Error Handling Patterns
```python
# Use result types for better error handling
from typing import Union, Optional
from enum import Enum

class ErrorCode(Enum):
    INVALID_INPUT = "invalid_input"
    NETWORK_ERROR = "network_error"
    
def process_data(data: str) -> Union[str, ErrorCode]:
    """Process data and return result or error code."""
    if not data:
        return ErrorCode.INVALID_INPUT
    
    try:
        # Processing logic
        return processed_result
    except NetworkError:
        return ErrorCode.NETWORK_ERROR
```

## Testing Strategies

### Test Categories
```bash
# Unit tests - Fast, isolated
uv run pytest tests/unit/ -v

# Integration tests - Database, API calls
uv run pytest tests/integration/ -v  

# End-to-end tests - Full application workflow
uv run pytest tests/e2e/ -v --slow
```

### Mock and Fixture Patterns
```python
# tests/conftest.py
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_api():
    """Mock external API calls."""
    with patch('package_name.api.make_request') as mock:
        mock.return_value = {"status": "success"}
        yield mock

# Use in tests
def test_api_integration(mock_api):
    result = call_api_function()
    assert result["status"] == "success"
    mock_api.assert_called_once()
```

This module provides comprehensive Python development patterns optimized for modern Python development with UV, Ruff, and pytest.