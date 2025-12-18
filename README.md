# Blender Distill

> **"Distilling the essence of complex .blend files."**

**Blender Distill** is a headless inspection toolkit designed for Technical Artists.
It allows you to extract logic, hierarchy, and driver dependencies from `.blend` files without launching the GUI.

## Features
- **Structure Distillation**: Dumps scene hierarchy, modifiers, and material nodes.
- **Logic Extraction**: Decodes driver expressions and custom property links.
- **Headless**: Runs purely via `blender --background`.

## Usage
```bash
# Extract Scene Structure
blender file.blend --background --python src/inspect.py
```

## License
MIT License
