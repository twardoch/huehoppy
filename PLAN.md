# Project Plan: huehoppy MVP (Attempt 2)

This document outlines the plan for refactoring the `huehoppy` project into a modular and extensible library for color transfer, focusing on an MVP (Minimum Viable Product). This is the second attempt after a repository reset.

1.  **Initial Project Setup & Analysis (Again):** (Current)
    *   Create `PLAN.md`, `TODO.md`, and `CHANGELOG.md`.
    *   Re-analyze `README.md` for project goals.
    *   List contents of `submodules/` to confirm their presence.
    *   List contents of `work/` and `2llm/` directories and decide on their removal (likely yes, as before).
    *   Verify submodule initialization status (`git submodule status`).

2.  **Decision on `pylutek.py` and `imagecolortransfer_install`:**
    *   Re-read `work/pylutek.py` and `work/imagecolortransfer_install`.
    *   Confirm the decision to remove the `work/` directory, understanding that `pylutek.py`'s functionality is out of scope for `huehoppy` MVP, and `imagecolortransfer_install` highlights `ColorTransferLib` complexities.

3.  **Core `huehoppy` Library Structure:**
    *   Create the `huehoppy` directory.
    *   Create `huehoppy/algorithms`, `huehoppy/core`, `huehoppy/utils` subdirectories.
    *   Add `__init__.py` files to make them packages.

4.  **Algorithm Abstraction:**
    *   Define the `ColorTransferAlgorithm` abstract base class in `huehoppy/core/base_algorithm.py`.

5.  **Wrapper for `python-color-transfer` (Reinhard):**
    *   Inspect `submodules/python-color-transfer` (README, requirements).
    *   Create the `huehoppy/algorithms/reinhard.py` wrapper.
    *   Handle submodule import (e.g., using `sys.path` temporarily, noting this for later dependency management).
    *   Note its dependencies (`numpy`, `opencv-python`).

6.  **Wrapper for `colortrans` (LHM, PCCM):**
    *   Inspect `submodules/colortrans` (README, setup.py/requirements).
    *   Create `huehoppy/algorithms/colortrans_lhm.py` and `huehoppy/algorithms/colortrans_pccm.py` wrappers.
    *   Handle BGR/RGB conversion if `colortrans` expects RGB.
    *   Note its dependencies (`numpy`, `pillow`).

7.  **Re-evaluate `ColorTransferLib` Integration for MVP:**
    *   Briefly re-inspect `submodules/ColorTransferLib/ColorTransferLib/Utils/Helper.py` and `ColorTransferLib/ColorTransfer.py` to confirm the list of available methods and complexity.
    *   **Make an early decision:** Given previous issues and the goal of a focused MVP, explicitly decide to defer `ColorTransferLib` wrapper implementation to post-MVP. The focus is on a working system with simpler integrations first.

8.  **Algorithm Manager:**
    *   Implement `AlgorithmManager` in `huehoppy/core/manager.py` to discover and load available algorithms (Reinhard, LHM, PCCM for MVP).
    *   Ensure graceful error handling for algorithm loading.

9.  **Image I/O Utilities & OpenCV Dependency:**
    *   Create `huehoppy/utils/image_io.py`.
    *   Implement basic image read/write functions using OpenCV (which will be a core dependency).
    *   Establish BGR as the internal NumPy array format for `huehoppy`.

10. **Pipeline System (Basic):**
    *   Implement a `Pipeline` class in `huehoppy/core/pipeline.py` for chaining algorithms.

11. **Basic Command-Line Interface (CLI):**
    *   Create `cli.py` using `click` or `argparse`.
    *   Allow listing and running of available MVP algorithms.

12. **Dependency Management (MVP):**
    *   Create a top-level `requirements.txt` for `huehoppy` including `numpy`, `opencv-python`, `Pillow`, and any CLI tool dependencies.
    *   Install these base dependencies in the environment early to facilitate testing of wrappers.

13. **Documentation and Examples (MVP):**
    *   Update `README.md` for the `huehoppy` MVP.
    *   Provide usage examples for the included algorithms.

14. **Testing (MVP Focus):**
    *   Basic integration tests for `AlgorithmManager`, each wrapped algorithm, and a simple pipeline.

15. **Refinement and Final Submission:**
    *   Code review, update documentation, and submit.
