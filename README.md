# python-cli

[![CI](https://img.shields.io/badge/ci-passing-brightgreen)](https://github.com/Enzim3-sudo/python-cli/actions)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A simple Python CLI template for learning open-source contributions.

## Quick Start

### Clone the repository

```bash
git clone https://github.com/Enzim3-sudo/python-cli.git
cd python-cli
```

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install the project

```bash
pip install -e .
```

### Run the application

```bash
python -m python_cli.main --name "John Doe"
```

Example output:

```text
Hello, John Doe!
```

### Display available options

```bash
python -m python_cli.main --help
```

## Resources

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [ONBOARDING.md](ONBOARDING.md)
- [GUIDE_GOOD_FIRST_ISSUES.md](GUIDE_GOOD_FIRST_ISSUES.md)

## Development

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

(or `pip install pytest flake8`)

Run tests:

```bash
pytest
```

Run linter:

```bash
flake8 src
```
