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

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# # `prospect` demo
#
# Jacob Deppen, DigAR Lab, 26 April 2019

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Overview
#
# Simulated surveys are made of four building blocks, some of which have their own building blocks.
# 1. `Area`: spatial extent
# 2. `Assemblage`: artifacts/features
#     - Made up of multiple `Layer` objects
#         - A `Layer` is composed of `Feature` objects
# 3. `Coverage`: survey strategy
#     - Made up of multiple `SurveyUnit` objects
# 4. `Team`: people
#     - Made up of multiple `Surveyor` objects

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Import Python packages

# + {"slideshow": {"slide_type": "fragment"}}
# %matplotlib inline
import prospect as pspt
from prospect.utils import beta, truncnorm

import matplotlib.pyplot as plt

import geopandas as gpd
import numpy as np

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create two `Survey` objects
#
# `transect_survey` where the units are transects
#
# `radial_survey` where the units are circular patches like the LEIA Project survey

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey = pspt.Survey(name='transect_survey')
radial_survey = pspt.Survey(name='radial_survey')

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create `Area` from shapefile

# + {"slideshow": {"slide_type": "fragment"}}
shapefile_path = '../tests/test_data/shapefiles/areas/leiap_field1.shp'
area_from_shp = pspt.Area.from_shapefile(
    name='area_from_shp', 
#     survey_name='deprecated', 
    path=shapefile_path, 
    vis=beta(a=9, b=1)
)

# + {"slideshow": {"slide_type": "fragment"}, "cell_type": "markdown"}
# Also available:
# - Create from any `shapely` shape
# - Create a square `Area` by specifying the desired area value

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Explore `area_from_shp`

# + {"slideshow": {"slide_type": "fragment"}}
area_from_shp.__dict__

# + {"slideshow": {"slide_type": "fragment"}}
area_from_shp.df

# + {"slideshow": {"slide_type": "fragment"}}
type(area_from_shp.df)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Visualize with generic `geopandas` plot

# + {"slideshow": {"slide_type": "fragment"}}
area_from_shp.df.plot()
plt.savefig("../outputs/uw_gis_symp/area_demo.png")

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create four `Layer` objects
# Think of them as four different artifact types (e.g., ceramics, lithics, metal, and bones)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ### Layer 1 from a shapefile

# + {"slideshow": {"slide_type": "fragment"}}
layer_shp_path = '../tests/test_data/shapefiles/layers/leiap_field1_points.shp'
layer_from_shp = pspt.Layer.from_shapefile(
    path=layer_shp_path, 
    name='ceramics', 
    area=area_from_shp,
    assemblage_name='iron_age',
    time_penalty=truncnorm(mean=30, sd=10, lower=5, upper=600),
    ideal_obs_rate=1.0
)

# + {"slideshow": {"slide_type": "fragment"}}
layer_from_shp.df.plot()

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ### Layer 2 from a Poisson point process

# + {"slideshow": {"slide_type": "fragment"}}
poisson_rate = 0.01
layer_from_poisson = pspt.Layer.from_poisson_points(
    rate=poisson_rate, 
    name='lithics', 
    area=area_from_shp,
    assemblage_name='iron_age', 
    time_penalty=truncnorm(mean=30, sd=10, lower=5, upper=600), 
    ideal_obs_rate=beta(9.5, 0.5)
)

# + {"slideshow": {"slide_type": "fragment"}}
layer_from_poisson.df.plot()
plt.savefig("poisson_demo.png");

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ### Layer 3 from a Thomas point process

# + {"slideshow": {"slide_type": "fragment"}}
parent_rate = 0.01
child_rate = 0.1
gauss = 10.0
layer_from_thomas = pspt.Layer.from_thomas_points(
    parent_rate=parent_rate, 
    child_rate=child_rate, 
    gauss_var = gauss,
    name='metals', 
    area=area_from_shp, 
    assemblage_name='iron_age', 
    time_penalty=truncnorm(mean=20, sd=5, lower=2, upper=600), 
    ideal_obs_rate=1.0
)

# + {"slideshow": {"slide_type": "fragment"}}
layer_from_thomas.df.plot();

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ### Layer 4 from a Matern point process

# + {"slideshow": {"slide_type": "fragment"}}
parent_rate = 0.01
child_rate = 0.1
radius = 10.0
layer_from_matern = pspt.Layer.from_matern_points(
    parent_rate=parent_rate, 
    child_rate=child_rate, 
    radius = radius,
    name='bones', 
    area=area_from_shp, 
    assemblage_name='iron_age', 
    time_penalty=truncnorm(mean=30, sd=10, lower=5, upper=600), 
    ideal_obs_rate=1.0
)

# + {"slideshow": {"slide_type": "fragment"}}
layer_from_matern.df.plot();

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# Can also create `Layer` from:
# - a list of `Feature` objects
# - pseudorandom point coordinates

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Compile the `Layer` objects into an `Assemblage`

