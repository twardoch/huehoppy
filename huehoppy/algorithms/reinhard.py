# huehoppy.algorithms.reinhard - Wrapper for Reinhard color transfer

import numpy as np
import sys
import os

# Attempt to add the submodule to sys.path for direct import.
# This is primarily for development convenience.
# A more robust solution involves proper packaging or vendoring.
try:
    # Assuming this script is in huehoppy/algorithms/
    # Path to the root of the huehoppy project: ../../
    # Path to submodules directory from project root: submodules/
    HUEHOPPY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    SUBMODULE_DIR = os.path.join(HUEHOPPY_ROOT, "submodules", "python-color-transfer")

    if SUBMODULE_DIR not in sys.path:
        sys.path.insert(0, SUBMODULE_DIR)

    from python_color_transfer.color_transfer import ColorTransfer as PCTColorTransfer
except ImportError as e:
    # This allows the module to be imported, but the algorithm will likely fail at runtime if deps are missing.
    # The AlgorithmManager (to be implemented) should ideally handle such cases gracefully.
    print(f"Info: Could not import 'python-color-transfer' submodule. Reinhard algorithm may not be available. Error: {e}")
    PCTColorTransfer = None

from huehoppy.core.base_algorithm import ColorTransferAlgorithm

class Reinhard(ColorTransferAlgorithm):
    """
    Reinhard Color Transfer.

    Wraps the "Lab mean transfer" method from the 'python-color-transfer' library
    by Pengbo-learn. This method is based on the paper:
    "Color Transfer between Images" by Reinhard, Ashikhmin, Gooch, and Shirley.

    Dependencies (from python-color-transfer):
    - opencv-python>=4.2
    - numpy>=1.19
    """

    def __init__(self):
        if PCTColorTransfer is None:
            raise ImportError(
                "Reinhard algorithm requires 'python-color-transfer' which could not be imported. "
                "Please ensure it is available and its dependencies (numpy, opencv-python) are installed."
            )
        self._transfer_instance = PCTColorTransfer()

    def transfer(self, source_image: np.ndarray, target_image: np.ndarray) -> np.ndarray:
        """
        Applies Reinhard color transfer.

        Args:
            source_image: The source image (NumPy BGR array).
            target_image: The target image (NumPy BGR array).

        Returns:
            The color-transferred target image (NumPy BGR array).
        """
        if not isinstance(source_image, np.ndarray) or not isinstance(target_image, np.ndarray):
            raise TypeError("Input images must be NumPy ndarrays.")
        if source_image.ndim != 3 or target_image.ndim != 3:
            raise ValueError("Input images must be 3-dimensional (height, width, channels).")
        if source_image.shape[2] != 3 or target_image.shape[2] != 3:
            raise ValueError("Input images must have 3 color channels (BGR).")

        # The python-color-transfer library's lab_transfer expects:
        # img_arr_in: image to be changed (our target)
        # img_arr_ref: reference image (our source)
        # It uses OpenCV internally, so BGR format is expected.
        transferred_image = self._transfer_instance.lab_transfer(
            img_arr_in=target_image,
            img_arr_ref=source_image
        )
        return transferred_image

    def __str__(self) -> str:
        return "Reinhard (python-color-transfer)"

    def __repr__(self) -> str:
        return "<Reinhard Algorithm (via python-color-transfer)>"
