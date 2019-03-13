# SurveySim code style guide

## GitHub and git

Branch liberally

## Imports

### Order

- `surveysim` imports
- `sqlalchemy` imports
- stdlib imports
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
- space before first code line

## Building block classes

### Arguments

- If type is `float`, make default a `float`, not an `int`

### Method argument order

- first argument is `name`
- second argument is `sim`
- next arguments are names referring to other building blocks (e.g., `survey_name`)
- shapes
- model parameters

### Model parameters

- type and default argument `Union[float, rv_frozen] = 1.0`

### SQL Table specifications

- table columns go first
- all `relationship` statements grouped together