# + {"slideshow": {"slide_type": "fragment"}}
iron_age_assemblage = pspt.Assemblage(
    name='iron_age', 
#     survey_name='deprecated', 
    area_name='area_from_shp', 
    layer_list=[layer_from_shp, layer_from_poisson, layer_from_thomas, layer_from_matern]
)

# + {"slideshow": {"slide_type": "fragment"}}
iron_age_assemblage.df.plot();

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Build two `Coverage` objects
#
# - One for transects
# - One for radial units

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create transect `Coverage`

# + {"slideshow": {"slide_type": "fragment"}}
coverage_transects = pspt.Coverage.from_transects(
    name='transects', 
    area=area_from_shp, 
#     survey_name='deprecated', 
    spacing=10.0, 
    sweep_width=2.0, 
    orientation=0.0,
    optimize_orient_by='area_coverage', # area_orient aligns w/orient_axis
    orient_increment=4.0,
    orient_axis='short',
    min_time_per_unit=5.0
)

# + {"slideshow": {"slide_type": "slide"}}
coverage_transects.df.plot()
plt.savefig("../outputs/uw_gis_symp/coverage_demo.png")

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create radial `Coverage`

# + {"slideshow": {"slide_type": "fragment"}}
coverage_radials = pspt.Coverage.from_radials(
    name='radials',
    area=area_from_shp,
#     survey_name="deprecated",
    spacing=10.0, 
    radius=2.0, 
    orientation=0.0,
    optimize_orient_by='area_coverage', 
    orient_increment=4.0, 
    orient_axis='short',
    min_time_per_unit=60
)

# + {"slideshow": {"slide_type": "slide"}}
coverage_radials.df.plot()
plt.savefig("../outputs/uw_gis_symp/radials_demo.png");

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# Can also create `Coverage` from:
# - shapefile
# - `geopandas GeoDataFrame`

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create six `Surveyor` objects
#
# Best to simply create each person by hand

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Experts

# + {"slideshow": {"slide_type": "fragment"}}
expert = pspt.Surveyor(
    name='expert', 
    team_name='leiap_team', 
    surveyor_type='expert_person', 
    skill=1.0, 
    speed_penalty=0.0
)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Mid-level

# + {"slideshow": {"slide_type": "fragment"}}
mid1 = pspt.Surveyor(
    name='mid1', 
    team_name='leiap_team', 
    surveyor_type='mid_level_person', 
    skill=0.9, 
    speed_penalty=0.1
)
mid2 = pspt.Surveyor(
    name='mid2',
    team_name='leiap_team', 
    surveyor_type='mid_level_person', 
    skill=0.8, 
    speed_penalty=0.1
)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Novices

# + {"slideshow": {"slide_type": "fragment"}}
novice1 = pspt.Surveyor(
    name='novice1', 
    team_name='leiap_team', 
    surveyor_type='novice_person', 
    skill=0.75, 
    speed_penalty=0.2
)
novice2 = pspt.Surveyor(
    name='novice2', 
    team_name='leiap_team', 
    surveyor_type='novice_person', 
    skill=beta(7, 3), 
    speed_penalty=0.2
)
novice3 = pspt.Surveyor(
    name='novice3', 
    team_name='leiap_team', 
    surveyor_type='novice_person', 
    skill=0.70, 
    speed_penalty=0.25
)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Create `Team` from `Surveyor` objects

# + {"slideshow": {"slide_type": "fragment"}}
team_list = [expert, mid1, mid2, novice1, novice2, novice3]
leiap_team = pspt.Team(
    name='leiap_team', 
#     survey_name='deprecated', 
    surveyor_list=team_list,
    assignment='naive'
)

# + {"slideshow": {"slide_type": "fragment"}}
leiap_team.df

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Plot all spatial building blocks together

# + {"slideshow": {"slide_type": "fragment"}}
from prospect.plotting import bb_plot
bb_plot(area_from_shp, iron_age_assemblage, coverage_transects, figsize=(20,20))

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Add building blocks to their respective `Survey` objects

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.add_bb(bb=[area_from_shp, iron_age_assemblage, coverage_transects, leiap_team])
radial_survey.add_bb(bb=[area_from_shp, iron_age_assemblage, coverage_radials, leiap_team])

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Run the transect survey!!!

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.run(n_runs=100)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## What happened?
#
# With `Assemblage`
# 1. Extract `ideal_obs_rate` values (if distribution, select from it) -> `obs_rate`
# 2. Extract feature `time_penalty` values (if distribution, select from it) -> `time_penalty_obs`
# 3. Extract surface `vis` values (if distribution, select from it) -> `vis_obs`
#      - TODO: if raster, extract value from raster
#
# With `Coverage`
# 1. Extract `min_time_per_unit` (if distribution, select from it)
# 2. Calculate base_search_time (different methods for transect and radial) -> `base_search_time`
# 3. Allocate surveyors to survey units based on chosen assignment method
#     - TODO: implement optimized methods
# 4. Merge data from `Team` to `Coverage`
# 5. Extract surveyor speed penalty values (if distribution, select from it) -> `speed_penalty_obs`
#
# Find `Feature`s from `Assemblage` that intersect `Coverage` (via spatial join)
# - Record which survey unit it intersects (or NaN)
# - If intersects, set proximity to 1.0, else set proximity to 0.0 -> `proximity_obs`
#
# Extract surveyor skill values (if distribution, select from it) -> `skill_obs`
#
# `discovery_prob = obs_rate * vis_obs * proximity_obs * skill_obs`

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Inspect the results

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.raw.head()

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.raw.shape

