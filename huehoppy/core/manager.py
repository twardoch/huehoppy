"""Manager for discovering and loading color transfer algorithms."""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type

from loguru import logger

from .base import ColorTransferAlgorithm, AlgorithmError, DependencyError


class HueHoppyManager:
    """Manager for discovering and loading color transfer algorithms."""
    
    def __init__(self) -> None:
        """Initialize the manager and discover available algorithms."""
        self._algorithms: Dict[str, Type[ColorTransferAlgorithm]] = {}
        self._discover_algorithms()
    
    def _discover_algorithms(self) -> None:
        """Discover all available algorithms."""
        # Get the algorithms directory
        algorithms_dir = Path(__file__).parent.parent / "algorithms"
        
        if not algorithms_dir.exists():
            logger.warning(f"Algorithms directory not found: {algorithms_dir}")
            return
        
        # Search for algorithm modules
        for item in algorithms_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                self._load_algorithm(item.name)
    
    def _load_algorithm(self, algorithm_name: str) -> None:
        """Load a single algorithm by name."""
        try:
            module_name = f"huehoppy.algorithms.{algorithm_name}"
            module = importlib.import_module(module_name)
            
            # Look for algorithm class in the module
            algorithm_class = getattr(module, "Algorithm", None)
            if algorithm_class is None:
                # Try common naming patterns
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type) and
                        issubclass(attr, ColorTransferAlgorithm) and
                        attr is not ColorTransferAlgorithm
                    ):
                        algorithm_class = attr
                        break
            
            if algorithm_class is None:
                logger.warning(f"No algorithm class found in {module_name}")
                return
            
            # Check if dependencies are available
            if not algorithm_class.is_available():
                logger.warning(f"Algorithm {algorithm_name} dependencies not available")
                return
            
            # Register the algorithm
            self._algorithms[algorithm_name] = algorithm_class
            logger.info(f"Loaded algorithm: {algorithm_name}")
            
        except Exception as e:
            logger.warning(f"Failed to load algorithm {algorithm_name}: {e}")
    
    def get_available_algorithms(self) -> List[str]:
        """Get list of available algorithm names."""
        return sorted(self._algorithms.keys())
    
    def get_algorithm(self, name: str) -> ColorTransferAlgorithm:
        """Get an algorithm instance by name."""
        if name not in self._algorithms:
            raise AlgorithmError(f"Algorithm '{name}' not found")
        
        algorithm_class = self._algorithms[name]
        try:
            return algorithm_class()
        except Exception as e:
            raise AlgorithmError(f"Failed to create algorithm '{name}': {e}")
    
    def get_algorithm_metadata(self, name: str) -> Optional[object]:
        """Get metadata for an algorithm."""
        if name not in self._algorithms:
            return None
        
        algorithm_class = self._algorithms[name]
        try:
            return algorithm_class.get_metadata()
        except Exception as e:
            logger.warning(f"Failed to get metadata for {name}: {e}")
            return None
    
    def transfer(
        self, 
        algorithm_name: str, 
        source: 'np.ndarray', 
        reference: 'np.ndarray', 
        **kwargs
    ) -> 'np.ndarray':
        """
        Perform color transfer using specified algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to use
            source: Source image
            reference: Reference image
            **kwargs: Algorithm-specific parameters
            
        Returns:
            Transferred image
        """
        algorithm = self.get_algorithm(algorithm_name)
        return algorithm.transfer(source, reference, **kwargs)