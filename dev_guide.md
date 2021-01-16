# Guide to code style and development conventions for Prospect

## GitHub and git

- Branch liberally
- Use `jupytext` to put notebooks under better version control. `*.ipynb` added to .gitignore

## Imports

### Order

- `prospect` imports
- stdlib imports
- `sqlalchemy` imports
- all other imports (in order used)

### Scope

Imports should almost always be at the top level. The only things that should be imported within functions or methods are utilities that are used only within that function or method.

## Type hints

- Everything that can be type-hinted, should be
- Make sure to include a return hint, `-> Thing`, if appropriate
- Use `code` formatting when referring to objects

## Docstrings

- Use `"""`
- Use numpy-style
- Blank line before first code line

## Building block classes

### Arguments

- If type is `float`, make default a `float`, not an `int`

### Method argument order

- first argument is `name`
- next arguments are names referring to other building blocks (e.g., `survey_name`)
- shapes
- model parameters

### Model parameters

- type and default argument `Union[float, rv_frozen] = 1.0`

### SQL Table specifications

- table columns go first
- all `relationship` statements grouped together

## Testing

### Testing each building block

#### Test simplest version of object

- Test that the correct class of object is created
- Test that the object has all of the appropriate attributes
- Test that the attributes are of the correct types

#### Test factory methods

- Test that the correct class of object is created
- Test that the object has all of the appropriate attributes
- Test that the attributes are of the correct types

## Docs

### UML diagrams

To create UML diagrams, use `pyreverse` package. `pyreverse` is installed when you install `pylint`, but also requires `graphviz` if you want to write to image output formats. The following generates the UML diagram for only the current module.

```bash
cd prospect  # project folder, not package (aka src)
pyreverse -s 0 -a 0 prospect -o png
```

### Sphinx docs

Initial setup.

```bash
cd docs
sphinx-apidoc -F -o . ../prospect
```

#### Changes to default `conf.py`

Set path to:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

Change the extensions list as below. 

Notes:

- `sphinx.ext.viewcode` controls if docs generate links to actual sourcecode.
- `sphinx.ext.napoleon` parses numpy-style docstrings

```python
extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.viewcode',
    # 'sphinx.ext.todo',
    'sphinx.ext.napoleon',
]
```

Change html theme, if desired. Default is:

```python
html_theme = 'alabaster'
```
