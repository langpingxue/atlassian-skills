# Atlassian Skills Test Suite

This directory contains comprehensive test coverage for all Jira, Confluence, and Bitbucket methods.

## Test Coverage

**203 test cases** covering **45 methods**:

### Jira (22 methods, 83 tests)
- Issue management (5 methods, 16 tests)
- Agile/Sprint management (6 methods, 15 tests)
- Issue links (4 methods, 11 tests)
- Projects and versions (4 methods, 10 tests)
- Search (2 methods, 10 tests)
- User management (1 method, 4 tests)
- Workflow transitions (2 methods, 8 tests)
- Worklogs (2 methods, 9 tests)

### Confluence (11 methods, 41 tests)
- Page management (4 methods, 15 tests)
- Comments (2 methods, 6 tests)
- Labels (3 methods, 9 tests)
- Search (1 method, 6 tests)
- User search (1 method, 5 tests)

### Bitbucket (12 methods, 45 tests)
- Commits (2 methods, 9 tests)
- Files and search (2 methods, 11 tests)
- Projects and repositories (2 methods, 5 tests)
- Pull requests (6 methods, 20 tests)

### Common Module (34 tests)
- Configuration management (AtlassianConfig)
- HTTP client (AtlassianClient)
- Helper functions (formatting, parsing, etc.)

## Test Statistics

| Category | Files | Methods | Tests |
|----------|-------|---------|-------|
| Jira | 8 | 22 | 83 |
| Confluence | 5 | 11 | 41 |
| Bitbucket | 4 | 12 | 45 |
| Common | 1 | - | 34 |
| **Total** | **18** | **45** | **203** |

## Installation

```bash
# Activate project virtual environment
source .venv/bin/activate

# Or install test dependencies
pip install -r test/requirements.txt
```

## Running Tests

### Run All Tests
```bash
pytest test/ -v
```

### Run Specific Module Tests
```bash
# Jira tests
pytest test/test_jira_*.py -v

# Confluence tests
pytest test/test_confluence_*.py -v

# Bitbucket tests
pytest test/test_bitbucket_*.py -v

# Common module tests
pytest test/test_common.py -v
```

### Run Specific Test File
```bash
pytest test/test_jira_issues.py -v
```

### Run Specific Test Class or Method
```bash
# Run specific test class
pytest test/test_jira_issues.py::TestJiraGetIssue -v

# Run specific test method
pytest test/test_jira_issues.py::TestJiraGetIssue::test_get_issue_success -v
```

### Generate Coverage Report
```bash
pytest test/ --cov=atlassian-skills/scripts --cov-report=html
```

## Test Structure

Each test file corresponds to a script file:

```
test/
├── conftest.py              # Shared fixtures and configuration
├── pytest.ini               # pytest configuration
├── requirements.txt         # Test dependencies
├── test_common.py           # _common.py tests (34 tests)
├── test_jira_*.py          # Jira tests (8 files, 83 tests)
├── test_confluence_*.py    # Confluence tests (5 files, 41 tests)
└── test_bitbucket_*.py     # Bitbucket tests (4 files, 45 tests)
```

## Test Types

Each method includes the following test types:

1. **Success scenarios** - Verify normal functionality
2. **Parameter validation** - Verify required parameter checks
3. **Error handling** - Verify exception handling
4. **Boundary conditions** - Verify edge cases and special situations

## Mock Strategy

All tests use mocks to isolate external dependencies:
- Mock HTTP client to avoid actual API calls
- Mock configuration to avoid requiring real credentials
- Use pytest fixtures to provide test data

## Test Dependencies

```
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
requests>=2.28.0
python-dotenv>=1.0.0
```

## Continuous Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run tests
  run: |
    pip install -r test/requirements.txt
    pytest test/ -v --cov
```

## Quality Assurance

### Code Quality
- All tests pass (203/203)
- Mock isolation for external dependencies
- Clear test naming conventions
- Consistent test structure
- Complete error scenario coverage

### Documentation
- Each test has clear docstrings
- README with comprehensive instructions
- Inline comments for complex logic

### Maintainability
- Fixtures reduce code duplication
- Tests are independent and can run individually
- Correct mock path configuration
- Clear test organization structure

## Contributing

When adding new features, ensure:
1. Add corresponding tests for new methods
2. Cover both success and failure scenarios
3. Run all tests to ensure no regressions
4. Keep tests concise and maintainable

## Troubleshooting

### Import Errors
If you encounter import errors, ensure Python path is correct:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/atlassian-skills/scripts"
```

### Mock Not Working
Ensure mock paths are correct, use `scripts.module_name.function_name` format.

### Test Failures
Run individual tests to see detailed errors:
```bash
pytest test/test_file.py::TestClass::test_method -vv
```

## Future Recommendations

1. **CI/CD Integration**: Integrate tests into GitHub Actions or other CI systems
2. **Coverage Target**: Maintain current 100% coverage standard
3. **Performance Testing**: Consider adding performance benchmarks
4. **Integration Testing**: Optionally add real API integration tests (requires test environment)
5. **Documentation Sync**: Update tests when adding new features
