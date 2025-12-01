# Hollard Policy Assistant - Unit Tests

## Overview
This directory contains comprehensive unit tests for the Hollard Policy Assistant application.

## Test Files

### 1. `test_config.py`
Tests for configuration and file operations:
- Configuration constants validation
- Atomic file writing
- Unique filename generation
- File validation (size, extension)
- Document management operations

### 2. `test_utils.py`
Tests for utility functions:
- Text extraction from various file formats (.txt, .md, .pdf, .docx)
- Unicode and special character handling
- Edge cases (empty files, large files)
- Error handling for unsupported formats

### 3. `test_app_functions.py`
Tests for application UI functions:
- Handover detection mechanism
- Session state management
- Welcome message logic
- Avatar configuration
- File signature generation

### 4. `test_rag_engine.py`
Tests for RAG engine functionality:
- Document loading from various formats
- Text chunking configuration
- Embeddings model initialization
- Vector store operations
- Chat chain configuration
- System prompt validation
- Message history management
- Error handling

## Running Tests

### Run all tests:
```powershell
python -m pytest tests/
```

### Run specific test file:
```powershell
python -m pytest tests/test_config.py
```

### Run with verbose output:
```powershell
python -m pytest tests/ -v
```

### Run with coverage:
```powershell
python -m pytest tests/ --cov=. --cov-report=html
```

### Using unittest directly:
```powershell
python -m unittest discover -s tests -p "test_*.py"
```

### Run specific test class:
```powershell
python -m unittest tests.test_config.TestConfigConstants
```

### Run specific test method:
```powershell
python -m unittest tests.test_config.TestConfigConstants.test_chunk_size_is_positive
```

## Test Coverage

The tests cover:
- ✅ Configuration validation
- ✅ File operations (read, write, validate)
- ✅ Text extraction from multiple formats
- ✅ Handover detection logic
- ✅ Session state management
- ✅ Document loading and processing
- ✅ Vector store operations
- ✅ RAG chain configuration
- ✅ Error handling and edge cases

## Requirements

Install test dependencies:
```powershell
pip install pytest pytest-cov
```

Or install from requirements.txt if it includes test dependencies.

## Test Structure

Each test file follows this structure:
```python
import unittest

class TestFeatureName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_specific_behavior(self):
        """Test a specific behavior"""
        # Arrange
        # Act
        # Assert
        pass
```

## Mocking

Tests use mocking for:
- Streamlit components (to avoid GUI dependencies)
- OpenAI API calls (to avoid external API calls during testing)
- File system operations (when testing in isolation)

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- No external dependencies required (mocked)
- Fast execution
- Clear pass/fail indicators
- Detailed error messages

## Notes for Junior Developers

### Writing Good Tests:
1. **Arrange-Act-Assert**: Structure tests in three clear sections
2. **One assertion per test**: Keep tests focused
3. **Descriptive names**: Test names should describe what they test
4. **Test edge cases**: Empty inputs, None values, boundary conditions
5. **Clean up**: Always clean up resources in tearDown()

### Common Patterns:
- Use `setUp()` for test fixtures
- Use `tearDown()` for cleanup
- Use `self.assert*()` methods for assertions
- Use `with self.subTest()` for multiple similar assertions
- Mock external dependencies to isolate code under test

### Running Tests During Development:
```powershell
# Quick test run (single file)
python -m pytest tests/test_config.py -v

# Watch mode (re-run on changes) - requires pytest-watch
ptw tests/

# Run only failed tests
python -m pytest --lf
```

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass before committing
3. Maintain test coverage above 80%
4. Update this README if adding new test files
