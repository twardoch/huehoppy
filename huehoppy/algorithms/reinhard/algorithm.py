"""
Reinhard et al. color transfer algorithm implementation.

Based on: "Color Transfer between Images" by Reinhard et al. (2001)
"""

import numpy as np
import cv2
from typing import Any

from huehoppy.core.base import ColorTransferAlgorithm, AlgorithmMetadata


class Algorithm(ColorTransferAlgorithm):
    """Reinhard et al. color transfer algorithm."""
    
    @classmethod
    def get_metadata(cls) -> AlgorithmMetadata:
        """Return algorithm metadata."""
        return AlgorithmMetadata(
            name="Reinhard",
            description="Color transfer using mean and standard deviation matching in Lab color space",
            author="Reinhard et al.",
            paper="Color Transfer between Images (2001)",
            version="1.0.0",
            supported_types=["image"],
            parameters={
                "preserve_luminance": {
                    "type": "bool",
                    "default": False,
                    "description": "Whether to preserve luminance channel"
                }
            }
        )
    
    @classmethod
    def _check_dependencies(cls) -> None:
        """Check required dependencies."""
        import cv2
        import numpy as np
    
    def transfer(
        self, 
        source: np.ndarray, 
        reference: np.ndarray, 
        preserve_luminance: bool = False,
        **kwargs: Any
    ) -> np.ndarray:
        """
        Perform color transfer using Reinhard et al. method.
        
        Args:
            source: Source image in BGR format
            reference: Reference image in BGR format
            preserve_luminance: Whether to preserve luminance
            **kwargs: Additional parameters (ignored)
            
        Returns:
            Transferred image in BGR format
        """
        # Convert to Lab color space
        source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype(np.float32)
        reference_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB).astype(np.float32)
        
        # Calculate statistics
        source_mean = np.mean(source_lab, axis=(0, 1))
        source_std = np.std(source_lab, axis=(0, 1))
        reference_mean = np.mean(reference_lab, axis=(0, 1))
        reference_std = np.std(reference_lab, axis=(0, 1))
        
        # Avoid division by zero
        source_std = np.maximum(source_std, 1e-8)
        
        # Apply color transfer
        result_lab = source_lab.copy()
        
        if preserve_luminance:
            # Only transfer a and b channels
            for i in range(1, 3):
                result_lab[:, :, i] = (
                    (source_lab[:, :, i] - source_mean[i]) * 
                    (reference_std[i] / source_std[i]) + 
                    reference_mean[i]
                )
        else:
            # Transfer all channels
            for i in range(3):
                result_lab[:, :, i] = (
                    (source_lab[:, :, i] - source_mean[i]) * 
                    (reference_std[i] / source_std[i]) + 
                    reference_mean[i]
                )
        
        # Clip values to valid range
        result_lab = np.clip(result_lab, 0, 255)
        
        # Convert back to BGR
        result = cv2.cvtColor(result_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
        return result