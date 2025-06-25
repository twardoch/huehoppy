# huehoppy.cli - Command-Line Interface for huehoppy

import click
import numpy as np
import os

try:
    from huehoppy.core.manager import AlgorithmManager
    from huehoppy.utils.image_io import read_image_bgr, save_image_bgr, ImageIOError
    from huehoppy.core.pipeline import Pipeline # For potential future use
except ImportError as e:
    # This might happen if huehoppy is not installed or PYTHONPATH is not set correctly
    # when developing. For the CLI to run, these need to be resolvable.
    print(f"Error: Could not import huehoppy components. Ensure huehoppy is installed or PYTHONPATH is set.")
    print(f"Details: {e}")
    # Allow click to register commands but they will likely fail if imports are missing.
    # A better approach for a real package would be to have huehoppy installed.
    AlgorithmManager = None
    read_image_bgr = None
    save_image_bgr = None
    ImageIOError = None


@click.group()
def cli():
    """HueHoppy: A command-line tool for color transfer between images."""
    if AlgorithmManager is None: # Basic check if core components failed to load
        click.echo(click.style("Critical Error: HueHoppy core components could not be loaded. CLI is non-functional.", fg="red"), err=True)
        # Consider exiting if absolutely non-functional:
        # raise click.Abort()
    pass

@cli.command("list")
def list_algorithms():
    """Lists all available color transfer algorithms."""
    if AlgorithmManager is None:
        click.echo(click.style("AlgorithmManager not available.", fg="red"), err=True)
        return

    manager = AlgorithmManager()
    algorithms = manager.list_available_algorithms()
    if not algorithms:
        click.echo("No algorithms found.")
        return
    click.echo("Available algorithms:")
    for alg_name in sorted(algorithms):
        click.echo(f"- {alg_name}")

@cli.command("run")
@click.option('-s', '--source', 'source_path', required=True, type=click.Path(exists=True, dir_okay=False, readable=True), help="Path to the source image.")
@click.option('-t', '--target', 'target_path', required=True, type=click.Path(exists=True, dir_okay=False, readable=True), help="Path to the target image.")
@click.option('-o', '--output', 'output_path', required=True, type=click.Path(writable=True, dir_okay=False), help="Path to save the output image.")
@click.option('-a', '--algorithm', 'algorithm_name', required=True, type=str, help="Name of the algorithm to use (see 'list' command).")
def run_algorithm(source_path: str, target_path: str, output_path: str, algorithm_name: str):
    """Runs a specified color transfer algorithm."""
    if AlgorithmManager is None or read_image_bgr is None or save_image_bgr is None or ImageIOError is None:
        click.echo(click.style("Core components (Manager, ImageIO) not available.", fg="red"), err=True)
        return

    manager = AlgorithmManager()
    algorithm_instance = manager.get_algorithm(algorithm_name)

    if algorithm_instance is None:
        click.echo(click.style(f"Error: Algorithm '{algorithm_name}' not found.", fg="red"), err=True)
        click.echo(f"Available algorithms: {', '.join(sorted(manager.list_available_algorithms()))}")
        return

    try:
        click.echo(f"Reading source image from: {source_path}")
        source_img = read_image_bgr(source_path)
        click.echo(f"Reading target image from: {target_path}")
        target_img = read_image_bgr(target_path)
    except ImageIOError as e:
        click.echo(click.style(f"Error reading images: {e}", fg="red"), err=True)
        return
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred while reading images: {e}", fg="red"), err=True)
        return

    click.echo(f"Applying algorithm: {algorithm_name}...")
    try:
        # Ensure images are contiguous if required by any algorithm (good practice)
        source_img_cont = np.ascontiguousarray(source_img)
        target_img_cont = np.ascontiguousarray(target_img)

        processed_image = algorithm_instance.transfer(source_img_cont, target_img_cont)
        click.echo("Algorithm applied successfully.")
    except Exception as e:
        click.echo(click.style(f"Error during color transfer with '{algorithm_name}': {e}", fg="red"), err=True)
        # More detailed error logging could be added here if needed
        # import traceback
        # click.echo(traceback.format_exc(), err=True)
        return

    try:
        click.echo(f"Saving output image to: {output_path}")
        # Ensure output directory exists, though save_image_bgr does this
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        save_image_bgr(output_path, processed_image)
        click.echo(f"Output image saved successfully: {output_path}")
    except ImageIOError as e:
        click.echo(click.style(f"Error saving image: {e}", fg="red"), err=True)
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred while saving the image: {e}", fg="red"), err=True)

if __name__ == '__main__':
    # This allows running `python huehoppy/cli.py ...`
    # For this to work correctly when developing without installing huehoppy,
    # the PYTHONPATH needs to include the project root.
    # Example: PYTHONPATH=$PYTHONPATH:/path/to/your/huehoppy_project python huehoppy/cli.py list
    cli()
