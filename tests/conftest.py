"""Pytest configuration and fixtures."""

import numpy as np
import pytest
import cv2
from pathlib import Path


@pytest.fixture
def sample_image():
    """Create a sample test image."""
    # Create a simple 100x100 RGB image with gradient
    height, width = 100, 100
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a gradient pattern
    for i in range(height):
        for j in range(width):
            image[i, j] = [i * 255 // height, j * 255 // width, 128]
    
    return image


@pytest.fixture
def sample_reference():
    """Create a sample reference image."""
    # Create a different 100x100 RGB image
    height, width = 100, 100
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a different pattern
    for i in range(height):
        for j in range(width):
            image[i, j] = [128, (i + j) * 255 // (height + width), 200]
    
    return image


@pytest.fixture
def temp_image_path(tmp_path):
    """Create a temporary image file path."""
    return tmp_path / "test_image.png"


@pytest.fixture
def sample_image_file(sample_image, temp_image_path):
    """Create a sample image file."""
    cv2.imwrite(str(temp_image_path), sample_image)
    return temp_image_path


@pytest.fixture
def sample_reference_file(sample_reference, tmp_path):
    """Create a sample reference image file."""
    ref_path = tmp_path / "reference.png"
    cv2.imwrite(str(ref_path), sample_reference)
    return ref_path