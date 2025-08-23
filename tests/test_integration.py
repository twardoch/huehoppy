"""Integration tests for huehoppy."""

import numpy as np
import pytest
from pathlib import Path
import tempfile
import cv2

from huehoppy import HueHoppyManager, Pipeline
from huehoppy.core.base import AlgorithmError


class TestIntegration:
    """Integration tests for the entire system."""
    
    def test_end_to_end_workflow(self, sample_image, sample_reference):
        """Test complete end-to-end workflow."""
        # Initialize manager
        manager = HueHoppyManager()
        
        # Get available algorithms
        algorithms = manager.get_available_algorithms()
        assert len(algorithms) > 0
        
        # Perform transfer
        result = manager.transfer("reinhard", sample_image, sample_reference)
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
        
        # Test with different parameters
        result_with_params = manager.transfer(
            "reinhard", 
            sample_image, 
            sample_reference, 
            preserve_luminance=True
        )
        assert isinstance(result_with_params, np.ndarray)
        assert result_with_params.shape == sample_image.shape
        
        # Results should be different
        assert not np.array_equal(result, result_with_params)
    
    def test_pipeline_workflow(self, sample_image, sample_reference):
        """Test pipeline workflow."""
        # Create pipeline
        pipeline = Pipeline()
        pipeline.add_step("reinhard", {"preserve_luminance": False})
        pipeline.add_step("reinhard", {"preserve_luminance": True})
        
        # Execute pipeline
        result = pipeline.execute(sample_image, sample_reference, save_intermediate=True)
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
        
        # Check intermediate results
        intermediate = pipeline.get_intermediate_results()
        assert len(intermediate) == 3  # Original + 2 steps
        
        # All results should be different
        for i in range(len(intermediate) - 1):
            assert not np.array_equal(intermediate[i], intermediate[i + 1])
    
    def test_multiple_algorithms(self, sample_image, sample_reference):
        """Test with multiple algorithms if available."""
        manager = HueHoppyManager()
        algorithms = manager.get_available_algorithms()
        
        results = {}
        for algorithm_name in algorithms:
            result = manager.transfer(algorithm_name, sample_image, sample_reference)
            results[algorithm_name] = result
            
            # Basic sanity checks
            assert isinstance(result, np.ndarray)
            assert result.shape == sample_image.shape
            assert result.dtype == np.uint8
            assert np.all(result >= 0)
            assert np.all(result <= 255)
        
        # If multiple algorithms available, results should be different
        if len(algorithms) > 1:
            algorithm_names = list(algorithms)
            for i in range(len(algorithm_names) - 1):
                name1, name2 = algorithm_names[i], algorithm_names[i + 1]
                assert not np.array_equal(results[name1], results[name2])
    
    def test_error_handling(self, sample_image, sample_reference):
        """Test error handling in integration scenarios."""
        manager = HueHoppyManager()
        
        # Test with invalid algorithm
        with pytest.raises(AlgorithmError):
            manager.transfer("nonexistent", sample_image, sample_reference)
        
        # Test with invalid image shapes
        invalid_image = np.zeros((10, 10, 4), dtype=np.uint8)  # 4 channels
        # Should still work or handle gracefully
        try:
            result = manager.transfer("reinhard", invalid_image, sample_reference)
            assert isinstance(result, np.ndarray)
        except Exception as e:
            # Error should be informative
            assert len(str(e)) > 0
    
    def test_real_world_scenario(self, tmp_path):
        """Test with real-world-like scenario."""
        # Create more realistic test images
        height, width = 256, 256
        
        # Create a "photo-like" source image
        source = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                # Create a simple landscape-like pattern
                source[i, j] = [
                    min(255, 100 + i // 4),  # Blue sky gradient
                    min(255, 150 + j // 8),  # Green ground
                    min(255, 80 + (i + j) // 10)  # Mixed tones
                ]
        
        # Create a "reference style" image
        reference = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                # Create a warmer, more saturated pattern
                reference[i, j] = [
                    min(255, 50 + i // 6),   # Warmer blue
                    min(255, 200 + j // 12), # Vibrant green
                    min(255, 180 + (i + j) // 8)  # Warm highlights
                ]
        
        # Apply transfer
        manager = HueHoppyManager()
        result = manager.transfer("reinhard", source, reference)
        
        # Verify result properties
        assert isinstance(result, np.ndarray)
        assert result.shape == source.shape
        assert result.dtype == np.uint8
        
        # Result should be different from source
        assert not np.array_equal(result, source)
        
        # Save images for manual inspection if needed
        test_dir = tmp_path / "integration_test"
        test_dir.mkdir()
        
        cv2.imwrite(str(test_dir / "source.jpg"), source)
        cv2.imwrite(str(test_dir / "reference.jpg"), reference)
        cv2.imwrite(str(test_dir / "result.jpg"), result)
    
    def test_memory_efficiency(self, sample_image, sample_reference):
        """Test memory efficiency with larger images."""
        # Create larger images
        height, width = 512, 512
        large_source = cv2.resize(sample_image, (width, height))
        large_reference = cv2.resize(sample_reference, (width, height))
        
        manager = HueHoppyManager()
        
        # Should handle larger images without issues
        result = manager.transfer("reinhard", large_source, large_reference)
        assert isinstance(result, np.ndarray)
        assert result.shape == large_source.shape
        
        # Test with pipeline on larger images
        pipeline = Pipeline()
        pipeline.add_step("reinhard")
        
        result = pipeline.execute(large_source, large_reference)
        assert isinstance(result, np.ndarray)
        assert result.shape == large_source.shape
    
    def test_algorithm_metadata_integration(self):
        """Test that algorithm metadata is properly integrated."""
        manager = HueHoppyManager()
        algorithms = manager.get_available_algorithms()
        
        for algorithm_name in algorithms:
            metadata = manager.get_algorithm_metadata(algorithm_name)
            assert metadata is not None
            assert hasattr(metadata, 'name')
            assert hasattr(metadata, 'description')
            assert hasattr(metadata, 'author')
            assert hasattr(metadata, 'version')
            assert hasattr(metadata, 'supported_types')
            
            # All algorithms should support images
            assert "image" in metadata.supported_types