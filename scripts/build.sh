#!/bin/bash
# Build script for huehoppy

set -e

echo "🏗️  Building huehoppy..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from the project root."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and build tools
echo "⬆️  Upgrading build tools..."
pip install --upgrade pip setuptools wheel build

# Install development dependencies
echo "📥 Installing development dependencies..."
pip install -e ".[dev]"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "🔨 Building package..."
python -m build

# Verify build
echo "✅ Build completed successfully!"
echo "📦 Built packages:"
ls -la dist/

echo "🎉 Build process complete!"