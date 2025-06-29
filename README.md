# huehoppy: Advanced Color Transfer Tool

**huehoppy** is a powerful and flexible Python library for transferring color palettes and styles between images and other visual media. It aims to consolidate the best features of existing color transfer libraries while offering enhanced modularity, a consistent API, and the ability to create sophisticated processing pipelines.

## What is huehoppy?

At its core, huehoppy allows you to take the color characteristics of a *reference* image (or other media) and apply them to a *source* image, transforming its look and feel. This can be used for a variety of applications, such as:

*   **Artistic stylization:** Give your photos the color palette of a famous painting.
*   **Color correction and grading:** Standardize colors across a set of images or video clips.
*   **Data augmentation:** Generate new training data for machine learning models with varied color profiles.
*   **Scientific visualization:** Enhance or alter colors in data representations to improve clarity.

huehoppy is designed to be a comprehensive toolkit, integrating a variety of algorithms from established research and open-source projects. It addresses common pain points found in other libraries, such as brittle dependency management and difficulty in extending or combining different methods.

## Who is it for?

huehoppy is designed for a diverse range of users:

*   **Researchers:** Provides a unified platform to implement, compare, and evaluate different color transfer, style transfer, and colorization algorithms.
*   **Developers:** Offers a clean and consistent API to integrate advanced color manipulation capabilities into their applications.
*   **Digital Artists & Designers:** Enables creative exploration of color and style in their visual projects.
*   **Hobbyists:** Makes sophisticated color transfer techniques accessible for personal projects.

## Why is huehoppy useful?

huehoppy offers several key advantages:

*   **Unified Access to Multiple Algorithms:** Integrates various algorithms from libraries like ColorTransferLib, python-color-transfer, and colortrans under a single, consistent interface.
*   **Improved Modularity:** Algorithms are loaded independently. If one algorithm fails due to missing dependencies or other issues, others remain operational.
*   **Extensibility:** The architecture makes it straightforward to add new algorithms without impacting existing ones.
*   **Algorithm Chaining:** A pipeline system allows users to chain multiple algorithms together, applying a sequence of transformations to achieve complex effects.
*   **Flexible Dependency Management:** Users can install only the dependencies required for the specific algorithms they intend to use, keeping installations lean.
*   **Separation of Concerns:** Core algorithm logic is decoupled from file I/O and data type handling, leading to cleaner and more maintainable code.
*   **Broad Data Type Support:** Aims to support various data types beyond simple images, including point clouds, textured meshes, videos, and more (inspired by ColorTransferLib).

## Installation

Installing huehoppy is straightforward using pip.

```bash
pip install huehoppy
```

While the core `huehoppy` package is lightweight, some specific algorithms may require additional dependencies (e.g., specific versions of PyTorch, TensorFlow, or other scientific libraries). huehoppy will inform you if a selected algorithm has unmet dependencies, and you will be able to install them as needed. For example, to install dependencies for a specific algorithm 'some_algo':

```bash
pip install huehoppy[some_algo_dependencies]
# or follow specific instructions provided by the algorithm's documentation within huehoppy.
```

## How to Use huehoppy

huehoppy can be used both from the command line for quick tasks and programmatically within your Python scripts for more complex integrations.

### Command-Line Interface (CLI)

The CLI provides a convenient way to apply color transfer between two images using a specified algorithm.

```bash
huehoppy transfer --source path/to/source_image.png \
                  --reference path/to/reference_image.png \
                  --output path/to/output_image.png \
                  --algorithm GLO  # Example: Reinhard et al. algorithm
```

To list available algorithms:

```bash
huehoppy list-algorithms
```

For help on a specific command or algorithm:

```bash
huehoppy transfer --help
huehoppy transfer --algorithm GLO --help
```
*(Note: Specific CLI syntax is illustrative and subject to final design.)*

### Programmatic Usage (Python API)

The Python API offers fine-grained control and flexibility.

