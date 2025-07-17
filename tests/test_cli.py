"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner
import tempfile
import cv2
import numpy as np

from huehoppy.cli import main


class TestCLI:
    """Tests for command-line interface."""
    
    def test_main_help(self):
        """Test main help command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "huehoppy: Advanced Color Transfer Tool" in result.output
    
    def test_list_algorithms(self):
        """Test list-algorithms command."""
        runner = CliRunner()
        result = runner.invoke(main, ["list-algorithms"])
        assert result.exit_code == 0
        assert "Available Color Transfer Algorithms" in result.output
        assert "reinhard" in result.output.lower()
    
    def test_transfer_command_help(self):
        """Test transfer command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["transfer", "--help"])
        assert result.exit_code == 0
        assert "Perform color transfer between two images" in result.output
    
    def test_transfer_missing_files(self):
        """Test transfer with missing files."""
        runner = CliRunner()
        result = runner.invoke(main, [
            "transfer", 
            "nonexistent_source.jpg",
            "nonexistent_ref.jpg", 
            "output.jpg"
        ])
        assert result.exit_code != 0
    
    def test_transfer_success(self, sample_image_file, sample_reference_file, tmp_path):
        """Test successful color transfer."""
        output_path = tmp_path / "output.jpg"
        
        runner = CliRunner()
        result = runner.invoke(main, [
            "transfer",
            str(sample_image_file),
            str(sample_reference_file),
            str(output_path),
            "--algorithm", "reinhard"
        ])
        
        assert result.exit_code == 0
        assert output_path.exists()
        
        # Verify output image
        output_img = cv2.imread(str(output_path))
        assert output_img is not None
        assert output_img.shape[0] > 0
        assert output_img.shape[1] > 0
        assert output_img.shape[2] == 3
    
    def test_transfer_invalid_algorithm(self, sample_image_file, sample_reference_file, tmp_path):
        """Test transfer with invalid algorithm."""
        output_path = tmp_path / "output.jpg"
        
        runner = CliRunner()
        result = runner.invoke(main, [
            "transfer",
            str(sample_image_file),
            str(sample_reference_file),
            str(output_path),
            "--algorithm", "nonexistent_algorithm"
        ])
        
        assert result.exit_code != 0
        assert "not available" in result.output
    
    def test_verbose_flag(self, sample_image_file, sample_reference_file, tmp_path):
        """Test verbose flag."""
        output_path = tmp_path / "output.jpg"
        
        runner = CliRunner()
        result = runner.invoke(main, [
            "--verbose",
            "transfer",
            str(sample_image_file),
            str(sample_reference_file),
            str(output_path),
        ])
        
        assert result.exit_code == 0
        assert output_path.exists()
    
    def test_pipeline_command_help(self):
        """Test pipeline command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["pipeline", "--help"])
        assert result.exit_code == 0
        assert "Execute a color transfer pipeline" in result.output
    
    def test_pipeline_not_implemented(self, sample_image_file, sample_reference_file, tmp_path):
        """Test that pipeline is not yet implemented."""
        config_path = tmp_path / "config.json"
        output_path = tmp_path / "output.jpg"
        
        # Create dummy config file
        config_path.write_text('{"steps": []}')
        
        runner = CliRunner()
        result = runner.invoke(main, [
            "pipeline",
            str(config_path),
            str(sample_image_file),
            str(sample_reference_file),
            str(output_path),
        ])
        
        assert result.exit_code != 0
        assert "not yet implemented" in result.output