"""Tests for color transfer algorithms."""

import numpy as np
import pytest

from huehoppy.algorithms.reinhard import Algorithm as ReinhardAlgorithm
from huehoppy.core.base import AlgorithmMetadata


class TestReinhardAlgorithm:
    """Tests for Reinhard algorithm."""
    
    def test_algorithm_creation(self):
        """Test creating Reinhard algorithm instance."""
        algorithm = ReinhardAlgorithm()
        assert isinstance(algorithm, ReinhardAlgorithm)
    
    def test_algorithm_metadata(self):
        """Test Reinhard algorithm metadata."""
        metadata = ReinhardAlgorithm.get_metadata()
        assert isinstance(metadata, AlgorithmMetadata)
        assert metadata.name == "Reinhard"
        assert "Reinhard" in metadata.author
        assert "2001" in metadata.paper
        assert metadata.supported_types == ["image"]
    
    def test_algorithm_availability(self):
        """Test that algorithm is available."""
        assert ReinhardAlgorithm.is_available() is True
    
    def test_dependencies_check(self):
        """Test dependencies check."""
        # Should not raise exception
        ReinhardAlgorithm._check_dependencies()
    
    def test_basic_transfer(self, sample_image, sample_reference):
        """Test basic color transfer."""
        algorithm = ReinhardAlgorithm()
        result = algorithm.transfer(sample_image, sample_reference)
        
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
        assert result.dtype == np.uint8
        assert np.all(result >= 0)
        assert np.all(result <= 255)
    
    def test_transfer_with_luminance_preservation(self, sample_image, sample_reference):
        """Test color transfer with luminance preservation."""
        algorithm = ReinhardAlgorithm()
        result = algorithm.transfer(sample_image, sample_reference, preserve_luminance=True)
        
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
        assert result.dtype == np.uint8
    
    def test_transfer_different_sizes(self):
        """Test transfer with different image sizes."""
        algorithm = ReinhardAlgorithm()
        
        # Create images of different sizes
        small_img = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        large_img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        
        result = algorithm.transfer(small_img, large_img)
        assert result.shape == small_img.shape
        
        result = algorithm.transfer(large_img, small_img)
        assert result.shape == large_img.shape
    
    def test_transfer_edge_cases(self):
        """Test transfer with edge cases."""
        algorithm = ReinhardAlgorithm()
        
        # Test with uniform color images
        uniform_img = np.full((100, 100, 3), 128, dtype=np.uint8)
        result = algorithm.transfer(uniform_img, uniform_img)
        assert isinstance(result, np.ndarray)
        
        # Test with extreme values
        black_img = np.zeros((100, 100, 3), dtype=np.uint8)
        white_img = np.full((100, 100, 3), 255, dtype=np.uint8)
        result = algorithm.transfer(black_img, white_img)
        assert isinstance(result, np.ndarray)
    
    def test_algorithm_parameters(self):
        """Test algorithm parameter handling."""
        algorithm = ReinhardAlgorithm()
        metadata = algorithm.get_metadata()
        
        # Check that parameters are documented
        assert "preserve_luminance" in metadata.parameters
        param_info = metadata.parameters["preserve_luminance"]
        assert param_info["type"] == "bool"
        assert param_info["default"] is False
    
    def test_preprocess_postprocess(self, sample_image):
        """Test preprocessing and postprocessing."""
        algorithm = ReinhardAlgorithm()
        
        # Test preprocessing (should be identity by default)
        preprocessed = algorithm.preprocess(sample_image)
        assert np.array_equal(preprocessed, sample_image)
        
        # Test postprocessing (should clip and convert to uint8)
        test_array = np.array([[-10, 128, 300]], dtype=np.float32)
        postprocessed = algorithm.postprocess(test_array)
        assert np.array_equal(postprocessed, [[0, 128, 255]])
        assert postprocessed.dtype == np.uint8