"""Core components for huehoppy color transfer framework."""

from .base import ColorTransferAlgorithm, AlgorithmMetadata
from .manager import HueHoppyManager
from .pipeline import Pipeline

__all__ = [
    "ColorTransferAlgorithm",
    "AlgorithmMetadata", 
    "HueHoppyManager",
    "Pipeline",
]