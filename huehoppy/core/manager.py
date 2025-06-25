# huehoppy.core.manager - Algorithm Manager

import os
import importlib
import inspect
import pkgutil

from huehoppy.core.base_algorithm import ColorTransferAlgorithm
import huehoppy.algorithms # To ensure the package is recognized

class AlgorithmManager:
    """
    Manages discovery and access to color transfer algorithms.

    Scans the `huehoppy.algorithms` package for modules containing classes
    that inherit from `ColorTransferAlgorithm`.
    """

    def __init__(self):
        self._algorithms = {}
        self._load_algorithms()

    def _load_algorithms(self):
        """
        Discovers and loads algorithms from the `huehoppy.algorithms` package.
        """
        alg_package = huehoppy.algorithms
        prefix = alg_package.__name__ + "."

        # Iterate over all modules in the huehoppy.algorithms package
        for importer, modname, ispkg in pkgutil.iter_modules(alg_package.__path__, prefix):
            if ispkg: # Skip __init__.py itself or sub-packages if any
                continue

            module_name_short = modname.split('.')[-1]
            # print(f"Attempting to load module: {modname}")
            try:
                module = importlib.import_module(modname)

                # Iterate over members of the imported module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and \
                       issubclass(obj, ColorTransferAlgorithm) and \
                       obj is not ColorTransferAlgorithm:

                        # Use a consistent key, e.g., lowercase class name
                        # or a dedicated property if algorithms define one.
                        # For now, class name lowercased.
                        alg_key = name.lower()

                        try:
                            self._algorithms[alg_key] = obj()
                            # print(f"  Successfully loaded and instantiated: {name} as '{alg_key}'")
                        except Exception as e:
                            print(f"  Error instantiating algorithm '{name}' from module '{modname}': {e}")
                            # Optionally, store the failed algorithm name/error

            except ImportError as e:
                # This handles cases where an algorithm file itself has an import error for its *own* dependencies
                # (e.g. a submodule like 'colortrans' not found by an algorithm in huehoppy.algorithms)
                # The individual algorithm wrappers already print info messages for their specific submodule issues.
                print(f"  Error importing module '{modname}': {e}. This module's algorithms may not be available.")
            except Exception as e:
                # Other unexpected errors during module import
                print(f"  Unexpected error loading module '{modname}': {e}")


    def list_available_algorithms(self) -> list[str]:
        """
        Returns a list of names of the successfully loaded algorithms.
        """
        return list(self._algorithms.keys())

    def get_algorithm(self, name: str) -> ColorTransferAlgorithm | None:
        """
        Retrieves an instantiated algorithm by its name.

        Args:
            name: The name (key) of the algorithm (typically lowercase class name).

        Returns:
            An instance of the ColorTransferAlgorithm, or None if not found.
        """
        return self._algorithms.get(name.lower())

if __name__ == '__main__':
    # Basic test
    print("Initializing AlgorithmManager...")
    manager = AlgorithmManager()
    print("\nAvailable algorithms:")
    for alg_name in manager.list_available_algorithms():
        print(f"- {alg_name}")

    # Test getting an algorithm
    reinhard_alg = manager.get_algorithm("reinhard")
    if reinhard_alg:
        print(f"\nRetrieved Reinhard: {reinhard_alg}")
    else:
        print("\nReinhard algorithm not found by manager.")

    lhm_alg = manager.get_algorithm("colortranslhm")
    if lhm_alg:
        print(f"\nRetrieved ColortransLHM: {lhm_alg}")
    else:
        print("\nColortransLHM algorithm not found by manager.")

    # Test a non-existent one
    non_existent = manager.get_algorithm("nonexistent")
    if not non_existent:
        print("\nCorrectly did not find 'nonexistent' algorithm.")
