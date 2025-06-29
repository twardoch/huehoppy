# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-06-29

### Recent Changes

#### 2025-06-26
- **Updated submodules**: Updated ColorTransferLib and colortrans to their latest versions

#### 2025-06-25  
- **Work improvements**: Enhanced imagecolortransfer script with better installation handling
- **pylutek.py updates**: Improved path handling and validation in pylutek.py script

#### 2025-01-25
- **New pylutek.py script**: Added comprehensive video and LUT processing script with:
  - Configuration management using Pydantic models
  - Video processing capabilities with color matching
  - LUT generation and application
  - Error handling and progress tracking
  - Support for multiple source-target image pairs

#### 2025-01-19
- **README update**: Clarified project vision and future architecture plans for huehoppy
- **Defined project goals**: 
  - Independent algorithm loading with graceful failure handling
  - Clean, consistent API across all algorithms
  - Pipeline system for chaining algorithms
  - Separated I/O from core algorithm logic
  - Optional dependency installation

### Project Status

The project is currently in a transitional phase, using existing color transfer libraries (ColorTransferLib, python-color-transfer, colortrans) as temporary implementations while working towards a new unified architecture.

### Known Issues

- ColorTransferLib fails completely if any dependency is missing
- Limited modularity in simpler libraries (python-color-transfer, colortrans)
- Difficulty chaining multiple algorithms together
- Mixed code organization across different submodules