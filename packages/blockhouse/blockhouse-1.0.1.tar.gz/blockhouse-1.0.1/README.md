## Guide doc for Packaging SDK API for PyPI Deployment

sdk.py is for interacting with the JSONPlaceholder API. This SDK provides functions to fetch todos, posts, comments,
albums, photos, and users. It supports both library usage and command-line interface (CLI) for quick data access.

## Table of Contents
1. Features
2. Installation
3. Usage
4. Development and Packaging
5. Building the Package
6. Publishing to TestPyPI and PyPI
7. Testing the Package Locally
8. Automating Deployment with GitHub Actions
9. License
10. Contributing
11. Support


## Features
- Fetch todos, posts, comments, albums, photos, and users from JSONPlaceholder.
- Command-line support to quickly access data.
- Scalable and reusable in other Python projects.
- Simple installation using pip.
  
## Installation

To install the package after publishing it to PyPI:

```bash
pip install sdk-api-package
```
For local testing before deployment, install the package from your local dist/ folder:

```bash
pip install dist/sdk_api_package-0.1.0-py3-none-any.whl
```

## Usage

Using as a Python Library
```python

from sdk import get_todos, get_users

# Fetch and print all todos
get_todos()

# Fetch and print all users
get_users()
```

Using the Command-Line Interface (CLI)
```bash

python -m sdk [command] [id]
```

## Available Commands:
todos [user_id] – Fetch todos for a specific user or all users.

posts [user_id] – Fetch posts for a specific user or all users.

comments [post_id] – Fetch comments for a specific post or all posts.

albums [user_id] – Fetch albums for a specific user or all albums.

photos [album_id] – Fetch photos for a specific album or all albums.

users – Fetch and print all users.

## Examples:
```bash

# Fetch all todos
python -m sdk todos

# Fetch posts for user ID 2
python -m sdk posts 2
```

## Development and Packaging
Project Structure:
```perl
Copy code
sdk-package/
│
├── PythonSDK/
│   ├── __init__.py          # Initialize package
│   └── sdk.py               # Your SDK code
│
├── LICENSE                  # License information
├── README.md                # Documentation
├── setup.cfg                # Package metadata and configurations
├── pyproject.toml           # Build system configurations
├── MANIFEST.in              # Optional: Include non-code files
└── dist/                    # Distribution files after building
```

# Building the Package

Install the required tools:

```bash
pip install build
```

Build the package:

```bash
python -m build
```
This will create .tar.gz and .whl files in the dist/ directory.

## Publishing to TestPyPI and PyPI
Create an account on PyPI and TestPyPI.

1. Install Twine:

```bash
pip install twine
```

2. Upload to TestPyPI:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

3. Upload to PyPI:

```bash
twine upload dist/*
```

Verify the package on PyPI or TestPyPI.

## Testing the Package Locally
After building the package, test it locally:

1. Install the package:

```bash
pip install dist/sdk_api_package-0.1.0-py3-none-any.whl
```

2. Test the library:

```python
from sdk import get_users
get_users()
```

## Automating Deployment with GitHub Actions
You can automate the deployment process using GitHub Actions.

Create a .github/workflows/python-publish.yml file:

```yaml
name: Publish Python Package

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.x

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          python -m build
          twine upload dist/*
```

## Add PyPI Token to GitHub Secrets:

Go to your GitHub repository.
Navigate to Settings > Secrets > Actions.
Add a new secret with the name PYPI_API_TOKEN and paste your PyPI token.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Support
If you encounter any issues or have questions, feel free to open an issue on GitHub.

## Changelog
Version 0.1.0
Initial release with:
Functions for todos, posts, comments, albums, photos, and users
Command-line interface (CLI) support
