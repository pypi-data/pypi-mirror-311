<p align="center">
  <img src="docs/assets/logo.png" alt="KairosML" width="300" />
</p>

# KairosML - An open-source causal AI library

## Open source roadmap

-   [ ] Update documentation to be user-friendly
-   [ ] Thorough example notebooks
-   [ ] High test coverage (including statistical tests)
-   [ ] CI pipeline/branch strategy
-   [ ] PyPI package
-   [ ] Code coverage badge
-   [ ] Contribution guide
-   [ ] License
-   [ ] Formatting rules/vscode settings
-   [ ] Code polishing (comments, docstrings, minor refactoring etc.)
-   [ ] Clean dependencies
-   [ ] Improve plotting functionality (make visuals more appealing)
-   [ ] matplotlib colour scheme
-   [ ] Support for categorical nodes
-   [ ] Support for model fitting diagnostics
-   [ ] Feature roadmap

This is the Python library for the core causal AI functionality of Causa products. It's primarily used in the CausaDB server, but can also be used in demo apps and other projects.

We've separated the core functionality from the server to make it easier to use in other projects, to improve development speed, and to make it easier to maintain and document.

## File Structure

The library is organized into the following directories:

-   `kairosml`: The main library code.
-   `tests`: Unit tests for the library.
-   `notebooks`: Jupyter notebooks for testing and development.

## Roadmap

We should do test-driven development.

Model should just be called `Model`. It should handle only fitting and forward pass. Create separate classes for data loading, querying, diagnostics, etc. Maybe separate functionality like:

```python

model = Model()
model.fit(data)

model.query.simulate_action()
```

Not sure how to attach query like this.

## Testing

To run the tests, use the following command:

```bash
make test
```

You can view the test coverage report by running:

```bash
make coverage
```

## Commands

-   `make test` - Run the test suite located in the `tests` directory
-   `make coverage` - Open the coverage report in your browser (only available after running `make test`)
-   `make docs` - Build the documentation
