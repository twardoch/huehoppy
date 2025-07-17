#!/bin/bash
# Development setup script for huehoppy

set -e

echo "🛠️  Setting up development environment for huehoppy..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from the project root."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install package in development mode with all dependencies
echo "📥 Installing huehoppy in development mode..."
pip install -e ".[dev,test,docs,all]"

# Install pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p docs/
mkdir -p examples/
mkdir -p .github/workflows/

# Run initial tests to verify setup
echo "🧪 Running initial tests..."
python -m pytest tests/ -v --tb=short -x

# Check CLI
echo "🖥️  Testing CLI..."
huehoppy --help

echo "✅ Development environment setup complete!"
echo ""
echo "🎉 You're ready to develop huehoppy!"
echo ""
echo "📋 Next steps:"
echo "   - Activate environment: source venv/bin/activate"
echo "   - Run tests: ./scripts/test.sh"
echo "   - Build package: ./scripts/build.sh"
echo "   - Create release: ./scripts/release.sh"
echo ""
echo "🔧 Available commands:"
echo "   - huehoppy --help"
echo "   - huehoppy list-algorithms"
echo "   - huehoppy transfer source.jpg ref.jpg output.jpg"