```python
from huehoppy import HueHoppyManager, ImageObject # Assuming these class names

# Initialize the manager - it discovers available algorithms
manager = HueHoppyManager()

# List available algorithms
print("Available algorithms:", manager.list_algorithms())

# Load source and reference images (example using a hypothetical ImageObject)
# huehoppy will provide utilities or expect data in a common format (e.g., NumPy arrays)
source_img = ImageObject.from_file("path/to/source_image.png")
reference_img = ImageObject.from_file("path/to/reference_image.png")

# Select and apply an algorithm
algorithm_name = "GLO" # Example: Reinhard et al. from ColorTransferLib
options = {"mode": "RGB"} # Algorithm-specific options

try:
    color_transfer_algo = manager.get_algorithm(algorithm_name)

    # The API will clearly define how source, reference, and options are passed
    result_img = color_transfer_algo.apply(source_img, reference_img, options=options)

    # Save the output
    result_img.save("path/to/output_image.png")
    print(f"Successfully applied {algorithm_name} and saved the output.")

except Exception as e:
    print(f"An error occurred: {e}")

# Example of chaining algorithms (conceptual)
# pipeline = manager.create_pipeline()
# pipeline.add_step("Reinhard", {"param1": "value1"})
# pipeline.add_step("ColorBalance", {"brightness": 1.1})
# result_img_pipelined = pipeline.execute(source_img, reference_img_for_reinhard)
# result_img_pipelined.save("path/to/output_pipelined.png")
```
*(Note: Specific API calls and class names are illustrative and subject to final design based on the "Future" section of the original README.)*

## How huehoppy Works: Technical Architecture

huehoppy is being built with a modular and extensible architecture in mind, drawing lessons from existing libraries like ColorTransferLib, python-color-transfer, and colortrans. The goal is to create a robust system that is easy to maintain and extend.

### Core Architectural Principles:

1.  **Algorithm Isolation:**
    *   Each color transfer (or related, like style transfer/colorization) algorithm will reside in its own dedicated sub-directory within the `huehoppy/algorithms/` path.
    *   Each algorithm's directory will contain its specific implementation and can declare its own dependencies (e.g., in a `requirements.txt` or `pyproject.toml` snippet). This ensures that dependency conflicts for one algorithm do not affect others.
    *   The main `huehoppy` package will have minimal core dependencies.

2.  **Manager Class:**
    *   A central `HueHoppyManager` class will be responsible for discovering and loading available algorithms at runtime.
    *   It will scan the `algorithms` directory and register valid algorithm plugins.
    *   It will provide a consistent interface to instantiate and use any loaded algorithm.
    *   The manager will handle potential errors during algorithm loading gracefully (e.g., if an algorithm's dependencies are not met, it will be marked as unavailable but won't crash the system).

3.  **Standardized API:**
    *   Each algorithm, despite its internal complexity, will be expected to conform to a standardized API. This typically involves an `apply(source_data, reference_data, options)` method.
    *   `source_data` and `reference_data` will be instances of well-defined data wrapper classes (e.g., `ImageObject`, `PointCloudObject`) that abstract the underlying data representation (e.g., NumPy array, file path, specific 3D data structure).
    *   `options` will be a dictionary allowing algorithm-specific parameters to be passed. Each algorithm will document its available options.

4.  **Pipeline System:**
    *   A pipeline system will be implemented to allow users to chain multiple algorithms together.
    *   Users will be able to define a sequence of operations (e.g., apply Reinhard color transfer, then adjust contrast, then apply a specific artistic filter).
    *   The pipeline will manage the flow of data between steps.

5.  **Separation of I/O and Core Logic:**
    *   File input/output operations (loading from and saving to disk) will be handled by the data wrapper classes or utility functions, separate from the core algorithm implementations.
    *   Algorithms will primarily operate on in-memory data representations (e.g., NumPy arrays for images).

6.  **Data Type Abstraction:**
    *   Inspired by ColorTransferLib, `huehoppy` aims to support various data types. This will be achieved through:
        *   Base data classes (e.g., `VisualMediaObject`).
        *   Derived classes for specific types (e.g., `ImageObject`, `VideoObject`, `MeshObject`, `PointCloudObject`, `GaussianSplattingObject`).
        *   Algorithms will declare which data types they support. The manager class can help filter algorithms based on input data types.

### Integrated Algorithms:

huehoppy will initially focus on integrating and providing a unified interface to algorithms found in its submodules:

