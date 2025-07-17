#!/bin/bash
# Release script for huehoppy

set -e

echo "🚀 Preparing release for huehoppy..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from the project root."
    exit 1
fi

# Check if git is clean
if ! git diff-index --quiet HEAD --; then
    echo "❌ Error: Git working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Get current version from git tags
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "📋 Current version: $CURRENT_VERSION"

# Ask for new version
echo "🏷️  Enter new version (e.g., 1.0.0):"
read NEW_VERSION

# Validate version format
if ! echo "$NEW_VERSION" | grep -E "^[0-9]+\.[0-9]+\.[0-9]+$" > /dev/null; then
    echo "❌ Error: Invalid version format. Use semantic versioning (e.g., 1.0.0)."
    exit 1
fi

# Confirm release
echo "🔍 About to release version v$NEW_VERSION"
echo "⚠️  This will:"
echo "   - Run all tests"
echo "   - Build the package"
echo "   - Create a git tag"
echo "   - Push to remote"
echo "   - Upload to PyPI (if configured)"
echo ""
echo "Continue? (y/N)"
read -r CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "❌ Release cancelled."
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[dev,test]"
fi

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Build package
echo "🏗️  Building package..."
./scripts/build.sh

# Create git tag
echo "🏷️  Creating git tag v$NEW_VERSION..."
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

# Push tag to remote
echo "📤 Pushing tag to remote..."
git push origin "v$NEW_VERSION"

# Check if we should upload to PyPI
if [ -f ".pypirc" ] || [ -n "$PYPI_API_TOKEN" ]; then
    echo "📦 Uploading to PyPI..."
    pip install twine
    twine upload dist/*
    echo "✅ Package uploaded to PyPI!"
else
    echo "⚠️  PyPI credentials not found. Skipping upload."
    echo "   To upload manually, run: twine upload dist/*"
fi

# Update CHANGELOG
echo "📝 Updating CHANGELOG..."
if [ -f "CHANGELOG.md" ]; then
    # Add new version to changelog
    DATE=$(date '+%Y-%m-%d')
    sed -i "1 a\\
\\
## [v$NEW_VERSION] - $DATE\\
\\
### Added\\
- New release\\
" CHANGELOG.md
fi

# Create GitHub release (if gh CLI is available)
if command -v gh &> /dev/null; then
    echo "🐙 Creating GitHub release..."
    gh release create "v$NEW_VERSION" dist/* --title "Release v$NEW_VERSION" --generate-notes
    echo "✅ GitHub release created!"
else
    echo "⚠️  GitHub CLI not found. Create release manually at:"
    echo "   https://github.com/terragonlabs/huehoppy/releases/new"
fi

echo "🎉 Release v$NEW_VERSION completed successfully!"
echo "📦 Built packages are available in dist/"
echo "🏷️  Git tag: v$NEW_VERSION"
echo "📝 Don't forget to update the CHANGELOG.md with release notes"