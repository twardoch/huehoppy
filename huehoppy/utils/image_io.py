# huehoppy.utils.image_io - Image input/output utilities

import cv2
import numpy as np
from pathlib import Path
import os # Added for os.path.exists

class ImageIOError(IOError):
    """Custom exception for image I/O errors."""
    pass

def read_image_bgr(image_path: str | Path) -> np.ndarray:
    """
    Reads an image from the given path using OpenCV.

    Args:
        image_path: Path to the image file.

    Returns:
        A NumPy ndarray representing the image in BGR format.

    Raises:
        ImageIOError: If the image cannot be read or is invalid.
    """
    if not isinstance(image_path, (str, Path)):
        raise TypeError("image_path must be a string or Path object.")

    img_path_str = str(image_path)
    if not os.path.exists(img_path_str):
        raise ImageIOError(f"Image file not found at path: {img_path_str}")

    image = cv2.imread(img_path_str)

    if image is None:
        raise ImageIOError(f"Failed to read image from path: {img_path_str}. File might be corrupted or an unsupported format.")

    if image.ndim != 3 or image.shape[2] != 3:
        # This could be a grayscale image or something else.
        # Forcing color for now, or could raise a more specific error.
        # If grayscale, it might be read as (H, W) or (H, W, 1) depending on flags.
        # cv2.imread by default loads as BGR if color.
        # For simplicity, huehoppy currently expects 3-channel BGR images.
        raise ImageIOError(f"Image at {img_path_str} is not a 3-channel image. Loaded shape: {image.shape}")

    return image

def save_image_bgr(image_path: str | Path, image: np.ndarray) -> None:
    """
    Saves a NumPy ndarray (BGR format) as an image file using OpenCV.

    Args:
        image_path: Path where the image will be saved.
        image: NumPy ndarray representing the image in BGR format.

    Raises:
        ImageIOError: If the image cannot be saved or the input is invalid.
        TypeError: If input arguments are of incorrect types.
    """
    if not isinstance(image_path, (str, Path)):
        raise TypeError("image_path must be a string or Path object.")
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a NumPy ndarray.")

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Image to save must be a 3-channel BGR NumPy ndarray.")
    if image.dtype != np.uint8:
        print(f"Warning: Image data type is {image.dtype}, not uint8. OpenCV imwrite expects uint8 for most formats. Clamping and conversion will occur if values are out of [0, 255] range or float.")
        # Potentially add auto-conversion/clipping here if desired, e.g.:
        # if image.dtype != np.uint8:
        #     image = np.clip(image, 0, 255).astype(np.uint8) if image.max() > 1 else (image * 255).clip(0,255).astype(np.uint8)


    # Ensure parent directory exists
    parent_dir = Path(image_path).parent
    if not parent_dir.exists():
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ImageIOError(f"Could not create directory {parent_dir} for saving image: {e}")

    try:
        success = cv2.imwrite(str(image_path), image)
        if not success:
            raise ImageIOError(f"Failed to save image to path: {image_path}. OpenCV returned failure, possibly due to an invalid path or format extension.")
    except Exception as e: # Catch cv2 errors which might not be specific cv2.error
        raise ImageIOError(f"An error occurred while saving image to {image_path}: {e}")
