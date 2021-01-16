# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: 'Python 3.7.6 64-bit (''prospect'': conda)'
#     name: python37664bitprospectcondad74ec1694dc048969bdb9fe0d71480b0
# ---

# %%
import prospect

# %% [markdown]
# ## Sample universe
#
# Let's define a very simple generic sample universe.

# %%
sample_universe = prospect.Area.from_area_value("sample_universe", 10000, vis=1.0)

# %%
sample_universe.df.plot()

# %%
sample_population_lithics = prospect.Layer.from_poisson_points(rate=0.001, area=sample_universe, assemblage_name="sample_population", name="lithics")

# %%
sample_population_lithics.df.plot()

# %%
sample_population_ceramics = prospect.Layer.from_thomas_points(
    parent_rate=0.001,
    child_rate=5,
    gauss_var=5,
    name="ceramics",
    area=sample_universe,
    assemblage_name="sample_population"
)

# %%
sample_population_ceramics.df.plot()

# %%
sample_population = prospect.Assemblage(
    name="sample_population",
    area_name="sample_universe",
    layer_list=[sample_population_lithics, sample_population_ceramics]
)

# %%
sample_population.df.plot(column='layer_name', legend=True)

# %%
sample_units = prospect.Coverage.from_transects(name="transect_10m", area=sample_universe, orientation=90)

# %%
sample_units.df.plot()

# %%
