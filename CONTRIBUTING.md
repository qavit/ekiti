# Contributing to Ekiti

Thank you for your interest in contributing to Ekiti! This guide will help you set up the development environment and contribute to the project.

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - A fast Python package installer and resolver

### Recommended Setup with uv

1. **Install uv** (if not already installed):
   ```bash
   curl -sSf https://astral.sh/uv/install.sh | sh
   ```
   This will install `uv` and add it to your PATH. Restart your terminal after installation.

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ekiti.git
   cd ekiti
   ```

3. **Create and activate virtual environment**:
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate the virtual environment
   # On Unix/macOS:
   source .venv/bin/activate
   # On Windows:
   # .venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   uv pip install -e ".[dev]"
   ```
   This will install all required dependencies, including development tools.

5. **Install pre-commit hooks** (recommended):
   ```bash
   pre-commit install
   ```

### Manual Setup (Alternative)

If you prefer not to use `uv`, you can use the traditional approach:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in development mode
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ekiti tests/
# View coverage in browser
python -m http.server --directory=htmlcov
```

## Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for code linting and formatting. Ruff is an extremely fast Python linter and formatter that can replace multiple tools like Flake8, isort, and Black.

### Key Features
- ⚡️ **Blazing fast** - 10-100x faster than existing linters
- 🛠️ **Drop-in compatibility** with common tools (Black, isort, flake8, etc.)
- 🔧 **Auto-fix** support for many rules
- 📦 **Single dependency** - no need to manage multiple tools

### Basic Commands

```bash
# Check for errors
ruff check .

# Fix all fixable errors
ruff check --fix .
# Format code (similar to Black)
ruff format .
# Type checking (requires mypy)
mypy src/
```

### Pre-commit Hook

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.7  # Use the latest version
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  
  # Use mypy for type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-PyYAML]
        args: [--strict, --implicit-reexport, --show-error-codes]
        files: ^src/ekiti/
```

## Submitting Code

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. Push to the remote repository:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request

## Code Review

- Ensure all tests pass
- Follow the code style guidelines
- Add appropriate documentation and tests
- Keep commit history clean and atomic

## Reporting Issues

If you find a bug or have a feature suggestion, please create an issue on GitHub. Make sure to include:

- A clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- Relevant logs or screenshots

Thank you for your contributions! 🎉
