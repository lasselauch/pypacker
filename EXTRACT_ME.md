# Extract This Directory

This `pypacker-standalone` directory contains a complete, ready-to-publish Python package.

## How to Create a New Repository

### Option 1: GitHub Web Interface

1. Create a new repository on GitHub named `pypacker`
2. Clone it locally:
   ```bash
   git clone https://github.com/yourusername/pypacker.git
   cd pypacker
   ```
3. Copy all contents from this directory (except this file):
   ```bash
   cp -r path/to/pypacker-standalone/* .
   rm EXTRACT_ME.md
   ```
4. Commit and push:
   ```bash
   git add .
   git commit -m "Initial commit: Python Script Packer v1.0.0"
   git push origin main
   ```

### Option 2: Command Line

```bash
# Navigate to where you want the new repo
cd ~/projects

# Copy this directory
cp -r path/to/pypacker-standalone pypacker
cd pypacker
rm EXTRACT_ME.md

# Initialize git
git init
git add .
git commit -m "Initial commit: Python Script Packer v1.0.0"

# Add remote and push
git remote add origin https://github.com/yourusername/pypacker.git
git branch -M main
git push -u origin main
```

## Publishing to PyPI

Once you have the repository set up, follow the instructions in `PUBLISHING.md` to publish to PyPI.

### Quick Publishing Steps

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Test on Test PyPI:
   ```bash
   twine upload --repository testpypi dist/*
   ```

4. Publish to PyPI:
   ```bash
   twine upload dist/*
   ```

See `PUBLISHING.md` for complete details.

## Testing Before Publishing

```bash
# Install in development mode
pip install -e .

# Test the CLI
pypacker --help

# Test with the example
cd examples/simple_plugin
pypacker 3.5 output.pyp my_product myplugin .
python output.pyp
```

## What's Included

- `pypacker/` - Main package code
- `examples/` - Working example project
- `pyproject.toml` - PyPI packaging configuration
- `README.md` - User documentation
- `CONTRIBUTING.md` - Contributor guidelines
- `PUBLISHING.md` - Publishing instructions
- `LICENSE` - MIT License
- `.gitignore` - Python-specific ignores

## Package Information

- **Name**: pypacker
- **Version**: 1.0.0
- **License**: MIT
- **Author**: Lasse Lauch
- **Python**: >=3.7 (tool itself)
- **Target**: Python 2.7 and 3.5+ (generated code)

Ready to publish! 🚀
