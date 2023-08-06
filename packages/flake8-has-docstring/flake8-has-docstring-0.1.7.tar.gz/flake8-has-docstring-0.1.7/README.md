# flake8-has-docstring

A flake8 plugin that checks that functions have docstrings.

This package adds the following warnings:

- `UUG001`: An unused global variable.

There are no configuration options at this time.

The following functions are currently unchecked:

- Functions which are decorated with `@pytest.fixture`.
- Functions which are decorated with `@typing.overload`.
