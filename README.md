# huehoppy

Tool to transfer colors between images

- https://github.com/twardoch/huehoppy

## Current

Currently a temporary implementation that relies on

- https://github.com/ImmersiveMediaLaboratory/ColorTransferLib
- https://github.com/pengbo-learn/python-color-transfer
- https://github.com/dstein64/colortrans

## Future

The task is to create a new lib `huehoppy` that improves upon three existing color transfer libraries. The main problems are:

1. ColorTransferLib has good organization but fails completely if any dependency is missing
2. The other two libraries (python-color-transfer and colortrans) are simpler but less modular/extensible
3. All libraries make it hard to chain multiple algorithms together

The proposed solution is to create a new system that:

1. Loads algorithms independently - if one fails, others still work
2. Uses a clean, consistent API across all algorithms
3. Makes it easy to chain multiple algorithms together
4. Separates file I/O from the core algorithm logic
5. Lets users install only the dependencies they need

The architecture of `huehoppy` would use:

- A folder for each algorithm with its own dependencies listed
- A manager class that discovers and loads available algorithms
- A pipeline system for chaining algorithms
- Separate classes for handling different data types (images, meshes etc.)

This maintains good organization of `ColorTransferLib` while fixing its brittleness and adding new capabilities.
