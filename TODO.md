# huehoppy MVP - TODO List (Attempt 2)

- [X] **1. Initial Project Setup & Analysis (Again):**
    - [x] Create `PLAN.md`
    - [x] Create `TODO.md`
    - [x] Create `CHANGELOG.md`
    - [x] Re-analyze `README.md`
    - [x] List `submodules/`
    - [x] List `work/` and `2llm/`, decide on removal (Decision: Remove in Step 2)
    - [x] Verify submodule status

- [X] **2. Decision on `pylutek.py` and `imagecolortransfer_install`:**
    - [x] Re-read `work/pylutek.py` (Decision: Out of scope for MVP)
    - [x] Re-read `work/imagecolortransfer_install` (Decision: Informational, confirms CTL complexity)
    - [x] Confirm removal of `work/` (Decision: Yes, also `2llm/`)

- [X] **3. Core `huehoppy` Library Structure:**
    - [x] Create `huehoppy/` directory
    - [x] Create `huehoppy/algorithms/`
    - [x] Create `huehoppy/core/`
    - [x] Create `huehoppy/utils/`
    - [x] Add `__init__.py` files

- [X] **4. Algorithm Abstraction:**
    - [x] Define `ColorTransferAlgorithm` base class

- [X] **5. Wrapper for `python-color-transfer` (Reinhard):**
    - [x] Inspect submodule (Confirmed from previous attempt and README)
    - [x] Create `reinhard.py` wrapper
    - [x] Handle import & dependencies (sys.path modification and noted deps)

- [X] **6. Wrapper for `colortrans` (LHM, PCCM):**
    - [x] Inspect submodule (Confirmed from previous attempt and README)
    - [x] Create `colortrans_lhm.py` wrapper
    - [x] Create `colortrans_pccm.py` wrapper
    - [x] Handle BGR/RGB, import & dependencies (sys.path, cv2 conversions, noted deps)

- [X] **7. Re-evaluate `ColorTransferLib` Integration for MVP:**
    - [x] Briefly re-inspect submodule (Confirmed findings from previous attempt)
    - [x] Decide and document deferral for MVP (Decision: Deferred for stability and MVP focus)

- [X] **8. Dependency Management (MVP):** (Moved up from Step 12)
    - [x] Create top-level `requirements.txt` for `huehoppy`
    - [x] Install base dependencies (`numpy`, `opencv-python`, `Pillow`)

- [X] **9. Algorithm Manager:**
    - [x] Implement `AlgorithmManager` class in `huehoppy/core/manager.py`.
    - [x] Test `AlgorithmManager` discovery with installed dependencies (Successfully tested).
    - [x] Ensure graceful error handling for algorithm loading (Basic error handling tested as part of discovery).
    - [x] Provide methods to list available algorithms and retrieve a specific algorithm instance (Successfully tested).

- [X] **10. Image I/O Utilities & OpenCV Dependency:**
    - [x] Create utility functions in `huehoppy/utils/image_io.py`.
    - [x] Implement basic image read/write functions using OpenCV (`read_image_bgr`, `save_image_bgr`).
    - [x] Confirm BGR as the internal NumPy array format (Confirmed and implemented in I/O).

- [X] **11. Pipeline System (Basic):**
    - [x] Implement `Pipeline` class in `huehoppy/core/pipeline.py`.

- [X] **12. Basic Command-Line Interface (CLI):**
    - [x] Create `cli.py` using `click`.
    - [x] Allow listing and running of available MVP algorithms (Implemented and basic tests passed).
    - [x] Added `click` to `requirements.txt` and installed.

- [X] **13. Documentation and Examples (MVP):**
    - [x] Update `README.md` with MVP scope, install, and usage instructions.
    - [x] Add usage examples to `README.md` (CLI and library).
    - [x] Ensured algorithm wrappers have basic docstrings (Done during wrapper creation).

- [X] **14. Testing (MVP Focus):**
    - [x] AlgorithmManager test moved to step 9 and completed.
    - [x] Basic integration tests for each wrapped algorithm (Reinhard, LHM, PCCM) passed.
    - [x] Test a simple pipeline with 2 steps using available algorithms passed.
    - [x] Created `huehoppy/tests/test_mvp_functionality.py`.

- [X] **15. Refinement and Final Submission:**
    - [x] Code review (Self-review completed).
    - [x] Docs update (`PLAN.md`, `TODO.md`, `CHANGELOG.md` are up-to-date).
    - [ ] Submit the changes.
