# huehoppy.tests.test_mvp_functionality - Basic tests for MVP features

import unittest
import numpy as np
import os
import sys

# Adjust path to import huehoppy components if running script directly
# This assumes the script is run from the project root as: python -m unittest huehoppy.tests.test_mvp_functionality
HUEHOPPY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if HUEHOPPY_ROOT not in sys.path:
    sys.path.insert(0, HUEHOPPY_ROOT)

try:
    from huehoppy.core.manager import AlgorithmManager
    from huehoppy.core.pipeline import Pipeline
    from huehoppy.utils.image_io import read_image_bgr, save_image_bgr # For potential future use with actual images
except ImportError as e:
    print(f"CRITICAL: Failed to import huehoppy components for testing: {e}")
    # This will cause tests to fail if components are not found
    AlgorithmManager = None
    Pipeline = None

class TestMVPFunctionality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if AlgorithmManager is None:
            raise unittest.SkipTest("Skipping tests: AlgorithmManager not available due to import errors.")
        cls.manager = AlgorithmManager()
        cls.algorithms_to_test = cls.manager.list_available_algorithms()
        if not cls.algorithms_to_test:
            raise unittest.SkipTest("Skipping tests: No algorithms found by AlgorithmManager.")

        # Create dummy images for testing
        # Dimensions can be small to speed up tests
        cls.dummy_source_bgr = np.random.randint(0, 256, size=(64, 64, 3), dtype=np.uint8)
        cls.dummy_target_bgr = np.random.randint(0, 256, size=(60, 70, 3), dtype=np.uint8) # Different size for target

    def test_01_algorithm_manager_discovery(self):
        """Test if AlgorithmManager discovers the expected MVP algorithms."""
        self.assertIsNotNone(self.manager, "AlgorithmManager should be initialized.")
        expected_mvp_algorithms = ["reinhard", "colortranslhm", "colortranspccm"]
        discovered_algorithms = self.manager.list_available_algorithms()
        for alg_name in expected_mvp_algorithms:
            self.assertIn(alg_name, discovered_algorithms, f"{alg_name} not found by AlgorithmManager.")
        print(f"\n[Test Log] Discovered algorithms by manager: {discovered_algorithms}")

    def test_02_individual_algorithms_transfer(self):
        """Test the transfer method of each discovered algorithm with dummy data."""
        self.assertIsNotNone(self.manager, "AlgorithmManager should be initialized.")
        self.assertTrue(len(self.algorithms_to_test) > 0, "No algorithms available to test.")

        for alg_name in self.algorithms_to_test:
            with self.subTest(algorithm=alg_name):
                print(f"\n[Test Log] Testing algorithm: {alg_name}")
                algorithm = self.manager.get_algorithm(alg_name)
                self.assertIsNotNone(algorithm, f"Could not retrieve algorithm: {alg_name}")

                try:
                    # Using copies to ensure original dummy images are not modified if an alg works in-place (it shouldn't)
                    source_copy = self.dummy_source_bgr.copy()
                    target_copy = self.dummy_target_bgr.copy()

                    result_image = algorithm.transfer(source_copy, target_copy)

                    self.assertIsNotNone(result_image, "Algorithm transfer() returned None.")
                    self.assertIsInstance(result_image, np.ndarray, "Result is not a NumPy array.")
                    self.assertEqual(result_image.ndim, 3, "Result image does not have 3 dimensions.")
                    self.assertEqual(result_image.shape[2], 3, "Result image does not have 3 channels.")
                    # Output dimensions should match the target image's dimensions
                    self.assertEqual(result_image.shape[0], self.dummy_target_bgr.shape[0], "Result height mismatch.")
                    self.assertEqual(result_image.shape[1], self.dummy_target_bgr.shape[1], "Result width mismatch.")
                    self.assertEqual(result_image.dtype, np.uint8, "Result image dtype is not uint8 (expected for BGR images).")
                    print(f"[Test Log] {alg_name} transfer successful. Output shape: {result_image.shape}, dtype: {result_image.dtype}")

                except Exception as e:
                    self.fail(f"Algorithm {alg_name} transfer method failed with error: {e}")

    def test_03_basic_pipeline(self):
        """Test a simple pipeline with two algorithms using dummy data."""
        self.assertIsNotNone(self.manager, "AlgorithmManager should be initialized.")
        if len(self.algorithms_to_test) < 2:
            self.skipTest("Skipping pipeline test: Less than 2 algorithms available.")

        alg1_name = self.algorithms_to_test[0]
        alg2_name = self.algorithms_to_test[1] # Choose a different one if available

        if alg1_name == alg2_name and len(self.algorithms_to_test) > 1: # Ensure different algs if possible
             alg2_name = self.algorithms_to_test[1] if len(self.algorithms_to_test) > 1 else self.algorithms_to_test[0]


        alg1 = self.manager.get_algorithm(alg1_name)
        alg2 = self.manager.get_algorithm(alg2_name)

        self.assertIsNotNone(alg1, f"Could not retrieve algorithm for pipeline: {alg1_name}")
        self.assertIsNotNone(alg2, f"Could not retrieve algorithm for pipeline: {alg2_name}")

        pipeline = Pipeline()
        pipeline.add_step(alg1).add_step(alg2)
        print(f"\n[Test Log] Testing pipeline: {pipeline}")

        try:
            source_copy = self.dummy_source_bgr.copy()
            target_copy = self.dummy_target_bgr.copy()

            result_image = pipeline.process(source_copy, target_copy)

            self.assertIsNotNone(result_image, "Pipeline process() returned None.")
            self.assertIsInstance(result_image, np.ndarray, "Pipeline result is not a NumPy array.")
            self.assertEqual(result_image.ndim, 3, "Pipeline result image does not have 3 dimensions.")
            self.assertEqual(result_image.shape[2], 3, "Pipeline result image does not have 3 channels.")
            self.assertEqual(result_image.shape[0], self.dummy_target_bgr.shape[0], "Pipeline result height mismatch.")
            self.assertEqual(result_image.shape[1], self.dummy_target_bgr.shape[1], "Pipeline result width mismatch.")
            self.assertEqual(result_image.dtype, np.uint8, "Pipeline result image dtype is not uint8.")
            print(f"[Test Log] Pipeline processing successful. Output shape: {result_image.shape}, dtype: {result_image.dtype}")

        except Exception as e:
            self.fail(f"Pipeline processing failed with error: {e}")

if __name__ == '__main__':
    # This allows running tests with `python huehoppy/tests/test_mvp_functionality.py`
    # For this to work, PYTHONPATH must include the project root.
    # Better to run with `python -m unittest huehoppy.tests.test_mvp_functionality` from root.
    unittest.main()
