# huehoppy.core.base_algorithm - Base class for color transfer algorithms

from abc import ABC, abstractmethod
import numpy as np

class ColorTransferAlgorithm(ABC):
    """
    Abstract base class for color transfer algorithms.

    All specific algorithm implementations should inherit from this class
    and implement the `transfer` method.
    """

    @abstractmethod
    def transfer(self, source_image: np.ndarray, target_image: np.ndarray) -> np.ndarray:
        """
        Applies the color transfer from the source image to the target image.

        Args:
            source_image: The source image (as a NumPy ndarray) from which to take the color palette.
            target_image: The target image (as a NumPy ndarray) to which to apply the color palette.
                          It's assumed to be in BGR format if OpenCV is the primary image loader.

        Returns:
            A new image (as a NumPy ndarray) which is the target image with colors transferred
            from the source image. Expected to be in BGR format.
        """
        pass

    def __str__(self) -> str:
        """
        Returns the name of the algorithm (class name by default).
        """
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} Algorithm>"
