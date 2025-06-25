#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["opencv-python", "fire", "loguru", "pydantic", "rich", "numpy"]
# ///
# this_file: /Users/adam/bin/pylutek

import os
import subprocess
import time
from pathlib import Path
from typing import TypeAlias, Union

import cv2
import numpy as np
from fire import Fire
from loguru import logger
from pydantic import BaseModel, field_validator
from rich.console import Console
from rich.progress import track

# Type aliases for clarity
NDArray: TypeAlias = np.ndarray
PathLike: TypeAlias = Union[str, Path]
console = Console()


class PylutekError(Exception):
    """Base exception for Pylutek errors."""


class VideoProcessingError(PylutekError):
    """Raised when video processing fails."""


class ImageProcessingError(PylutekError):
    """Raised when image processing fails."""


class ProcessingConfig(BaseModel):
    """Configuration for video and LUT processing."""

    source_target_pairs: list[tuple[Path, Path]]
    input_video: Path | None = None
    output_video: Path | None = None
    lut_path: Path | None = None
    quick: bool = False

    @field_validator("output_video", mode="before")
    @classmethod
    def set_default_output(cls, v: PathLike | None, info) -> Path | None:
        if not v and "input_video" in info.data and info.data["input_video"]:
            input_path = Path(info.data["input_video"])
            lut_path = info.data.get("lut_path")
            if lut_path:
                # Use LUT stem for output video name
                return input_path.with_stem(f"{input_path.stem}--{Path(lut_path).stem}")
            else:
                # Default fallback
                return input_path.with_stem(f"{input_path.stem}_matched")
        return Path(v) if v else None

    @field_validator("lut_path", mode="before")
    @classmethod
    def set_default_lut(cls, v: PathLike | None, info) -> Path | None:
        if (
            not v
            and "source_target_pairs" in info.data
            and info.data["source_target_pairs"]
        ):
            # Use first source-target pair for naming
            first_source, first_target = info.data["source_target_pairs"][0]
            source_stem = Path(first_source).stem
            target_stem = Path(first_target).stem
            return Path(f"{source_stem}--{target_stem}.cube")
        return Path(v) if v else None

    @field_validator("*")
    @classmethod
    def validate_paths(
        cls, v: PathLike | None | list[tuple[PathLike, PathLike]], info
    ) -> Path | None | list[tuple[Path, Path]]:
        """Convert all path-like fields to Path objects."""
        if isinstance(v, (str, Path)):
            return Path(v) if v else None
        elif isinstance(v, list):
            return [(Path(s), Path(t)) for s, t in v]
        return v

    model_config = {
        "arbitrary_types_allowed": True,
    }


def read_image(path: Path) -> NDArray:
    """Read an image file and convert to BGR format."""
    img = cv2.imread(str(path))
    if img is None:
        raise ImageProcessingError(f"Could not read image: {path}")
    return img


def calculate_stats(lab_img: NDArray) -> tuple[NDArray, NDArray]:
    """Calculate mean and standard deviation of Lab image."""
    mean = np.mean(lab_img, axis=(0, 1))
    std = np.std(lab_img, axis=(0, 1))
    return mean, std