# + {"slideshow": {"slide_type": "slide"}}
transect_survey.discovery.iloc[7:15]
# -

transect_survey.discovery[transect_survey.discovery["discovery_prob"].notna()].groupby(["run"]).count()

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.discovery.shape

# + {"slideshow": {"slide_type": "slide"}}
transect_survey.discovery.describe()

# + {"slideshow": {"slide_type": "slide"}}
transect_survey.discovery_plot()
# -

import pandas as pd
import altair as alt
alt.data_transformers.enable('json')

tmp = pd.DataFrame(transect_survey.discovery.drop(columns=['shape']))

run0 = tmp[tmp["discovery_prob"].notna() & (tmp["run"]==0)]
run1 = tmp[tmp["discovery_prob"].notna() & (tmp["run"]==1)]
run2 = tmp[tmp["discovery_prob"].notna() & (tmp["run"]==2)]

run0.head()

run1.head()


class Surveyor(Base):
    __tablename__ = "surveyors"

    name = Column("name", String(50), primary_key=True, sqlite_on_conflict_unique="IGNORE")
    team_name = Column("team_name", String(50), ForeignKey("teams.name"))
    surveyor_type = Column("surveyor_type", String(50))
    skill = Column("skill", PickleType)
    speed_penalty = Column("speed_penalty", PickleType)

    # relationships
    team = relationship("Team")




tmp_grp = tmp.groupby("feature_name").agg({"discovery_prob":"mean"})
tmp_grp = tmp_grp.dropna().reset_index()
tmp_grp

alt.Chart(tmp_grp.head(15)).mark_bar().encode(
    y = alt.Y("feature_name:N", title="artifact"),
    x = alt.X("discovery_prob:Q", title="mean discovery probability")
)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Run the radial survey!!!

# + {"slideshow": {"slide_type": "fragment"}}
radial_survey.run(n_runs=1)

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Inspect the results

# + {"slideshow": {"slide_type": "fragment"}}
radial_survey.discovery.head()

# + {"slideshow": {"slide_type": "fragment"}}
radial_survey.discovery.shape

# + {"slideshow": {"slide_type": "slide"}}
radial_survey.discovery.describe()

# + {"slideshow": {"slide_type": "slide"}}
radial_survey.discovery_plot()

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Set a discovery probability threshold and count the number of artifacts

# + {"slideshow": {"slide_type": "fragment"}}
tdf = transect_survey.discovery
tdf.loc[tdf["discovery_prob"]>0.5, :].shape[0]

# + {"slideshow": {"slide_type": "fragment"}}
rdf = radial_survey.discovery
rdf.loc[rdf["discovery_prob"]>0.5, :].shape[0]

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Compare area covered

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.coverage.df.area.sum(), radial_survey.coverage.df.area.sum()

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Examine survey time
# (converted to person-hours)

# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.total_time / 3600, radial_survey.total_time / 3600

# + {"slideshow": {"slide_type": "slide"}}
transect_survey.time_surveyunit.head(10)
# -

import altair as alt

alt.Chart(transect_survey.time_surveyunit).mark_bar().encode(
    x = alt.X("sum(total_time_per_surveyunit):Q", title="Total time (seconds)"),
    y = alt.Y("surveyor_name:N", title="Surveyor")
)





# + {"slideshow": {"slide_type": "fragment"}}
transect_survey.time_surveyor

# + {"slideshow": {"slide_type": "slide"}}
radial_survey.time_surveyunit.head()

# + {"slideshow": {"slide_type": "fragment"}}
radial_survey.time_surveyor

# + {"slideshow": {"slide_type": "slide"}, "cell_type": "markdown"}
# ## Performance

# + {"slideshow": {"slide_type": "fragment"}}
# %%timeit
for i in range(100):
    transect_survey.run()

# + {"slideshow": {"slide_type": "fragment"}}
import datetime
print(str(datetime.datetime.now()))

for i in range(1000):
    transect_survey.run()
    
print(str(datetime.datetime.now()))
