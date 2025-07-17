# Development Guide for huehoppy

This document explains how to set up the development environment, run tests, create releases, and contribute to huehoppy.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/terragonlabs/huehoppy.git
   cd huehoppy
   ```

2. **Set up development environment**
   ```bash
   ./scripts/dev-setup.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Run tests**
   ```bash
   ./scripts/test.sh
   ```

5. **Set up GitHub Actions** (optional)
   ```bash
   ./scripts/setup-github-actions.sh
   ```

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Make (optional, for convenience)

### Manual Setup

If you prefer to set up manually instead of using the `dev-setup.sh` script:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev,test,all]"

# Install pre-commit hooks
pre-commit install

# Make scripts executable
chmod +x scripts/*.sh
```

## Git Tag-based Semversioning

This project uses `setuptools-scm` for automatic version management based on git tags.

### How It Works

1. **Version Detection**: The version is automatically determined from git tags
2. **Development Versions**: Between releases, versions include the commit hash
3. **Release Versions**: Tagged versions are clean (e.g., `1.0.0`)

### Version Examples

- `1.0.0` - Clean release from tag `v1.0.0`
- `1.0.1.dev3+g1234567` - Development version (3 commits after v1.0.0)
- `1.0.1.dev3+g1234567.dirty` - Development version with uncommitted changes

### Creating Releases

Use the release script which handles everything automatically:

```bash
./scripts/release.sh
```

This will:
1. Run all tests
2. Build the package
3. Create a git tag
4. Push to remote
5. Upload to PyPI (if configured)
6. Create GitHub release

### Manual Release Process

If you need to create a release manually:

```bash
# 1. Ensure clean working directory
git status

# 2. Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 3. Build and test
./scripts/build.sh
./scripts/test.sh

# 4. Upload to PyPI (if configured)
twine upload dist/*
```

## Testing

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage
pytest --cov=huehoppy --cov-report=html

# Run integration tests only
pytest tests/test_integration.py -v
```

### Test Categories

- **Unit Tests**: Test individual components (`test_core.py`, `test_algorithms.py`)
- **Integration Tests**: Test end-to-end workflows (`test_integration.py`)
- **CLI Tests**: Test command-line interface (`test_cli.py`)

### Writing Tests

1. **Test Structure**: Follow the existing patterns in the `tests/` directory
2. **Fixtures**: Use fixtures from `conftest.py` for common test data
3. **Naming**: Use descriptive test names that explain what's being tested
4. **Coverage**: Aim for >85% test coverage

## Building

### Python Package

```bash
./scripts/build.sh
```

This creates:
- Source distribution (`.tar.gz`)
- Wheel distribution (`.whl`)

### Binary Executables

```bash
./scripts/build-binaries.sh
```

This creates platform-specific binaries using PyInstaller.

### Docker Images

```bash
# Build Docker image
docker build -t huehoppy:latest .

# Run in container
docker run --rm huehoppy:latest --help
```

## Continuous Integration

### GitHub Actions Setup

Due to GitHub security restrictions, workflow files cannot be automatically created. Set them up manually:

```bash
# Use the setup script
./scripts/setup-github-actions.sh

# Or manually copy files
mkdir -p .github/workflows
cp github-workflows/*.yml .github/workflows/
git add .github/workflows/
git commit -m "Add GitHub Actions workflows"
git push origin <branch-name>
```

For detailed setup instructions, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md).

### GitHub Actions Workflows

The project includes three main workflows:

1. **CI Workflow** (`.github/workflows/ci.yml`)
   - Runs on push/PR to main/develop
   - Tests on multiple Python versions and platforms
   - Linting, type checking, security scans
   - Documentation building

2. **Release Workflow** (`.github/workflows/release.yml`)
   - Triggered by git tags
   - Builds packages and binaries
   - Uploads to PyPI
   - Creates GitHub releases

3. **Nightly Workflow** (`.github/workflows/nightly.yml`)
   - Runs comprehensive tests daily
   - Dependency auditing
   - Performance benchmarking

### Local CI Testing

Test the CI pipeline locally using `act`:

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI tests locally
act -j test
```

## Code Quality

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit:

- **ruff**: Linting and code style
- **black**: Code formatting
- **mypy**: Type checking
- **bandit**: Security analysis
- **isort**: Import sorting

### Manual Quality Checks

```bash
# Linting
ruff check huehoppy tests

# Formatting
black huehoppy tests

# Type checking
mypy huehoppy

# Security scan
bandit -r huehoppy/
```

## Project Structure

```
huehoppy/
├── huehoppy/                   # Main package
│   ├── __init__.py
│   ├── cli.py                  # Command-line interface
│   ├── core/                   # Core framework
│   │   ├── __init__.py
│   │   ├── base.py            # Base classes
│   │   ├── manager.py         # Algorithm manager
│   │   └── pipeline.py        # Pipeline system
│   └── algorithms/            # Algorithm implementations
│       ├── __init__.py
│       └── reinhard/          # Example algorithm
├── tests/                     # Test suite
├── scripts/                   # Build and utility scripts
├── .github/workflows/         # GitHub Actions
├── docs/                      # Documentation
├── pyproject.toml            # Project configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
└── README.md                 # Project overview
```

## Adding New Algorithms

1. **Create algorithm directory**:
   ```bash
   mkdir huehoppy/algorithms/my_algorithm
   ```

2. **Implement algorithm**:
   ```python
   # huehoppy/algorithms/my_algorithm/algorithm.py
   from huehoppy.core.base import ColorTransferAlgorithm, AlgorithmMetadata
   
   class Algorithm(ColorTransferAlgorithm):
       @classmethod
       def get_metadata(cls):
           return AlgorithmMetadata(
               name="My Algorithm",
               description="Description of my algorithm",
               author="Your Name",
               version="1.0.0"
           )
       
       def transfer(self, source, reference, **kwargs):
           # Your implementation here
           return result
   ```

3. **Create `__init__.py`**:
   ```python
   # huehoppy/algorithms/my_algorithm/__init__.py
   from .algorithm import Algorithm
   
   __all__ = ["Algorithm"]
   ```

4. **Add tests**:
   ```python
   # tests/test_my_algorithm.py
   def test_my_algorithm():
       # Test your algorithm
       pass
   ```

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
sphinx-build -b html docs/ docs/_build/html/
```

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add docstrings to all public functions
- Update README.md for user-facing changes

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you've installed in development mode (`pip install -e .`)
2. **Test Failures**: Check that all dependencies are installed (`pip install -e ".[test]"`)
3. **Binary Build Failures**: Ensure PyInstaller is installed and all hidden imports are specified
4. **Version Detection Issues**: Ensure git tags are properly formatted (`vX.Y.Z`)

### Getting Help

- Check existing [Issues](https://github.com/terragonlabs/huehoppy/issues)
- Create a new issue with detailed information
- Include error messages and system information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Pull Request Guidelines

- Clear description of changes
- Tests for new features
- Documentation updates
- Follow existing code style
- Link to relevant issues

## Release Process

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version tag created
- [ ] PyPI package uploaded
- [ ] GitHub release created
- [ ] Binaries built and uploaded

## Performance Considerations

- Use numpy operations where possible
- Avoid copying large arrays unnecessarily
- Profile code for bottlenecks
- Consider memory usage for large images
- Test with realistic image sizes

## Security

- Never commit secrets or API keys
- Use security scanning tools
- Follow security best practices
- Report security issues privately

This development guide should provide everything needed to contribute to huehoppy effectively!