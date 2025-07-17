"""Command-line interface for huehoppy."""

import sys
from pathlib import Path
from typing import Optional

import click
import cv2
import numpy as np
from loguru import logger
from rich.console import Console
from rich.table import Table

from .core import HueHoppyManager, Pipeline

console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    logger.remove()
    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=level, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")


def load_image(path: Path) -> np.ndarray:
    """Load an image file."""
    if not path.exists():
        raise click.ClickException(f"Image file not found: {path}")
    
    image = cv2.imread(str(path))
    if image is None:
        raise click.ClickException(f"Failed to load image: {path}")
    
    return image


def save_image(image: np.ndarray, path: Path) -> None:
    """Save an image file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(path), image)
    if not success:
        raise click.ClickException(f"Failed to save image: {path}")


@click.group()
@click.version_option()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """huehoppy: Advanced Color Transfer Tool"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    setup_logging(verbose)


@main.command()
@click.pass_context
def list_algorithms(ctx: click.Context) -> None:
    """List available color transfer algorithms."""
    manager = HueHoppyManager()
    algorithms = manager.get_available_algorithms()
    
    if not algorithms:
        console.print("[yellow]No algorithms available[/yellow]")
        return
    
    table = Table(title="Available Color Transfer Algorithms")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Author", style="green")
    table.add_column("Version", style="yellow")
    
    for name in algorithms:
        metadata = manager.get_algorithm_metadata(name)
        if metadata:
            table.add_row(
                name,
                metadata.description,
                metadata.author,
                metadata.version
            )
        else:
            table.add_row(name, "No metadata available", "Unknown", "Unknown")
    
    console.print(table)


@main.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.argument("reference", type=click.Path(exists=True, path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
@click.option("--algorithm", "-a", default="reinhard", help="Algorithm to use")
@click.option("--preview", is_flag=True, help="Show preview before saving")
@click.pass_context
def transfer(
    ctx: click.Context,
    source: Path,
    reference: Path,
    output: Path,
    algorithm: str,
    preview: bool,
) -> None:
    """Perform color transfer between two images."""
    verbose = ctx.obj["verbose"]
    
    try:
        # Load images
        console.print(f"Loading source image: {source}")
        source_img = load_image(source)
        
        console.print(f"Loading reference image: {reference}")
        reference_img = load_image(reference)
        
        # Initialize manager and perform transfer
        manager = HueHoppyManager()
        
        if algorithm not in manager.get_available_algorithms():
            available = ", ".join(manager.get_available_algorithms())
            raise click.ClickException(f"Algorithm '{algorithm}' not available. Available: {available}")
        
        console.print(f"Applying {algorithm} algorithm...")
        result = manager.transfer(algorithm, source_img, reference_img)
        
        # Save result
        console.print(f"Saving result to: {output}")
        save_image(result, output)
        
        console.print("[green]Color transfer completed successfully![/green]")
        
    except Exception as e:
        logger.error(f"Color transfer failed: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.argument("config", type=click.Path(exists=True, path_type=Path))
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.argument("reference", type=click.Path(exists=True, path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
@click.option("--save-intermediate", is_flag=True, help="Save intermediate results")
@click.pass_context
def pipeline(
    ctx: click.Context,
    config: Path,
    source: Path,
    reference: Path,
    output: Path,
    save_intermediate: bool,
) -> None:
    """Execute a color transfer pipeline from configuration file."""
    verbose = ctx.obj["verbose"]
    
    try:
        # Load images
        console.print(f"Loading source image: {source}")
        source_img = load_image(source)
        
        console.print(f"Loading reference image: {reference}")
        reference_img = load_image(reference)
        
        # TODO: Implement pipeline configuration loading
        raise click.ClickException("Pipeline configuration not yet implemented")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()