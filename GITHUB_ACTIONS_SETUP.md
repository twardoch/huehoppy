# GitHub Actions Setup Guide

This guide explains how to set up the GitHub Actions workflows for automated CI/CD, testing, and releases.

## Quick Setup

Since GitHub Apps cannot directly create workflow files, you'll need to set them up manually:

```bash
# Run the setup script
./scripts/setup-github-actions.sh

# Commit and push the workflows
git add .github/workflows/
git commit -m "Add GitHub Actions workflows for CI/CD"
git push origin <your-branch-name>
```

## Manual Setup

If you prefer to set up manually:

1. **Create the workflows directory**:
   ```bash
   mkdir -p .github/workflows
   ```

2. **Copy the workflow files**:
   ```bash
   cp github-workflows/ci.yml .github/workflows/ci.yml
   cp github-workflows/release.yml .github/workflows/release.yml
   cp github-workflows/nightly.yml .github/workflows/nightly.yml
   ```

3. **Add and commit**:
   ```bash
   git add .github/workflows/
   git commit -m "Add GitHub Actions workflows"
   git push origin <branch-name>
   ```

## Workflow Overview

### 1. CI Workflow (`ci.yml`)
**Triggers**: Push/PR to main/develop branches

**Features**:
- Tests on Python 3.8-3.12
- Multi-platform testing (Linux, Windows, macOS)
- Code quality checks (ruff, black, mypy)
- Security scanning (bandit, safety)
- Test coverage reporting
- Package building and verification
- Documentation building

### 2. Release Workflow (`release.yml`)
**Triggers**: Git tags matching `v*` pattern

**Features**:
- Comprehensive testing on multiple platforms
- Automated version detection from git tags
- Python package building (wheel + source)
- Binary building for Linux, Windows, macOS
- PyPI publishing (with proper credentials)
- GitHub release creation with binaries
- Automatic release notes generation
- Post-release housekeeping

### 3. Nightly Workflow (`nightly.yml`)
**Triggers**: Daily at 2 AM UTC + manual dispatch

**Features**:
- Extended testing suite
- Performance benchmarking
- Memory usage testing
- Dependency auditing
- Code complexity analysis
- Failure notifications via GitHub issues

## Repository Configuration

### Required Secrets

Set these in your repository settings (`Settings > Secrets and variables > Actions`):

1. **PYPI_API_TOKEN** (Required for releases)
   - Create at https://pypi.org/manage/account/token/
   - Scope: Entire account or specific project

2. **CODECOV_TOKEN** (Optional)
   - For enhanced code coverage reporting
   - Get from https://codecov.io/

### Repository Settings

1. **Enable GitHub Actions**:
   - Go to `Settings > Actions > General`
   - Choose "Allow all actions and reusable workflows"

2. **Configure Environments** (Optional):
   - Go to `Settings > Environments`
   - Create `release` environment with protection rules

3. **Branch Protection** (Recommended):
   - Go to `Settings > Branches`
   - Add rule for `main` branch
   - Enable "Require status checks to pass before merging"
   - Select CI checks as required

## Git Tag-Based Releases

The system uses git tags for semantic versioning:

### Creating a Release

```bash
# Create and push a release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Or use the automated release script
./scripts/release.sh
```

### Tag Format

- **Release tags**: `v1.0.0`, `v2.1.3`, etc.
- **Pre-release tags**: `v1.0.0-alpha`, `v1.0.0-beta.1`, etc.
- **Development versions**: Automatically generated between releases

### Version Detection

The system automatically detects versions:
- **Tagged commits**: Clean version (e.g., `1.0.0`)
- **Between releases**: Development version (e.g., `1.0.1.dev3+g1234567`)
- **Dirty working tree**: Includes `.dirty` suffix

## Binary Releases

The release workflow automatically builds binaries for:
- **Linux**: `huehoppy-linux-x86_64`
- **Windows**: `huehoppy-windows-x86_64.exe`
- **macOS**: `huehoppy-macos-x86_64`

### Binary Features

- Single-file executables
- No Python installation required
- Bundled dependencies
- Cross-platform compatibility
- Automatic checksums (SHA256)

## Testing Strategy

### CI Testing Matrix

- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating systems**: Ubuntu, Windows, macOS
- **Reduced matrix**: Excludes older Python versions on Windows/macOS for speed

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: End-to-end workflow testing
3. **CLI Tests**: Command-line interface testing
4. **Security Tests**: Vulnerability scanning
5. **Performance Tests**: Benchmarking and profiling

### Coverage Requirements

- **Minimum coverage**: 85%
- **Reports**: HTML, XML, and terminal output
- **Upload**: Codecov integration for tracking

## Troubleshooting

### Common Issues

1. **Workflow permission errors**:
   - Check repository settings
   - Ensure proper secrets are configured
   - Verify branch protection rules

2. **PyPI upload failures**:
   - Verify PYPI_API_TOKEN is correct
   - Check package name availability
   - Ensure proper version format

3. **Binary build failures**:
   - Check PyInstaller configuration
   - Verify all dependencies are included
   - Check platform-specific issues

### Debugging

1. **Check workflow logs**:
   - Go to `Actions` tab in GitHub
   - Click on failed workflow
   - Examine step-by-step output

2. **Test locally**:
   ```bash
   # Run the same commands locally
   ./scripts/test.sh
   ./scripts/build.sh
   ./scripts/build-binaries.sh
   ```

3. **Validate workflows**:
   ```bash
   # Install act for local testing
   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   
   # Run workflows locally
   act -j test
   ```

## Security Considerations

1. **Secrets Management**:
   - Use repository secrets for sensitive data
   - Never commit API tokens or keys
   - Use environment-specific secrets

2. **Dependency Scanning**:
   - Automated security scans with bandit
   - Dependency vulnerability checks with safety
   - Regular dependency updates

3. **Code Signing** (Future enhancement):
   - Binary signing for distribution
   - Certificate management
   - Trust chain verification

## Maintenance

### Regular Tasks

1. **Update dependencies**:
   - Monitor security advisories
   - Update action versions
   - Test compatibility

2. **Monitor workflows**:
   - Check failure rates
   - Optimize build times
   - Update test matrix

3. **Review releases**:
   - Verify binary functionality
   - Check release notes
   - Monitor download statistics

### Workflow Updates

When updating workflows:

1. Test changes in a feature branch
2. Use `workflow_dispatch` for manual testing
3. Update documentation as needed
4. Coordinate with team members

## Support

For issues with the GitHub Actions setup:

1. Check the workflow logs first
2. Review this documentation
3. Create an issue with detailed information
4. Include relevant log excerpts

The workflows are designed to be robust and handle common failure scenarios gracefully. They provide comprehensive testing and automated releases while maintaining security and reliability.