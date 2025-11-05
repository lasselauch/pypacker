# pypacker

A Python tool for bundling multiple Python modules into single executable scripts. Perfect for creating portable plugins for applications like Cinema 4D, Houdini, or any environment where you need to distribute Python code as a single file.

## Features

- 🎯 **Single File Distribution**: Bundle your entire Python project into one `.pyp` file
- 🐍 **Dual Python Support**: Generates code for both Python 2.7 and 3.5+ environments
- 📦 **Dependency Resolution**: Automatically resolves and packs nested module dependencies
- 🔄 **Import Rewriting**: Automatically rewrites imports to use a custom namespace
- 🌐 **No Runtime Dependencies**: Generated scripts are self-contained
- 🚀 **Fast & Lightweight**: Pure Python implementation, no external tools required

## Installation

### From PyPI (recommended)

```bash
pip install pypacker
```

### From Source

```bash
git clone https://github.com/lasselauch/pypacker.git
cd pypacker
pip install -e .
```

## Quick Start

### 1. Prepare Your Project

Create a `pack.list` file in your module directory:

```
.submodule1
.submodule2
.utils.helper
external_dependency
.
```

Ensure your main module has a `__main__.py` file.

### 2. Run the Packer

```bash
pypacker 3.5 output.pyp my_product my_module ./src
```

### 3. Distribute

Your bundled script is ready to distribute as a single file!

## Usage

### Command Line Interface

```bash
pypacker <dialect> <output> <product-name> <module-name> <library-path> [...]
```

**Parameters:**

- `dialect`: Target Python version (`2.7` or `3.5`)
- `output`: Output file path (typically `.pyp` or `.py`)
- `product-name`: Namespace for packed modules (use `*` for random name)
- `module-name`: Name of the main module to pack
- `library-path`: One or more paths to search for libraries

**Example:**

```bash
pypacker 3.5 ./dist/plugin.pyp my_plugin my_module ./src ./libs
```

### Python API

```python
from pypacker import pack

# Pack modules programmatically
packed_code = pack(
    dialect='3.5',
    product_name='my_product',
    library_name='my_module',
    library_paths=['./src', './libs']
)

# Write to file
with open('output.pyp', 'w') as f:
    f.write(packed_code)
```

## Pack List Format

The `pack.list` file defines what to include in your bundle:

### Local Modules

Lines starting with `.` reference local modules:

```
.mymodule           # References ./mymodule.py or ./mymodule/__init__.py
.utils.helper       # References ./utils/helper.py
.libs.              # References ./libs/__init__.py (package)
```

### External Libraries

Lines without `.` reference other libraries (which must have their own `pack.list`):

```
external_lib        # References external_lib/ directory
```

### Complete Example

```
# Local modules
.core
.utils.parser
.utils.formatter

# External dependencies
shared_library

# Package marker
.
```

## How It Works

1. **Reading**: Parses `pack.list` to identify dependencies
2. **Resolving**: Recursively finds all referenced modules
3. **Embedding**: Embeds module source code as strings
4. **Injecting**: Generates code to inject modules into `sys.modules`
5. **Rewriting**: Rewrites imports to use custom namespace
6. **Assembling**: Combines everything into a single executable script

### Generated Structure

The packed script contains three main sections:

1. **Allocation**: Creates module objects in `sys.modules`
2. **Linking**: Sets up parent-child module relationships
3. **Loading**: Executes module code to populate namespaces

## Advanced Features

### Custom Pack Location

Add a marker comment in your `__main__.py` to control where modules are injected:

```python
import sys

# !!! PACK HERE !!!

def main():
    # Your code here
```

Without the marker, modules are injected at the start of the file.

### Global Variables

Share variables across all packed modules using `_packer_global_vars`:

```python
_packer_global_vars = {
    '__plugin_directory__': '/path/to/plugin',
    'DEBUG': True,
    'logger': my_logger_instance,
}
```

These variables will be available in all packed modules.

### Random Product Names

Use `*` as the product name to generate a random namespace:

```bash
pypacker 3.5 output.pyp "*" my_module ./src
```

This prevents naming conflicts when multiple packed scripts run together.

## Real-World Example

See the [examples/](examples/) directory for complete working examples, including:

- Simple plugin structure
- Multi-module projects
- Cinema 4D plugin bundling

## Python 2.7 vs 3.5+ Differences

### Python 2.7 Output

```python
import sys, imp
sys.modules["product.module"] = imp.new_module("product.module")
exec code in sys.modules["product.module"].__dict__
```

### Python 3.5+ Output

```python
import sys, importlib.util
sys.modules["product.module"] = importlib.util.module_from_spec(...)
exec(code, sys.modules["product.module"].__dict__)
```

## Common Use Cases

- **Cinema 4D Plugins**: Bundle plugins into `.pyp` files
- **Houdini Digital Assets**: Embed Python code in HDAs
- **Nuke Scripts**: Create portable gizmos and tools
- **Standalone Tools**: Distribute tools as single files
- **Protected Code**: Combine with code obfuscation tools

## Limitations

- Does not handle C extensions or binary modules
- Imports must be simple (`import module` form)
- Dynamic imports (`__import__()`) are not rewritten
- Relative imports within packed modules need special handling

## Publishing to PyPI

This package is published on PyPI. To publish updates:

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Upload to PyPI
twine upload dist/*
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Comparison with Alternatives

| Tool | Language | Python 2 | Python 3 | Size | Dependencies |
|------|----------|----------|----------|------|--------------|
| pypacker | Python | ✅ | ✅ | ~15KB | None |
| PyInstaller | Python | ✅ | ✅ | Large | Many |
| cx_Freeze | Python | ✅ | ✅ | Large | Many |
| zipapp | Python | ❌ | ✅ | Medium | stdlib |

pypacker is designed specifically for embedding scripts in host applications, not creating standalone executables.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Credits

This is a Python port of the original npm [pypacker](https://www.npmjs.com/package/pypacker) tool, maintaining compatibility with its output format while eliminating the Node.js dependency.

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/lasselauch/pypacker/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/lasselauch/pypacker/discussions)
- 📧 **Email**: lasse@lasselauch.com

## Changelog

### v1.0.0 (2025-01-XX)

- Initial release
- Python 2.7 and 3.5+ support
- Recursive dependency resolution
- Import rewriting
- Command-line interface
- Python API

---

Made with ❤️ for the Python community
