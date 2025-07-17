"""Tests for core huehoppy functionality."""

import numpy as np
import pytest

from huehoppy.core.base import ColorTransferAlgorithm, AlgorithmMetadata
from huehoppy.core.manager import HueHoppyManager
from huehoppy.core.pipeline import Pipeline, PipelineStep


class TestColorTransferAlgorithm:
    """Tests for ColorTransferAlgorithm base class."""
    
    def test_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError."""
        with pytest.raises(TypeError):
            ColorTransferAlgorithm()
    
    def test_algorithm_metadata(self):
        """Test AlgorithmMetadata creation."""
        metadata = AlgorithmMetadata(
            name="Test Algorithm",
            description="A test algorithm",
            author="Test Author",
            version="1.0.0"
        )
        assert metadata.name == "Test Algorithm"
        assert metadata.description == "A test algorithm"
        assert metadata.author == "Test Author"
        assert metadata.version == "1.0.0"
        assert metadata.supported_types == ["image"]


class TestHueHoppyManager:
    """Tests for HueHoppyManager."""
    
    def test_manager_initialization(self):
        """Test manager initialization."""
        manager = HueHoppyManager()
        assert isinstance(manager, HueHoppyManager)
    
    def test_get_available_algorithms(self):
        """Test getting available algorithms."""
        manager = HueHoppyManager()
        algorithms = manager.get_available_algorithms()
        assert isinstance(algorithms, list)
        # Should contain at least the reinhard algorithm
        assert "reinhard" in algorithms
    
    def test_get_algorithm(self):
        """Test getting algorithm instance."""
        manager = HueHoppyManager()
        algorithm = manager.get_algorithm("reinhard")
        assert isinstance(algorithm, ColorTransferAlgorithm)
    
    def test_get_nonexistent_algorithm(self):
        """Test getting non-existent algorithm."""
        manager = HueHoppyManager()
        with pytest.raises(Exception):
            manager.get_algorithm("nonexistent")
    
    def test_transfer_method(self, sample_image, sample_reference):
        """Test the transfer method."""
        manager = HueHoppyManager()
        result = manager.transfer("reinhard", sample_image, sample_reference)
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape


class TestPipeline:
    """Tests for Pipeline class."""
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        pipeline = Pipeline()
        assert len(pipeline) == 0
        assert isinstance(pipeline.steps, list)
    
    def test_add_step(self):
        """Test adding steps to pipeline."""
        pipeline = Pipeline()
        pipeline.add_step("reinhard", {"preserve_luminance": True})
        assert len(pipeline) == 1
        assert pipeline.steps[0].algorithm_name == "reinhard"
        assert pipeline.steps[0].parameters == {"preserve_luminance": True}
    
    def test_clear_pipeline(self):
        """Test clearing pipeline."""
        pipeline = Pipeline()
        pipeline.add_step("reinhard")
        pipeline.add_step("reinhard")
        assert len(pipeline) == 2
        
        pipeline.clear()
        assert len(pipeline) == 0
    
    def test_empty_pipeline_execution(self, sample_image, sample_reference):
        """Test executing empty pipeline."""
        pipeline = Pipeline()
        with pytest.raises(Exception):
            pipeline.execute(sample_image, sample_reference)
    
    def test_single_step_execution(self, sample_image, sample_reference):
        """Test executing single step pipeline."""
        pipeline = Pipeline()
        pipeline.add_step("reinhard")
        
        result = pipeline.execute(sample_image, sample_reference)
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
    
    def test_multiple_step_execution(self, sample_image, sample_reference):
        """Test executing multi-step pipeline."""
        pipeline = Pipeline()
        pipeline.add_step("reinhard", {"preserve_luminance": False})
        pipeline.add_step("reinhard", {"preserve_luminance": True})
        
        result = pipeline.execute(sample_image, sample_reference)
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape
    
    def test_intermediate_results(self, sample_image, sample_reference):
        """Test saving intermediate results."""
        pipeline = Pipeline()
        pipeline.add_step("reinhard")
        pipeline.add_step("reinhard")
        
        result = pipeline.execute(sample_image, sample_reference, save_intermediate=True)
        intermediate = pipeline.get_intermediate_results()
        
        assert len(intermediate) == 3  # Original + 2 steps
        assert all(isinstance(img, np.ndarray) for img in intermediate)


class TestPipelineStep:
    """Tests for PipelineStep class."""
    
    def test_step_creation(self):
        """Test creating a pipeline step."""
        step = PipelineStep("reinhard", {"preserve_luminance": True})
        assert step.algorithm_name == "reinhard"
        assert step.parameters == {"preserve_luminance": True}
    
    def test_step_no_parameters(self):
        """Test creating step without parameters."""
        step = PipelineStep("reinhard")
        assert step.algorithm_name == "reinhard"
        assert step.parameters == {}
    
    def test_step_repr(self):
        """Test step string representation."""
        step = PipelineStep("reinhard", {"test": True})
        repr_str = repr(step)
        assert "reinhard" in repr_str
        assert "test" in repr_str