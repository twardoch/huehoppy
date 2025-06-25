# huehoppy.algorithms.colortrans_lhm - Wrapper for LHM color transfer (colortrans)

import numpy as np
import sys
import os
import cv2 # For BGR <-> RGB conversion

# Attempt to add the submodule to sys.path for direct import.
try:
    HUEHOPPY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    SUBMODULE_DIR = os.path.join(HUEHOPPY_ROOT, "submodules", "colortrans")

    if SUBMODULE_DIR not in sys.path:
        sys.path.insert(0, SUBMODULE_DIR)

    import colortrans
except ImportError as e:
    print(f"Info: Could not import 'colortrans' submodule. LHM algorithm may not be available. Error: {e}")
    colortrans = None

from huehoppy.core.base_algorithm import ColorTransferAlgorithm

class ColortransLHM(ColorTransferAlgorithm):
    """
    Linear Histogram Matching (LHM) Color Transfer.

    Wraps the `transfer_lhm` method from the 'colortrans' library by dstein64.
    Based on: Hertzmann, Aaron. "Algorithms for Rendering in Artistic Styles." (2001).

    Dependencies (from colortrans):
    - numpy
    - pillow
    This wrapper also uses opencv-python for BGR<->RGB color space conversions.
    """

    def __init__(self):
        if colortrans is None:
            raise ImportError(
                "ColortransLHM algorithm requires 'colortrans' which could not be imported. "
                "Please ensure it is available and its dependencies (numpy, pillow) are installed."
            )
        # No instance needed as colortrans provides functions directly.

    def transfer(self, source_image: np.ndarray, target_image: np.ndarray) -> np.ndarray:
        """
        Applies LHM color transfer.

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
            raise ValueError("Input images must have 3 color channels.")

        # colortrans expects RGB (H, W, C) images. Our internal standard is BGR.
        source_rgb = cv2.cvtColor(source_image, cv2.COLOR_BGR2RGB)
        target_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)

        # colortrans functions: transfer_METHOD(content, reference)
        # content = image to change (our target)
        # reference = image to take colors from (our source)
        transferred_rgb = colortrans.transfer_lhm(content=target_rgb, reference=source_rgb)

        # Convert back to BGR
        transferred_bgr = cv2.cvtColor(transferred_rgb, cv2.COLOR_RGB2BGR)

        return transferred_bgr

    def __str__(self) -> str:
        return "LHM (colortrans)"

    def __repr__(self) -> str:
        return "<ColortransLHM Algorithm (via colortrans)>"
