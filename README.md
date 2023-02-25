# AlgoKit Beaker Template

This template provides a good starting point to build Beaker smart contracts productively.

This is the default template used by AlgoKit to initialise an Algorand smart contract project. It's a [Copier template](https://copier.readthedocs.io/en/stable/).

## Features

This template supports the following features:

* [Poetry](https://python-poetry.org/) for Python dependency management and virtual environment management
* Linting via [Ruff](https://github.com/charliermarsh/ruff) or [Flake8](https://flake8.pycqa.org/en/latest/)
* Formatting via [Black](https://github.com/psf/black)
* Type checking via [mypy](https://mypy-lang.org/)
* Testing via pytest (not yet used)
* Dependency vulnerability scanning via pip-audit (not yet used)
* VS Code configuration (linting, formatting, breakpoint debugging)
* dotenv (.env) file for configuration (not yet used)

Planned (future) features:

* Deployment and automated testing of the compiled smart contracts using TypeScript or Python
* Output stability tests of the teal output via pytest
* CI/CD pipeline using GitHub actions

# Getting started

Once the template is instantiated you can follow the [README.md](template_content/README.md.jinja) file to see instructions for how to use the template.
