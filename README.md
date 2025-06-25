# huehoppy

A Python library for color transfer between images. This project aims to provide a modular and extensible system for applying various color transfer algorithms.

**MVP Status (Current Version: 0.1.0 - Unreleased)**

This is an MVP (Minimum Viable Product) version focusing on a stable core and a few selected algorithms.

- **Core Features:**
    - Modular architecture for easy addition of new algorithms.
    - `AlgorithmManager` to discover and load available algorithms.
    - Basic `Pipeline` system for chaining multiple algorithm steps (though each step currently uses the original source image).
    - Command-Line Interface (CLI) for listing and running algorithms.
- **Included Algorithms (MVP):**
    - `Reinhard`: Based on "Color Transfer between Images" by Reinhard et al. (via `python-color-transfer` submodule).
    - `LHM (Linear Histogram Matching)`: Based on Hertzmann (via `colortrans` submodule).
    - `PCCM (Principal Components Color Matching)`: Based on Kotera et al. (via `colortrans` submodule).
- **Deferred for Future Versions:**
    - Integration of `ColorTransferLib` due to its complex dependencies and installation.

## Original Project Goal (Future Vision)

The original goal (still a future aim) is to improve upon three existing color transfer libraries:
- `ColorTransferLib`
- `python-color-transfer`
- `colortrans`

Key problems to solve include dependency brittleness, lack of modularity, and difficulty in chaining algorithms. The proposed solution involves:
1. Loading algorithms independently.
2. Using a clean, consistent API.
3. Easy algorithm chaining.
4. Separating file I/O from core logic.
5. Allowing users to install only needed dependencies (future goal).

## Installation (MVP)

1.  **Clone the repository (including submodules):**
    ```bash
    git clone --recurse-submodules https://github.com/twardoch/huehoppy.git
    cd huehoppy
    ```

2.  **Set up a Python virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install `numpy`, `opencv-python`, `Pillow`, and `click`.

## Usage (MVP)

### Command-Line Interface (CLI)

The CLI allows you to list available algorithms and run them on images. Make sure your virtual environment is activated and you are in the project root directory.

**1. List available algorithms:**
```bash
PYTHONPATH=. python huehoppy/cli.py list
```
Expected output:
```
Available algorithms:
- colortranslhm
- colortranspccm
- reinhard
```

**2. Run an algorithm:**
```bash
PYTHONPATH=. python huehoppy/cli.py run \
    -s path/to/your/source_image.jpg \
    -t path/to/your/target_image.jpg \
    -o path/to/your/output_image.jpg \
    -a reinhard
```
Replace `path/to/...` with actual image paths and `reinhard` with your desired algorithm name from the list.

### Library Usage (Python)

You can also use `huehoppy` as a library in your Python scripts.

```python
from huehoppy.core.manager import AlgorithmManager
from huehoppy.utils.image_io import read_image_bgr, save_image_bgr
# Assuming huehoppy directory is in your PYTHONPATH or huehoppy is installed

# Initialize the manager
manager = AlgorithmManager()

# List available algorithms
print("Available algorithms:", manager.list_available_algorithms())

# Get an algorithm instance
algorithm_name = "reinhard" # Or "colortranslhm", "colortranspccm"
algorithm = manager.get_algorithm(algorithm_name)

if algorithm:
    try:
        # Load images (ensure paths are correct)
        source_img = read_image_bgr("path/to/source_image.jpg")
        target_img = read_image_bgr("path/to/target_image.jpg")

        # Apply the color transfer
        print(f"Applying {algorithm_name}...")
        processed_img = algorithm.transfer(source_img, target_img)

        # Save the result
        save_image_bgr("path/to/output_image.jpg", processed_img)
        print(f"Processed image saved to path/to/output_image.jpg")

    except FileNotFoundError:
        print("Error: One or both image files not found. Please check paths.")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print(f"Algorithm '{algorithm_name}' not found.")

# Example using the pipeline (conceptual for now)
# from huehoppy.core.pipeline import Pipeline
# if manager.get_algorithm("reinhard") and manager.get_algorithm("colortranslhm"):
#     pipeline = Pipeline()
#     pipeline.add_step(manager.get_algorithm("reinhard"))
#     pipeline.add_step(manager.get_algorithm("colortranslhm"))
#
#     # target_after_pipeline = pipeline.process(source_img, target_img)
#     # save_image_bgr("path/to/pipeline_output.jpg", target_after_pipeline)
#     print("Pipeline example is conceptual and would require images to be loaded.")

```

## Submodules

This project uses git submodules to include code from the original libraries it builds upon:
- `submodules/ColorTransferLib`
- `submodules/colortrans`
- `submodules/python-color-transfer`

Ensure you clone with `--recurse-submodules` or run `git submodule update --init --recursive` after cloning.

## Contributing

Contributions are welcome! Please refer to the project's issue tracker and consider submitting a pull request. (Further contribution guidelines can be added later).

## License

This project is licensed under the [MIT License](./LICENSE). Note that the submodules have their own licenses.
```
