# huehoppy.core.pipeline - Basic algorithm pipeline system

import numpy as np
from typing import List
from huehoppy.core.base_algorithm import ColorTransferAlgorithm

class Pipeline:
    """
    A simple pipeline to apply a sequence of color transfer algorithms.
    """

    def __init__(self):
        self._steps: List[ColorTransferAlgorithm] = []

    def add_step(self, algorithm: ColorTransferAlgorithm) -> 'Pipeline':
        """
        Adds a color transfer algorithm instance to the pipeline.

        Args:
            algorithm: An instance of a class derived from ColorTransferAlgorithm.

        Returns:
            The Pipeline instance, to allow for method chaining (e.g., p.add_step(a).add_step(b)).

        Raises:
            TypeError: If the provided algorithm is not an instance of ColorTransferAlgorithm.
        """
        if not isinstance(algorithm, ColorTransferAlgorithm):
            raise TypeError("Algorithm must be an instance of ColorTransferAlgorithm.")
        self._steps.append(algorithm)
        return self

    def process(self, source_image: np.ndarray, target_image: np.ndarray) -> np.ndarray:
        """
        Processes the target image through all algorithms in the pipeline.

        Each algorithm in the pipeline uses the *original* source_image as its reference
        and the output of the previous step as its target.

        Args:
            source_image: The initial source image (NumPy BGR array) to be used as reference by all steps.
            target_image: The initial target image (NumPy BGR array) to be processed.

        Returns:
            The final processed target image (NumPy BGR array) after all pipeline steps.

        Raises:
            ValueError: If the pipeline has no steps.
        """
        if not self._steps:
            raise ValueError("Cannot process with an empty pipeline. Add algorithm steps first.")

        if not isinstance(source_image, np.ndarray) or not isinstance(target_image, np.ndarray):
            raise TypeError("Initial source and target images must be NumPy ndarrays.")

        current_target_image = target_image.copy() # Work on a copy

        print(f"Starting pipeline processing with {len(self._steps)} step(s).")
        for i, algorithm_step in enumerate(self._steps):
            print(f"  Step {i+1}/{len(self._steps)}: Applying {algorithm_step}...")
            try:
                current_target_image = algorithm_step.transfer(source_image, current_target_image)
                print(f"    Step {i+1} completed.")
            except Exception as e:
                print(f"    Error during pipeline step {i+1} ({algorithm_step}): {e}")
                # Decide on error strategy: re-raise, return intermediate, or log and continue?
                # For MVP, re-raising to make issues visible.
                raise e

        print("Pipeline processing finished.")
        return current_target_image

    def __len__(self) -> int:
        return len(self._steps)

    def __str__(self) -> str:
        if not self._steps:
            return "<Pipeline (empty)>"
        step_names = " -> ".join(str(step) for step in self._steps)
        return f"<Pipeline: {step_names}>"

if __name__ == '__main__':
    # This is a conceptual test and requires actual algorithm instances.
    # It also needs AlgorithmManager and actual image data to run fully.
    print("Conceptual test for Pipeline:")

    # Mock Algorithm for testing pipeline structure
    class MockAlgorithm(ColorTransferAlgorithm):
        def __init__(self, name="Mock"):
            self._name = name
        def transfer(self, source_image: np.ndarray, target_image: np.ndarray) -> np.ndarray:
            print(f"    MockAlgorithm '{self._name}' processing...")
            # In a real scenario, it would return a modified target_image
            # For this mock, just return a copy to simulate change
            return target_image.copy()
        def __str__(self):
            return self._name

    mock_alg1 = MockAlgorithm("Reinhard_Mock")
    mock_alg2 = MockAlgorithm("LHM_Mock")

    pipeline = Pipeline()
    pipeline.add_step(mock_alg1).add_step(mock_alg2)

    print(f"Pipeline created: {pipeline}")
    print(f"Number of steps: {len(pipeline)}")

    # Dummy images (replace with actual image loading for a real test)
    dummy_source = np.zeros((10, 10, 3), dtype=np.uint8)
    dummy_target = np.ones((10, 10, 3), dtype=np.uint8) * 255

    print("\nSimulating pipeline processing...")
    try:
        processed_image = pipeline.process(dummy_source, dummy_target)
        print(f"Pipeline processing simulation successful. Output shape: {processed_image.shape}")
    except Exception as e:
        print(f"Error in pipeline processing simulation: {e}")

    # Test empty pipeline
    empty_pipeline = Pipeline()
    try:
        print("\nSimulating empty pipeline processing (should fail)...")
        empty_pipeline.process(dummy_source, dummy_target)
    except ValueError as e:
        print(f"Correctly caught error for empty pipeline: {e}")

    # Test adding non-algorithm
    try:
        print("\nTesting adding non-algorithm (should fail)...")
        pipeline.add_step("not an algorithm")
    except TypeError as e:
        print(f"Correctly caught error for adding non-algorithm: {e}")
