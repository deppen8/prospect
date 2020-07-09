# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np

import prospect

np.random.seed(5)


# %%
# A simple square area of 100k square units
area = prospect.Area.from_area_value(name="area", value=100000, origin=(0, 0), vis=1.0)
area.df.plot()


# %%
# Create one perfect surveyor and assign them to a team
surveyor = prospect.Surveyor(
    name="surveyor",
    team_name="team",
    surveyor_type="perfect",
    skill=1.0,
    speed_penalty=0.0,
)
team = prospect.Team(name="team", surveyor_list=[surveyor], assignment="naive")


# %%
# Create a bunch of transect Coverage configurations
pass


# %%
# Create a bunch of artifact Assemblage densities
pass


# %%
