#!/bin/bash
# Test script for huehoppy

set -e

echo "🧪 Testing huehoppy..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from the project root."
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

# Install test dependencies if not already installed
echo "📥 Installing test dependencies..."
pip install -e ".[test]"

# Run linting
echo "🔍 Running linting checks..."
echo "  - Running ruff..."
ruff check huehoppy tests
echo "  - Running black..."
black --check huehoppy tests

# Run type checking
echo "🔍 Running type checking..."
mypy huehoppy

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --cov=huehoppy --cov-report=term-missing --cov-report=html

# Run integration tests
echo "🔗 Running integration tests..."
pytest tests/test_integration.py -v -s

# Test CLI
echo "🖥️  Testing CLI..."
huehoppy --help
huehoppy list-algorithms

echo "✅ All tests passed!"
echo "📊 Coverage report generated in htmlcov/"
echo "🎉 Test process complete!"