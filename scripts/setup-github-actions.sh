#!/bin/bash
# Setup GitHub Actions workflows

set -e

echo "🔧 Setting up GitHub Actions workflows..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from the project root."
    exit 1
fi

# Create .github/workflows directory
echo "📁 Creating .github/workflows directory..."
mkdir -p .github/workflows

# Copy workflow files
echo "📄 Copying workflow files..."
cp github-workflows/ci.yml .github/workflows/ci.yml
cp github-workflows/release.yml .github/workflows/release.yml
cp github-workflows/nightly.yml .github/workflows/nightly.yml

# Verify files were copied
echo "✅ Workflow files copied:"
ls -la .github/workflows/

# Add to git
echo "📝 Adding workflows to git..."
git add .github/workflows/

echo "🎉 GitHub Actions workflows setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Commit and push the workflow files:"
echo "   git commit -m 'Add GitHub Actions workflows'"
echo "   git push origin <branch-name>"
echo ""
echo "2. Configure repository secrets:"
echo "   - PYPI_API_TOKEN: For PyPI publishing"
echo "   - CODECOV_TOKEN: For code coverage (optional)"
echo ""
echo "3. Enable GitHub Actions in your repository settings"
echo ""
echo "4. Create your first release:"
echo "   git tag -a v0.1.0 -m 'Initial release'"
echo "   git push origin v0.1.0"
echo ""
echo "🔍 Workflow files are now ready in .github/workflows/"
echo "   - ci.yml: Continuous Integration"
echo "   - release.yml: Release automation"
echo "   - nightly.yml: Nightly testing"