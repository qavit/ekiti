# Ekiti - Language Learning Flashcard App

A command-line application for learning vocabulary in multiple languages (Indonesian, German, Spanish, and more). Remember words better with Ekiti (會記得)!

## Features

### Core Features
- **Multiple Languages Support**:
  - Indonesian — *Bahasa Indonesia*
  - German — *Deutsch*
  - Spanish — *Español*
  - Taigi — *台語*
  - (More to come!)
- **Learning Modes**:
  - **Spelling Mode**: Type the correct translation
  - **Multiple Choice Mode**: Choose the correct translation from options
- **Flexible Testing**:
  - Target language → English
  - English → Target language
  - Additional info (example sentences, gender, collocations) → Word
  - Word → Additional info
- **Rich Vocabulary Entries**:
  - Word in target language
  - English translation
  - Example sentences
  - Grammatical gender (for languages that use it)
  - Collocations and usage notes
  - Custom tags and categories

### Technical Stack

### Current Stack
- **Language**: Python 3.8+
- **Core Dependencies**:
  - `typer` - CLI interface
  - `rich` - Beautiful terminal output
  - `pydantic` - Data validation
  - `pyyaml` - Data serialization
  - `sqlmodel` - SQL database with Pydantic models
  - `click` - Advanced CLI features
  - `ruff` - Linting and code formatting

### Future Considerations
- **Frontend**:
  - Textual or Textual-Web for TUI
  - PyQt/PySide for desktop GUI
  - Flutter for cross-platform mobile
- **Backend**:
  - FastAPI for web services
  - PostgreSQL for production database
  - Redis for caching
- **Deployment**:
  - Docker for containerization
  - GitHub Actions for CI/CD
  - PyPI for package distribution

## Project Structure

```
ekiti/
├── README.md
├── CONTRIBUTING.md    # Contribution guidelines
├── pyproject.toml     # Project configuration
├── ruff.toml          # Ruff configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── src/               # Source code
│   └── ekiti/         # Main package
│       ├── __init__.py
│       ├── cli/        # Command-line interface
│       ├── core/       # Core functionality
│       └── models/     # Data models
└── data/              # Data files
    └── vocabularies/  # Vocabulary files
```

## Contributing

We welcome and appreciate all contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setting up the development environment, submitting code, and contribution guidelines.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ekiti.git
   cd ekiti
   ```

2. **Install with uv (recommended)**:
   ```bash
   uv pip install -e .
   ```

   Or with pip:
   ```bash
   pip install -e .
   ```

### Usage

```bash
# Start the application
python -m ekiti

# Start with a specific language
python -m ekiti --language german

# Choose a specific mode
python -m ekiti --mode spelling
```

## Data Storage

### Local Storage (Initial Implementation)
- **Format**: YAML/JSON files in `~/.config/ekiti/`
- **Structure**:
  ```yaml
  # Example entry
  - word: "Buch"
    language: "german"
    translations:
      en: "book"
    details:
      gender: "n"  # n for neuter
      plural: "Bücher"
    examples:
      - sentence: "Ich lese ein Buch."  # Example sentence
        en: "I'm reading a book."       # Translation
    tags: ["noun", "A1"]
    created_at: 2025-06-01
    last_reviewed: 2025-06-01
    difficulty: 2.5  # 1-5 scale
  ```

### Future Cloud Storage Options
- **SQLite** for local database
- **Firebase/Firestore** for cross-device sync
- **Self-hosted** backend (FastAPI/Django) for full control
- **Git** for version control of vocabulary lists

## Future Enhancements
- [ ] Add progress tracking
- [ ] Implement spaced repetition algorithm
- [ ] Add more languages
- [ ] Support for custom vocabulary lists
- [ ] GUI version
- [ ] Mobile app

## License
[MIT License](LICENSE)