def create_multi_lut(config: ProcessingConfig, verbose: bool = False) -> Path:
    """Create a LUT from source-target pairs using direct or weighted averaging."""
    try:
        size = 32
        final_grid = np.zeros((size, size, size, 3), dtype=np.float32)

        # For single pair, use direct mapping without weighting
        is_single_pair = len(config.source_target_pairs) == 1
        if is_single_pair:
            source_path, target_path = config.source_target_pairs[0]
            source = read_image(source_path)
            target = read_image(target_path)

            source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
            target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)

            source_mean, source_std = calculate_stats(source_lab)
            target_mean, target_std = calculate_stats(target_lab)

            # Create direct mapping grid
            for b in range(size):
                for g in range(size):
                    for r in range(size):
                        rgb = np.array([r, g, b]) * (255.0 / (size - 1))
                        bgr = rgb[::-1]
                        lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0, 0]

                        # Direct color transfer without weighting
                        matched_lab = (
                            (lab - source_mean) * (target_std / source_std)
                        ) + target_mean
                        matched_lab = np.clip(matched_lab, 0, 255)

                        matched_bgr = cv2.cvtColor(
                            np.uint8([[matched_lab]]), cv2.COLOR_LAB2BGR
                        )[0, 0]
                        final_grid[b, g, r] = matched_bgr[::-1] / 255.0
        else:
            # Multiple pairs - use weighted averaging
            weight_sum = np.zeros((size, size, size), dtype=np.float32)
            pairs_iter = (
                track(
                    config.source_target_pairs,
                    description="Processing image pairs",
                )
                if verbose
                else config.source_target_pairs
            )
            for source_path, target_path in pairs_iter:
                source = read_image(source_path)
                target = read_image(target_path)

                source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
                target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)

                source_mean, source_std = calculate_stats(source_lab)
                target_mean, target_std = calculate_stats(target_lab)

                for b in range(size):
                    for g in range(size):
                        for r in range(size):
                            rgb = np.array([r, g, b]) * (255.0 / (size - 1))
                            bgr = rgb[::-1]
                            lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[
                                0, 0
                            ]

                            similarity = np.exp(
                                -np.sum((lab - source_mean) ** 2)
                                / (4 * np.sum(source_std**2))
                            )

                            matched_lab = (
                                (lab - source_mean) * (target_std / source_std)
                            ) + target_mean
                            matched_lab = np.clip(matched_lab, 0, 255)

                            matched_bgr = cv2.cvtColor(
                                np.uint8([[matched_lab]]), cv2.COLOR_LAB2BGR
                            )[0, 0]

                            final_grid[b, g, r] += matched_bgr[::-1] * similarity
                            weight_sum[b, g, r] += similarity

            # Normalize by total weights
            weight_sum = np.maximum(weight_sum, 1e-6)[:, :, :, np.newaxis]
            final_grid = final_grid / weight_sum

        # Ensure output is in valid range [0, 1]
        final_grid = np.clip(final_grid, 0, 1)

        # Save combined LUT
        if config.lut_path is None:
            raise ImageProcessingError("LUT path is not set")

        with open(config.lut_path, "w") as f:
            f.write(f"LUT_3D_SIZE {size}\n")
            for b in range(size):
                for g in range(size):
                    for r in range(size):
                        rgb = final_grid[b, g, r]
                        f.write(f"{rgb[0]:.6f} {rgb[1]:.6f} {rgb[2]:.6f}\n")

        return config.lut_path

    except Exception as e:
        raise ImageProcessingError(f"Failed to create LUT: {str(e)}") from e


def process_video(config: ProcessingConfig, verbose: bool = False) -> None:
    """Process a video using the created LUT."""
    try:
        if not config.input_video or not config.output_video:
            raise ValueError("Input and output video paths must be set")

        ffmpeg_loglevel = "info" if verbose else "warning"
        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel",
            ffmpeg_loglevel,
            "-threads",
            str(os.cpu_count()),
            "-i",
            str(config.input_video),
            "-vf",
            f"lut3d={config.lut_path},format=yuv420p",
            "-c:a",
            "copy",
            str(config.output_video),
        ]

        if config.quick:
            cmd.extend(
                [
                    "-preset",
                    "ultrafast",
                    "-c:v",
                    "h264_nvenc",
                ]
            )

        if verbose:
            logger.info("Processing video with command: {}", " ".join(cmd))
            start_time = time.time()

        subprocess.run(cmd, check=True, capture_output=not verbose, text=True)

        if verbose:
            end_time = time.time()
            duration = end_time - start_time
            logger.info("Success! Processed video saved to: {}", config.output_video)
            logger.info("Processing completed in {:.2f} seconds", duration)

    except subprocess.CalledProcessError as e:
        logger.error("FFmpeg processing failed: {}", e.stderr)
        raise RuntimeError(f"FFmpeg processing failed: {e.stderr}") from e
    except Exception as e:
        logger.error("Video processing failed: {}", str(e))
        raise RuntimeError(f"Video processing failed: {str(e)}") from e


def cli(
    *image_pairs: str,
    input_video: str = None,
    output_video: str = None,
    lut_path: str = None,
    quick: bool = False,
    verbose: bool = False,
) -> None:
    """Process multiple source-target image pairs and optionally apply to video.

    Args:
        *image_pairs: Variable number of source and target image paths as pairs
        input_video: Optional input video to process
        output_video: Optional output video path
        lut_path: Optional path for the LUT file
        verbose: Whether to log additional information
    """
    import sys

    logger.remove()
    logger.add(sys.stderr, level="INFO" if verbose else "WARNING")

    # Validate we have pairs of images
    if len(image_pairs) < 2 or len(image_pairs) % 2 != 0:
        raise ValueError("Must provide pairs of source and target images")

    pairs = list(zip(image_pairs[::2], image_pairs[1::2]))
    config = ProcessingConfig(
        source_target_pairs=pairs,
        input_video=input_video,
        output_video=output_video,
        lut_path=lut_path,
        quick=quick,
    )

    # Create LUT
    lut_file = create_multi_lut(config, verbose=verbose)
    if verbose:
        logger.info(f"Created LUT file: {lut_file}")

    # Process video if provided
    if config.input_video:
        process_video(config, verbose=verbose)


if __name__ == "__main__":
    Fire(cli)
