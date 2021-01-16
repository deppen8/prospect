# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# %matplotlib inline
import prospect as ssim

# import geoplot as gplt
# import geoplot.crs as gcrs
import matplotlib.pyplot as plt
from scipy.stats import beta, truncnorm

import geopandas as gpd
import numpy as np
# -

# ## `Survey`

survey = ssim.Survey(name='demo_survey')

# ## `Area`

# ### From shapefile

shapefile_path = '../tests/test_data/shapefiles/areas/leiap_field1.shp'
area_from_shp = ssim.Area.from_shapefile(name='demo_area_from_shp', survey_name='demo_survey', path=shapefile_path, vis=beta(a=9, b=1))

area_from_shp.df.plot();

# ## Layer

# ### From shapefile

layer_shp_path = '../tests/test_data/shapefiles/layers/leiap_field1_points.shp'
layer_from_shp = ssim.Layer.from_shapefile(path=layer_shp_path, name='demo_layer_from_shp', area=area_from_shp,
                                           assemblage_name='demo_assemblage',
                                           time_penalty=beta(a=9, b=1),
                                           ideal_obs_rate=1.0
                                          )

layer_from_shp.df.plot();

# ### From Poisson point process

poisson_rate = 0.01
layer_from_poisson = ssim.Layer.from_poisson_points(rate=poisson_rate, name='demo_poisson_layer', area=area_from_shp,
                                                    assemblage_name='demo_assemblage', time_penalty=0.2, ideal_obs_rate=beta(9.5, 0.5)
                                                   )

layer_from_poisson.df.plot();

# ### From Thomas point process

parent_rate = 0.01
child_rate = 0.1
gauss = 10.0
layer_from_thomas = ssim.Layer.from_thomas_points(parent_rate=parent_rate, child_rate=child_rate, gauss_var = gauss,
                                                  name='demo_thomas_layer', area=area_from_shp, 
                                                  assemblage_name='demo_assemblage', time_penalty=0.15, ideal_obs_rate=1.0)

layer_from_thomas.df.plot();

# ### From Matern point process

parent_rate = 0.01
child_rate = 0.1
radius = 10.0
layer_from_matern = ssim.Layer.from_matern_points(parent_rate=parent_rate, child_rate=child_rate, radius = radius,
                                                  name='demo_matern_layer', area=area_from_shp, 
                                                  assemblage_name='demo_assemblage', time_penalty=beta(15, 85), ideal_obs_rate=1.0)

layer_from_matern.df.plot();

# ## `Assemblage`

assemblage = ssim.Assemblage(name='demo_assemblage', survey_name='demo_survey', area_name='demo_area_from_shp', 
                             layer_list=[layer_from_shp, layer_from_poisson, layer_from_thomas, layer_from_matern])

assemblage.df.plot();

# ## `Coverage`

# ### From transects

coverage_transects = ssim.Coverage.from_transects(name='demo_coverage_from_transects', area=area_from_shp, 
                                                  survey_name='demo_survey', spacing=10.0, sweep_width=2.0, orientation=0.0,
                                                  optimize_orient_by='area_coverage', orient_increment=4.0, orient_axis='short',
                                                  min_time_per_unit=5.0)

coverage_transects.df.plot();

# ## `Surveyor`

# ### Experts

expert = ssim.Surveyor(name='demo_expert', team_name='demo_team', surveyor_type='expert_person', skill=1.0, speed_penalty=0.0)

# ### Mid-level

mid1 = ssim.Surveyor(name='demo_mid1', team_name='demo_team', surveyor_type='mid_level_person', skill=0.9, speed_penalty=0.1)
mid2 = ssim.Surveyor(name='demo_mid2', team_name='demo_team', surveyor_type='mid_level_person', skill=0.8, speed_penalty=0.1)

# ### Novices

novice1 = ssim.Surveyor(name='demo_novice1', team_name='demo_team', surveyor_type='novice_person', skill=0.75, speed_penalty=0.2)
novice2 = ssim.Surveyor(name='demo_novice2', team_name='demo_team', surveyor_type='novice_person', skill=beta(7, 3), speed_penalty=0.2)
novice3 = ssim.Surveyor(name='demo_novice3', team_name='demo_team', surveyor_type='novice_person', skill=0.70, speed_penalty=0.25)

# ## `Team`

team_list = [expert, mid1, mid2, novice1, novice2, novice3]
team = ssim.Team(name='demo_team', survey_name='demo_survey', surveyor_list=team_list)

team.df

# +
from prospect.plotting import bb_plot

bb_plot(area_from_shp, assemblage, coverage_transects, figsize=(12,20))
# -

survey.add_bb(bb=[area_from_shp, assemblage, coverage_transects, team])

survey.run()

survey.discovery.head()

# +
# time_cols = ["time_penalty_obs", "search_time", "speed_penalty_obs"]
# per survey unit
# groupby survey_unit_name, mean search_time, sum time_penalty_obs, add speed_penalty_obs factor at the end
output.groupby('layer_name')

# per layer

# per surveyor
# total time
