# Contributing to pypacker

Thank you for considering contributing to pypacker! This document provides guidelines for contributing to the project.

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/pypacker.git
   cd pypacker
   ```

### Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Verify installation:
   ```bash
   pypacker --help
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-compression` - New features
- `fix/import-rewrite-bug` - Bug fixes
- `docs/improve-readme` - Documentation
- `refactor/cleanup-pack` - Code refactoring

### Code Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Keep functions focused and small
- Add docstrings to all public functions

### Testing

Test your changes thoroughly:

1. Test with Python 2.7 dialect:
   ```bash
   cd examples/simple_plugin
   pypacker 2.7 test_py27.pyp my_product myplugin .
   python2 test_py27.pyp
   ```

2. Test with Python 3.5+ dialect:
   ```bash
   pypacker 3.5 test_py35.pyp my_product myplugin .
   python test_py35.pyp
   ```

3. Test edge cases:
   - Empty modules
   - Nested packages
   - External dependencies
   - Invalid pack.list entries

### Documentation

- Update README.md if adding features
- Add examples for new functionality
- Update docstrings
- Add comments for complex logic

## Submitting Changes

### Commit Messages

Write clear commit messages:

```
Add support for relative imports

- Implement relative import detection
- Rewrite relative imports to absolute
- Add tests for relative imports
- Update documentation
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed explanation if needed
- List of changes with bullet points

### Pull Request Process

1. Update your fork:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your changes:
   ```bash
   git push origin feature/your-feature
   ```

3. Create Pull Request on GitHub:
   - Describe what changes you made
   - Reference any related issues
   - Add screenshots if relevant
   - Request review

4. Respond to feedback:
   - Make requested changes
   - Push updates to the same branch
   - Reply to comments

## Reporting Bugs

### Before Reporting

- Check if the bug is already reported
- Try the latest version
- Create a minimal reproduction case

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Create pack.list with '...'
2. Run command '...'
3. See error

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.10.5]
- pypacker version: [e.g. 1.0.0]

**Additional context**
Any other relevant information.
```

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Describe the problem you're trying to solve.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other relevant information.
```

## Development Guidelines

### Project Structure

```
pypacker/
├── __init__.py       # Package exports
├── __main__.py       # CLI entry point
└── pack.py           # Core packing logic
```

### Adding New Features

1. Discuss in an issue first
2. Create a feature branch
3. Implement the feature
4. Add tests and examples
5. Update documentation
6. Submit pull request

### Code Review

All submissions require review. We look for:
- Correctness
- Code quality
- Test coverage
- Documentation
- Backward compatibility

## Release Process

For maintainers:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release

## Questions?

- Open an issue for discussion
- Check existing issues and PRs
- Read the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
