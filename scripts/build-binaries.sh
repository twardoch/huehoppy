#!/bin/bash
# Binary building script for huehoppy

set -e

echo "🔧 Building huehoppy binaries..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from the project root."
    exit 1
fi

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    ARCH="x86_64"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
    ARCH="x86_64"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PLATFORM="windows"
    ARCH="x86_64"
else
    echo "❌ Error: Unsupported platform: $OSTYPE"
    exit 1
fi

echo "🖥️  Building for: $PLATFORM-$ARCH"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"
fi

# Install PyInstaller
echo "📦 Installing PyInstaller..."
pip install pyinstaller

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Create binary name
BINARY_NAME="huehoppy-$PLATFORM-$ARCH"
if [[ "$PLATFORM" == "windows" ]]; then
    BINARY_NAME="$BINARY_NAME.exe"
fi

# Build binary
echo "🔨 Building binary: $BINARY_NAME"
pyinstaller \
    --onefile \
    --name "$BINARY_NAME" \
    --add-data "huehoppy:huehoppy" \
    --hidden-import "huehoppy.core" \
    --hidden-import "huehoppy.core.base" \
    --hidden-import "huehoppy.core.manager" \
    --hidden-import "huehoppy.core.pipeline" \
    --hidden-import "huehoppy.algorithms" \
    --hidden-import "huehoppy.algorithms.reinhard" \
    --hidden-import "huehoppy.algorithms.reinhard.algorithm" \
    --exclude-module "matplotlib" \
    --exclude-module "tkinter" \
    --exclude-module "PyQt5" \
    --exclude-module "PyQt6" \
    --exclude-module "PySide2" \
    --exclude-module "PySide6" \
    --exclude-module "jupyter" \
    --exclude-module "notebook" \
    --exclude-module "ipython" \
    --exclude-module "pandas" \
    --exclude-module "scipy" \
    --exclude-module "sklearn" \
    --exclude-module "torch" \
    --exclude-module "tensorflow" \
    --strip \
    --upx-dir=/usr/bin \
    huehoppy/cli.py

# Test the binary
echo "🧪 Testing binary..."
if [ -f "dist/$BINARY_NAME" ]; then
    echo "✅ Binary built successfully: dist/$BINARY_NAME"
    
    # Make executable on Unix systems
    if [[ "$PLATFORM" != "windows" ]]; then
        chmod +x "dist/$BINARY_NAME"
    fi
    
    # Test basic functionality
    "./dist/$BINARY_NAME" --help
    "./dist/$BINARY_NAME" list-algorithms
    
    # Get binary size
    BINARY_SIZE=$(du -h "dist/$BINARY_NAME" | cut -f1)
    echo "📦 Binary size: $BINARY_SIZE"
    
    # Create checksum
    if command -v sha256sum &> /dev/null; then
        sha256sum "dist/$BINARY_NAME" > "dist/$BINARY_NAME.sha256"
        echo "🔒 SHA256 checksum created: dist/$BINARY_NAME.sha256"
    elif command -v shasum &> /dev/null; then
        shasum -a 256 "dist/$BINARY_NAME" > "dist/$BINARY_NAME.sha256"
        echo "🔒 SHA256 checksum created: dist/$BINARY_NAME.sha256"
    fi
    
else
    echo "❌ Error: Binary not found in dist/"
    exit 1
fi

echo "🎉 Binary build completed successfully!"
echo "📍 Binary location: dist/$BINARY_NAME"

# Show installation instructions
echo ""
echo "📋 Installation instructions:"
echo "   1. Copy the binary to a directory in your PATH"
echo "   2. Make it executable (Unix): chmod +x $BINARY_NAME"
echo "   3. Test: $BINARY_NAME --help"