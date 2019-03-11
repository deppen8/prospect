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

Everything that can be type-hinted, should be

## Building block classes

### Method argument order

- first argument is `name`
- second argument is `sim`
- next arguments are names referring to other building blocks (e.g., `survey_name`)
- shapes
- model parameters

### Model parameters

- type and default argument `Union[float, rv_frozen] = 1.0`

### Table specifications

- table columns go first
- all `relationship` statements grouped together
