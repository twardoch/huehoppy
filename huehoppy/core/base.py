"""Base classes and interfaces for color transfer algorithms."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from pydantic import BaseModel, Field


@dataclass
class AlgorithmMetadata:
    """Metadata for a color transfer algorithm."""
    
    name: str
    description: str
    author: str
    paper: Optional[str] = None
    url: Optional[str] = None
    version: str = "1.0.0"
    supported_types: List[str] = Field(default_factory=lambda: ["image"])
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ColorTransferAlgorithm(ABC):
    """Abstract base class for all color transfer algorithms."""
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize the algorithm with optional parameters."""
        self.config = kwargs
        self._validate_config()
    
    @classmethod
    @abstractmethod
    def get_metadata(cls) -> AlgorithmMetadata:
        """Return algorithm metadata."""
        pass
    
    @abstractmethod
    def transfer(
        self, 
        source: np.ndarray, 
        reference: np.ndarray, 
        **kwargs: Any
    ) -> np.ndarray:
        """
        Perform color transfer from reference to source image.
        
        Args:
            source: Source image as numpy array (H, W, C)
            reference: Reference image as numpy array (H, W, C)
            **kwargs: Additional algorithm-specific parameters
            
        Returns:
            Transferred image as numpy array (H, W, C)
        """
        pass
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if algorithm dependencies are satisfied."""
        try:
            cls._check_dependencies()
            return True
        except ImportError:
            return False
    
    @classmethod
    def _check_dependencies(cls) -> None:
        """Check and import required dependencies. Override in subclasses."""
        pass
    
    def _validate_config(self) -> None:
        """Validate algorithm configuration. Override in subclasses."""
        pass
    
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess input image. Override in subclasses if needed."""
        return image
    
    def postprocess(self, image: np.ndarray) -> np.ndarray:
        """Postprocess output image. Override in subclasses if needed."""
        return np.clip(image, 0, 255).astype(np.uint8)


class HueHoppyError(Exception):
    """Base exception for huehoppy errors."""
    pass


class AlgorithmError(HueHoppyError):
    """Exception raised when an algorithm fails."""
    pass


class DependencyError(HueHoppyError):
    """Exception raised when required dependencies are missing."""
    pass