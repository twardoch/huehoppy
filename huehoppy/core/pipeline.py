"""Pipeline system for chaining color transfer algorithms."""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from loguru import logger

from .base import ColorTransferAlgorithm, AlgorithmError
from .manager import HueHoppyManager


class PipelineStep:
    """Represents a single step in a color transfer pipeline."""
    
    def __init__(self, algorithm_name: str, parameters: Optional[Dict[str, Any]] = None):
        """Initialize a pipeline step."""
        self.algorithm_name = algorithm_name
        self.parameters = parameters or {}
    
    def __repr__(self) -> str:
        return f"PipelineStep({self.algorithm_name}, {self.parameters})"


class Pipeline:
    """Pipeline for chaining multiple color transfer algorithms."""
    
    def __init__(self, manager: Optional[HueHoppyManager] = None):
        """Initialize the pipeline."""
        self.manager = manager or HueHoppyManager()
        self.steps: List[PipelineStep] = []
        self._results: List[np.ndarray] = []
    
    def add_step(self, algorithm_name: str, parameters: Optional[Dict[str, Any]] = None) -> 'Pipeline':
        """Add a step to the pipeline."""
        step = PipelineStep(algorithm_name, parameters)
        self.steps.append(step)
        return self
    
    def clear(self) -> 'Pipeline':
        """Clear all steps from the pipeline."""
        self.steps.clear()
        self._results.clear()
        return self
    
    def execute(
        self, 
        source: np.ndarray, 
        reference: np.ndarray, 
        save_intermediate: bool = False
    ) -> np.ndarray:
        """
        Execute the pipeline.
        
        Args:
            source: Source image
            reference: Reference image
            save_intermediate: Whether to save intermediate results
            
        Returns:
            Final processed image
        """
        if not self.steps:
            raise AlgorithmError("Pipeline is empty")
        
        current_image = source.copy()
        
        if save_intermediate:
            self._results = [current_image.copy()]
        
        for i, step in enumerate(self.steps):
            logger.info(f"Executing step {i+1}/{len(self.steps)}: {step.algorithm_name}")
            
            try:
                algorithm = self.manager.get_algorithm(step.algorithm_name)
                current_image = algorithm.transfer(
                    current_image, 
                    reference, 
                    **step.parameters
                )
                
                if save_intermediate:
                    self._results.append(current_image.copy())
                    
            except Exception as e:
                raise AlgorithmError(f"Step {i+1} failed: {e}")
        
        return current_image
    
    def get_intermediate_results(self) -> List[np.ndarray]:
        """Get intermediate results from the last execution."""
        return self._results.copy()
    
    def __len__(self) -> int:
        """Get the number of steps in the pipeline."""
        return len(self.steps)
    
    def __repr__(self) -> str:
        return f"Pipeline({len(self.steps)} steps)"