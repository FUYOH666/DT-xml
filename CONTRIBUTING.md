# Contributing to DT-XML

Thank you for your interest in contributing to DT-XML! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if you have ideas)
- Examples of how it would be used

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Write tests** for new functionality
5. **Update documentation** if needed
6. **Run tests and linting**:
   ```bash
   uv run pytest
   uv run ruff check src/
   uv run pyright src/
   ```
7. **Commit your changes**: Use clear, descriptive commit messages
8. **Push to your fork**: `git push origin feature/your-feature-name`
9. **Create a Pull Request** with a clear description

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/ScanovichAI/DT-xml.git
   cd DT-xml
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set up pre-commit hooks (optional but recommended):
   ```bash
   uv run pre-commit install
   ```

4. Run tests:
   ```bash
   uv run pytest
   ```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use `ruff` for linting and formatting

### Code Structure

- Keep functions focused and small
- Use descriptive names
- Add docstrings for public functions/classes
- Comment complex logic

### Testing

- Write tests for new features
- Aim for good test coverage
- Use descriptive test names
- Test both success and error cases

## Documentation

- Update relevant documentation when adding features
- Use clear, concise language
- Provide examples where helpful
- Keep documentation in sync with code

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add OCR text processing support

- Implement OCRProcessor class
- Add field extraction from unstructured text
- Support OCR as fallback input format
```

Common prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

## Questions?

Feel free to open an issue for questions or discussions. We're happy to help!

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
