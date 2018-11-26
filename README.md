# SurveySim
SurveySim is a set of tools for simulating archaeological field surveys.

## TODO:
- [ ] define data types used for each building block
- [ ] specify default values
- [ ] determine measures to calculate for any given simulation
- [ ] plan returns of the simulation 
- [ ] plan visualization methods

## Building blocks
SurveySim is designed around a few simple building blocks that can be customized (or not) to whatever degree the user
 requires.
 
 ### `Simulation` 
 A Simulation is receives all of the inputs and runs the digital survey. It also 
 
 ### `Area`
 The Area defines the spatial extent of the survey. Spatial aspects of the Assemblage and the SurveyStrategy are 
 placed within the Area.
 
 An Area can be defined with a simple rectangle or with more complex shapes from a shapefile.
 
 The surface visibility parameter is set on the Area either as a scalar value, a distribution, or with a 
 pre-calculated surface. 
 
 The Area has attributes like min/max bounds and area (as in m<sup>2</sup>).

 ```python
 from shapely.geometry import box
 import geopandas as gpd

 xmin=0; ymin=0; xmax=1; ymax=1
 rect = box(xmin, ymin, xmax, ymax)
 area1 = gpd.GeoDataFrame({'area_name':['area1'],
                           'visibility': [0.90],
                           'geometry': rect}, 
                          geometry='geometry')
 area1 
 ```
 |  | name | visibility | geometry |
 | :--: | --: | --------: | --------: |
 | **0** | 'area1'  | 0.90 | POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0) |

 ### `Assemblage` 
 The Assemblage represents the artifacts or other features-of-interest in an Area. The Assemblage needs to be able to
  handle multiple inputs because archaeologists are often interested in identifying more than one type of artifact or
  feature in their survey. SurveySim does this with Layers.
 
 #### `Layers`
 Each Layer of an Assemblage should be a homogeneous type of shape (e.g., points, lines, or polygons). The user can 
 ask SurveySim to place these shapes in various configurations (random, Poisson, Matern, etc.) with specified 
 densities or, in a case where the survey has already taken place, the user can provide their own shapefile(s).
 
 Each Layer is given a name that facilitates tracking and analysis through the simulation process.

 The user can assign a time penalty to a Layer that represents the amount of time added to the minimum search time (see below) for each artifact or feature observed in that Layer. This is designed to account for the fact that stopping to record, mark, or collect artifacts or features slows down the survey process.
 
 All Layers also have an ideal observation rate, which represents the frequency with which an artifact or feature will be
  recorded, assuming the following ideal conditions: 
  - It lies inside or intersect the Coverage (see below)
  - Surface visibility is 100%
  - The surveyor is highly skilled
  
 These assumptions are important to consider further. The ideal observation rate is specified here solely as a property
  of the materials (i.e., artifacts or features) themselves, unrelated to the distance from the observer, surface 
 visibility, or surveyor skill. These other factors are all accounted for in other parts of the simulation, so users 
 should avoid replicating that uncertainty here. For *most* Layers, this value should probably be 1.0 or close to 1
 .0, but there are some scenarios where you might want to consider an alternate value. For instance:
 - If the Layer represents extremely small artifacts (e.g., beads, tiny stone flakes) that are hard to observe even in 
 the best conditions.
 - If the Layer represents artifacts or features that are difficult to differentiate from the surface "background". For 
 example, in a gravelly area, ceramic sherds can be difficult to differentiate from rocks. A major caveat here is 
 that this "background noise" is sometimes considered in surface visibility estimations, so the user should take care
  not to duplicate that uncertainty if it is already accounted for in the simulation.

  ```python
  from numpy.random import random
  from shapely.geometry import Point
  import geopandas as gpd
  
  n = 3
  xrange=(0, 1); yrange=(0, 1)

  xs = (random(n) * (xrange[1] - xrange[0])) + xrange[0]
  ys = (random(n) * (yrange[1] - yrange[0])) + yrange[0]
  gds = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])

  ceramics = gpd.GeoDataFrame({'layer_name': ['ceramics'] * n,
                               'fid': [f'ceramics_{i}' for i in range(n)],
                               'time_penalty': [0.1] * n,
                               'ideal_obs_rate': [0.95] * n,
                               'geometry': gds},
                              geometry = 'geometry'
                             )
  ceramics
  ```
  
  |      | layer_name | fid | time_penalty | ideal_obs_rate | geometry |
  | :--: | ---: | --: | --------: | -------------: | -------: |
  | 0 | ceramics | ceramics_0 | 0.1 | 0.95 | POINT (0.7659078564803156 0.1877212286612516) |
  | 1 | ceramics | ceramics_1 | 0.1 | 0.95 | POINT (0.5184179878729432 0.08074126876487486) |
  | 2 | ceramics | ceramics_2 | 0.1 | 0.95 | POINT (0.296800501576222 0.73844029619897) |


  ```python
  n = 2
  xrange=(0, 1); yrange=(0, 1)

  xs = (random(n) * (xrange[1] - xrange[0])) + xrange[0]
  ys = (random(n) * (yrange[1] - yrange[0])) + yrange[0]
  gds = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])

  lithics = gpd.GeoDataFrame({'layer_name': ['lithics'] * n,
                              'fid': [f'lithics_{i}' for i in range(n)],
                              'time_penalty': [0.15] * n,
                              'ideal_obs_rate': [0.80] * n,
                              'geometry': gds},
                             geometry = 'geometry'
                            )
  lithics
  ```
  |      | layer_name | fid | time_penalty | ideal_obs_rate | geometry |
  | :--: | ---: | --: | --------: | -------------: | -------: |
  | 0 | lithics | lithics_0 | 0.15 | 0.8 | POINT (0.02430656162948697 0.6998436141265575) |
  | 1 | lithics | lithics_1 | 0.15 | 0.8 | POINT (0.2045555463799507 0.7795145855555298) |

  ```python
  assemblage = pd.concat([ceramics, lithics], ignore_index=True)
  assemblage
  ```
  |      | layer_name | fid | time_penalty | ideal_obs_rate | geometry |
  | :--: | ---: | --: | --------: | -------------: | -------: |
  | 0 | ceramics | ceramics_0 | 0.1 | 0.95 | POINT (0.7659078564803156 0.1877212286612516) |
  | 1 | ceramics | ceramics_1 | 0.1 | 0.95 | POINT (0.5184179878729432 0.08074126876487486) |
  | 2 | ceramics | ceramics_2 | 0.1 | 0.95 | POINT (0.296800501576222 0.73844029619897) |
  | 3 | lithics | lithics_0 | 0.15 | 0.8 | POINT (0.02430656162948697 0.6998436141265575) |
  | 4 | lithics | lithics_1 | 0.15 | 0.8 | POINT (0.2045555463799507 0.7795145855555298) |

 ### `Coverage`
 The Coverage is where the user defines how the survey will be set up. The user can define the shape of the survey 
 unit (transects, radial, quadrat, checkerboard, etc.) and the intervals at which they'd like them to be spaced. 
 Alternatively, they can specify the survey unit and the percent of the Area they'd like covered, and SurveySim will 
 generate a Coverage to fit.
 
 The Coverage also defines how an artifact or feature's distance from the survey unit impacts whether or not it is 
 discovered.

 The user can also specify an estimated minimum search time for a single survey unit. This should be an estimate of the amount of time it would take the most skilled surveyor to search a survey unit where they encountered no artifacts or features. This forms the baseline to which additional time is added. Time can be added for each artifact observed and/or based on the surveyor speed attribute (see below).
  
 #### `Transects`
 Transects are probably the most common type of coverage. They are represented in SurveySim by lines. The user will 
 also specify a buffer distance around the lines that represents the "sweep width". Artifacts or features within the 
 sweep width are "eligible" to be observed in the survey. Whether they are *actually* observed depends on the 
 the suite of all factors like ideal observation rate, surface visibility, and surveyor skill.

 
 #### `Radial`
 Radial survey units are regularly-spaced circles of a given radius. The radius is equivalent to the "sweep width" of a transect.

 #### `Quadrat`
 Quadrats are similar to Radial survey units except they are usually quadrilaterals (mostly typically, squares).

 #### `Checkerboard`
 A Checkerboard pattern is a special kind of quadrat-based survey.
 

 ### `Team`
 TODO: How to allocate surveyors across survey units? Proportionally? Randomly?

 The Team represents the surveyors who will carry out the simulated survey. The user can specify a skill level and a speed penalty for each surveyor. The skill level impacts the probability that an artifact or feature will be recorded (lower skill = more missed artifacts). The speed penalty adds extra time to both the Coverage's minimum survey time and the Layer's time penalty.
 
 In its most basic implementation, a Team would be made up of one surveyor with a skill level of 1.0 and a speed penalty of 0.0.
 
 In some cases though, it may be more appropriate to include surveyors of different skill levels and speeds. One situation where the user may want to specify surveyors of various skill levels and speeds would be where there was a high degree of difference between the least and most skilled team members. In a field school context, for example, it is often the case that there are a small number of very experienced archaeologists (PIs, TAs, etc.) and a larger number of inexperienced archaeologists (field school students, new volunteers, etc.). In that case, it may not be reasonable to assume a uniform skill level and speed.

```python
import pandas as pd

team = pd.DataFrame({'surveyor_type': ['pi', 'grad', 'undergrad', 'undergrad', 'undergrad'],
                     'skill': [1.0, 0.95, 0.85, 0.85, 0.85],
                     'speed_penalty': [0.0, 0.0, 0.2, 0.2, 0.2]
                    })

for stype in team['surveyor_type'].unique():
    stype_df = team.loc[team['surveyor_type']==stype, :]
    team.loc[stype_df.index, 'sid'] = [i for i in range(stype_df.shape[0])]

team['sid'] = team.apply(lambda x: x['surveyor_type'] + '_' + str(int(x['sid'])), axis=1)
team = team.loc[:, ['sid', 'surveyor_type', 'skill', 'speed_penalty']]

team
```
|      | sid | surveyor_type | skill | speed_penalty |
| :--: | --: | ------------: | ----: | ------------: |
| 0 | pi_0 | pi | 1.00 | 0.0 |
| 1 | grad_0 | grad | 0.95 | 0.0 |
| 2 | undergrad_0 | undergrad | 0.85 | 0.2 |
| 3	| undergrad_1 | undergrad | 0.85 | 0.2 |
| 4	| undergrad_2 | undergrad | 0.85 | 0.2 |	
