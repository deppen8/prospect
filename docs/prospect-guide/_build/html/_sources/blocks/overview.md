Introduction
============

A simulated survey is made up of a series of building blocks. The `Survey` object requires the following top-level building blocks:

- `Area`: the spatial boundaries of the survey
- `Assemblage`: the artifacts or other features
- `Coverage`: the survey strategy
- `Team`: the individuals who will carry out the survey

There are also lower-level building blocks that can be used to construct the four top-level blocks.

- `Layer` and `Feature` blocks make up the `Assemblage`
- `SurveyUnit` blocks make up the `Coverage`
- `Surveyor` blocks make up the `Team`

Each building block is its own Python class which defines different parameters that are accounted for when the `Survey` is "run". The power of `prospect` comes from keeping many aspects of the building blocks constant while varying certain parameters or properties of interest.

The following sections are designed to introduce the parameters of a `prospect` simulation, some common non-`prospect` object types, and each of the simulation's building blocks.
