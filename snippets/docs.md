# Creating documentation elements

## UML diagrams

To create UML diagrams, use `pyreverse` package. `pyreverse` is installed when you install `pylint`, but also requires `graphviz` if you want to write to image output formats. The following generates the UML diagram for only the current module.

```bash
cd prospect  # project folder, not package (aka src)
pyreverse -s 0 -a 0 prospect -o png
```

## Sphinx docs

Initial setup.

```bash
cd docs
sphinx-apidoc -F -o . ../prospect
```

### Changes to default `conf.py`

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