*   **ColorTransferLib:** A rich source of diverse color transfer, style transfer, and colorization methods for various data types (Images, Point Clouds, Meshes, Videos, etc.). Examples include:
    *   Reinhard et al. (GLO)
    *   Monge-Kantorovitch Linear Colour Mapping (MKL)
    *   Gradient-Preserving Color Transfer (GPC)
    *   Neural Style Transfer (NST)
    *   Instance-aware Image Colorization (IIC)
    *   *(Refer to `submodules/ColorTransferLib/README.md` for a full list)*
*   **python-color-transfer:** Provides implementations for:
    *   Mean standard deviation transfer (RGB and Lab spaces)
    *   PDF transfer + Regraining
*   **colortrans:** Offers:
    *   Linear Histogram Matching (LHM)
    *   Principal Components Color Matching (PCCM)
    *   Reinhard et al.

The goal is to adapt these algorithms to the new `huehoppy` API for a seamless user experience.

## Coding and Contribution Guidelines

We welcome contributions to `huehoppy`! To ensure consistency and maintainability, please adhere to the following guidelines.

### Coding Conventions:

*   **Language:** Python 3.8+.
*   **Style:** Follow [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/). Use a linter like Flake8 and a formatter like Black or Ruff to maintain consistent code style.
*   **Type Hinting:** Use type hints for all function signatures and important variables as per [PEP 484](https://www.python.org/dev/peps/pep-0484/).
*   **Docstrings:** Write clear and concise docstrings for all modules, classes, functions, and methods, following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) or NumPy/SciPy docstring conventions.
*   **Logging:** Use the `logging` module for any informational messages, warnings, or errors. Avoid using `print()` statements in library code.

### Adding New Algorithms:

1.  **Directory Structure:**
    *   Create a new directory for your algorithm under `huehoppy/algorithms/your_algorithm_name/`.
    *   Include an `__init__.py` file in this directory that exposes your main algorithm class.
2.  **Algorithm Class:**
    *   Your algorithm should be implemented as a class that inherits from a base `huehoppy.BaseAlgorithm` (or similar) class.
    *   Implement the required methods, primarily `apply(self, source_data, reference_data, **options)`.
    *   Define any algorithm-specific options with clear defaults.
    *   Specify the input and output data types it supports.
3.  **Dependencies:**
    *   If your algorithm has specific Python package dependencies, list them in a `requirements.txt` file within your algorithm's directory. The `HueHoppyManager` might use this for providing installation instructions or optional installs.
4.  **Metadata:**
    *   Provide metadata for your algorithm (e.g., name, description, paper reference if applicable). This might be done via class attributes or a separate manifest file.
5.  **Documentation:**
    *   Add a `README.md` inside your algorithm's folder explaining its purpose, how it works, its specific options, and citing any relevant publications.
6.  **Tests:**
    *   Write unit tests for your algorithm. Place them in a `tests/` subdirectory within your algorithm's folder or in the main `tests/` directory of the project, following the project's testing structure.

### Running Tests:

The project will use a standard testing framework like `pytest`.

```bash
# Install test dependencies (if any, e.g., pytest, pytest-cov)
pip install pytest pytest-cov

# Run all tests
pytest
```

Ensure all tests pass before submitting a contribution. Include new tests for any new features or bug fixes.

### Submitting Contributions:

1.  **Fork the Repository:** Create your own fork of the `huehoppy` repository on GitHub.
2.  **Create a Branch:** Create a new branch in your fork for your changes (e.g., `git checkout -b feature/my-new-algorithm` or `bugfix/issue-123`).
3.  **Make Your Changes:** Implement your feature or bug fix.
4.  **Test Your Changes:** Run the test suite to ensure everything passes.
5.  **Document Your Changes:** Update any relevant documentation, including docstrings and README files.
6.  **Commit Your Changes:** Write clear and concise commit messages.
7.  **Push to Your Fork:** Push your changes to your branch on GitHub.
8.  **Create a Pull Request:** Open a pull request from your branch to the `main` branch of the original `huehoppy` repository.
    *   Provide a clear description of your changes in the pull request.
    *   Reference any relevant issues.
9.  **Code Review:** Your pull request will be reviewed by maintainers. Be prepared to address any feedback or make further changes.

By contributing, you agree that your contributions will be licensed under the project's license (currently MIT License, as per the LICENSE file in the repository).

---

This document aims to be a comprehensive guide. If you have questions, please open an issue on the GitHub repository.
