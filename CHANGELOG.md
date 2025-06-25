# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project reset to initial state.
- `PLAN.md` (Attempt 2): Outlines the revised project plan for MVP refactoring.
- `TODO.md` (Attempt 2): Revised task checklist for the MVP refactoring.
- `CHANGELOG.md` (This file, Attempt 2).
- Core `huehoppy` library structure:
    - `huehoppy/` directory and `__init__.py`
    - `huehoppy/algorithms/` directory and `__init__.py`
    - `huehoppy/core/` directory and `__init__.py`
    - `huehoppy/utils/` directory and `__init__.py`
- `huehoppy/core/base_algorithm.py`: Added `ColorTransferAlgorithm` abstract base class.
- `huehoppy/algorithms/reinhard.py`: Added wrapper for Reinhard color transfer using `python-color-transfer` submodule.
- `huehoppy/algorithms/colortrans_lhm.py`: Added wrapper for LHM color transfer using `colortrans` submodule.
- `huehoppy/algorithms/colortrans_pccm.py`: Added wrapper for PCCM color transfer using `colortrans` submodule.
- `requirements.txt`: Created with core dependencies (`numpy`, `opencv-python`, `Pillow`) for MVP.
- `huehoppy/core/manager.py`: Implemented `AlgorithmManager` for discovering and loading algorithms.
- `huehoppy/utils/image_io.py`: Added `read_image_bgr` and `save_image_bgr` functions using OpenCV, establishing BGR as internal format.
- `huehoppy/core/pipeline.py`: Implemented basic `Pipeline` class for chaining algorithm steps.
- `huehoppy/cli.py`: Added CLI using `click` to list algorithms and run them.
- `requirements.txt`: Added `click>=8.0`.
- `README.md`: Updated with MVP scope, installation instructions, CLI and library usage examples.
- `huehoppy/tests/__init__.py` and `huehoppy/tests/test_mvp_functionality.py`: Added basic integration tests for algorithms and pipeline.

### Changed
- **Project Scope:** Decided to defer integration of `ColorTransferLib` for the MVP release to ensure stability and focus, due to its dependency complexity and previous integration challenges. MVP will focus on algorithms from `python-color-transfer` and `colortrans`.
- Installed `click` dependency.
- Installed core dependencies (`numpy`, `opencv-python`, `Pillow`) into the environment.
- Tested `AlgorithmManager`: Successfully discovers and loads implemented MVP algorithms (Reinhard, LHM, PCCM).
- **Testing**: All MVP integration tests for algorithms and pipeline passed.

### Removed
- N/A

### Removed
- All previous files created during the first attempt were removed due to repository reset.
- `work/` directory: Contained `pylutek.py` (out of scope for MVP), `imagecolortransfer_install` (informational script), and an empty `imagecolortransfer` directory.
- `2llm/` directory: Contained miscellaneous text files.
