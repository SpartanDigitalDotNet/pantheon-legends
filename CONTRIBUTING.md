# Contributing to Pantheon Legends

Thank you for your interest in contributing to Pantheon Legends! This document provides guidelines and information for contributors.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pantheon-legends
   cd pantheon-legends
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure they pass all checks:
   ```bash
   # Run tests
   pytest
   
   # Check code formatting
   black legends/
   isort legends/
   
   # Type checking
   mypy legends/
   
   # Linting
   flake8 legends/
   ```

3. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

4. Push to your fork and create a pull request

## Code Style

- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Follow PEP 8 guidelines
- Add type hints for all public functions and methods
- Write docstrings for all public classes and functions

## Testing

- Write tests for new functionality
- Ensure all existing tests pass
- Aim for good test coverage
- Use pytest for testing
- Test async functionality properly

## Creating Legend Engines

When contributing new legend engines:

1. Implement the `ILegendEngine` protocol
2. Include comprehensive docstrings
3. Add progress reporting
4. Include quality metadata
5. Write tests for your engine
6. Add usage examples

Example structure:
```python
class YourLegendEngine:
    @property
    def name(self) -> str:
        return "YourLegend"
    
    async def run_async(self, request, progress_callback=None):
        # Implementation here
        pass
```

## Documentation

- Update README.md if you add new features
- Add docstrings to all public APIs
- Include usage examples for new functionality
- Update type hints and comments

## Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Ensure all CI checks pass
- Include tests for new functionality
- Update documentation as needed

## Issue Reporting

When reporting issues:

- Use a clear, descriptive title
- Provide steps to reproduce
- Include error messages and stack traces
- Specify Python version and environment
- Include relevant code samples

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing!
