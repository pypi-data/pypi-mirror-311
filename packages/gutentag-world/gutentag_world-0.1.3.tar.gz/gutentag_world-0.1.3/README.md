# Gutentag, World

`gutentag_world` is a simple Python package that provides a single function to print "Hello, World!" to the console. It's perfect for learning how to create and distribute Python packages.

## Features

- Prints "Gutentag, World!" to the console.

## Installation

You can install the package from the source distribution:

1. Clone or download the repository.
2. Navigate to the package directory where `pyproject.toml` is located.
3. Install the package using pip:

```bash
pip install .
```

## Usage

After installing the package, you can import and use the say_hello function:

```python
from hello_package import say_hello

say_hello()
```

This will output:

```sh
Gutentag, World!
```

## Development

To build and install the package locally for development:

1. Clone the repository.
2. Navigate to the package directory.
3. Install the package in editable mode:

```bash
pip install -e .
```

## Contributing

Contributions are welcome! Here’s how you can help:

1. Fork the repository: Click the “Fork” button at the top of this page.
2. Clone your fork:

```bash
git clone https://github.com/your-username/gutentag_world.git
```

3. Create a new branch

```bash
git checkout -b feature-name
```

4. Make your changes and commit them:

```bash
git add .
git commit -m "Describe your changes"
```

5. Push your changes to your fork:

```bash
git push origin feature-name
```

6. Submit a pull request: Go to the original repository on GitHub and open a pull request.

## Guidelines

- Write clear commit messages.
- Follow PEP 8 style guidelines for Python code.
- Ensure the package builds and works as expected before submitting changes.
- If adding a new feature, update the documentation in this `README.md`.

## License

This project is licensed under the MIT License.

## Author

Sam Gutentag
