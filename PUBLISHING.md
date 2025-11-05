# Publishing to PyPI

This guide walks you through publishing pypacker to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - [Test PyPI](https://test.pypi.org/account/register/) (for testing)
   - [PyPI](https://pypi.org/account/register/) (for production)

2. **API Tokens**: Generate API tokens for automated uploads:
   - Go to Account Settings → API tokens
   - Create a new token with scope for the project
   - Save the token securely

3. **Install Build Tools**:
   ```bash
   pip install --upgrade build twine
   ```

## Step 1: Prepare the Package

### Update Version Number

Edit `pyproject.toml` and update the version:

```toml
[project]
version = "1.0.1"  # Increment this
```

### Verify Package Metadata

Ensure all metadata is correct in `pyproject.toml`:
- Name, description, authors
- License, keywords, classifiers
- URLs (homepage, repository, issues)

### Clean Previous Builds

```bash
rm -rf dist/ build/ *.egg-info
```

## Step 2: Build the Distribution

Build both source distribution and wheel:

```bash
python -m build
```

This creates:
- `dist/pypacker-X.Y.Z.tar.gz` (source distribution)
- `dist/pypacker-X.Y.Z-py3-none-any.whl` (wheel)

### Verify Build

Check the built distributions:

```bash
ls -lh dist/
```

Inspect the contents:

```bash
tar -tzf dist/pypacker-*.tar.gz
unzip -l dist/pypacker-*.whl
```

## Step 3: Test on Test PyPI

### Upload to Test PyPI

```bash
twine upload --repository testpypi dist/*
```

Or with token:

```bash
twine upload --repository testpypi dist/* \
  --username __token__ \
  --password pypi-AgEIcHlwaS5vcmc...
```

### Test Installation

Install from Test PyPI in a fresh environment:

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ pypacker

# Test it works
pypacker --help

# Clean up
deactivate
rm -rf test_env
```

### Test the Example

```bash
cd examples/simple_plugin
pypacker 3.5 test_output.pyp my_product myplugin .
python test_output.pyp
```

## Step 4: Publish to Production PyPI

### Final Checks

- [ ] All tests pass
- [ ] Example works correctly
- [ ] Documentation is up to date
- [ ] Version number is correct
- [ ] CHANGELOG updated
- [ ] Git tag created

### Create Git Tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Upload to PyPI

```bash
twine upload dist/*
```

Or with token:

```bash
twine upload dist/* \
  --username __token__ \
  --password pypi-AgEIcHlwaS5vcmc...
```

### Verify on PyPI

1. Visit https://pypi.org/project/pypacker/
2. Check that metadata is correct
3. Verify README renders properly
4. Test installation: `pip install pypacker`

## Step 5: Post-Release

### Update Documentation

Update README with the new version number and any changes.

### Announce Release

- Create GitHub release from the tag
- Post in relevant communities
- Update any dependent projects

### Monitor

- Watch for issues on GitHub
- Monitor download statistics
- Check for security vulnerabilities

## Configuration Files

### ~/.pypirc

Create this file for easier uploads:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

Set proper permissions:

```bash
chmod 600 ~/.pypirc
```

## Troubleshooting

### "File already exists" Error

PyPI doesn't allow re-uploading the same version. You must:
1. Increment the version number in `pyproject.toml`
2. Rebuild: `python -m build`
3. Upload again

### Import Errors After Installation

Ensure your package structure is correct:
- `__init__.py` files present
- Package listed in `pyproject.toml`
- No circular imports

### README Not Rendering

- Ensure README.md uses standard Markdown
- Check for unsupported syntax
- Validate with: `twine check dist/*`

### Token Authentication Issues

- Ensure token has correct scope
- Use `__token__` as username (exactly)
- Check token hasn't expired

## CI/CD Automation (Optional)

### GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build
        run: python -m build
      - name: Publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Add `PYPI_API_TOKEN` to repository secrets.

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- MAJOR: Incompatible API changes
- MINOR: New functionality, backward compatible
- PATCH: Bug fixes, backward compatible

Examples:
- `1.0.0` - Initial release
- `1.0.1` - Bug fix
- `1.1.0` - New feature
- `2.0.0` - Breaking changes

## Checklist for Each Release

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md
- [ ] Run all tests
- [ ] Update documentation
- [ ] Clean old builds: `rm -rf dist/ build/`
- [ ] Build: `python -m build`
- [ ] Check: `twine check dist/*`
- [ ] Test on Test PyPI
- [ ] Create git tag: `git tag v1.0.0`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub release
- [ ] Test installation: `pip install pypacker`
- [ ] Verify on PyPI website

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)
