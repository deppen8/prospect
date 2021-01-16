# Coverage

The `Coverage` represents the areas searched by the `Team` in a survey. Any `Feature` objects located within the `Coverage` *might* be discovered and collected; any `Feature` objects located outside the `Coverage` will definitely *not* be discovered and collected (at least in the current configuration of `prospect`). Like the `Assemblage`, the `Coverage` requires an `Area` object be passed as a parameter of the creation methods.

The shape and location of these areas are governed by the survey strategy adopted in the simulation. For example, the chosen spacing between transects (and the choice of transects themselves) can be represented in the `Coverage` building block.

## Creating a `Coverage`

A single `Coverage` is created from a list of `SurveyUnit` objects. These `SurveyUnit` objects can be created manually, but because these units are typically regularly-shaped, regularly-spaced, and sharing the same `min_time_per_unit` parameter, there are a some convenience methods provided to create them in bulk and add them to the `Coverage`.

### From a list of `SurveyUnit` objects

First, however, let us create some small square `SurveyUnit` objects manually and use them to create a `Coverage`.

from shapely.geometry import Point
import prospect

radius = 10
circ1 = Point(10, 10).buffer(radius)  # create circle
su1 = prospect.SurveyUnit(
        name="surveyunit1",
        coverage_name="demo_coverage",
        shape=circ1,
        surveyunit_type="radial",
        length=None,
        radius=radius,
        min_time_per_unit=prospect.utils.truncnorm(mean=20, sd=8, lower=0, upper=100),
)

circ2 = Point(50, 50).buffer(radius)  # create circle
su2 = prospect.SurveyUnit(
        name="surveyunit2",
        coverage_name="demo_coverage",
        shape=circ2,
        surveyunit_type="radial",
        length=None,
        radius=radius,
        min_time_per_unit=prospect.utils.truncnorm(mean=20, sd=8, lower=0, upper=100),
)

circ3 = Point(90, 90).buffer(radius)  # create circle
su3 = prospect.SurveyUnit(
        name="surveyunit3",
        coverage_name="demo_coverage",
        shape=circ3,
        surveyunit_type="radial",
        length=None,
        radius=radius,
        min_time_per_unit=prospect.utils.truncnorm(mean=20, sd=8, lower=0, upper=100),
)

type(circ1)

type(su1)

demo_area = prospect.Area.from_area_value(
    name='demo_area', 
    value=10000
)

coverage_from_list = prospect.Coverage(name="demo_coverage", area=demo_area, surveyunit_list=[su1, su2, su3], orientation=None, spacing=None)

type(coverage_from_list)

coverage_from_list.__dict__

coverage_from_list.df

type(coverage_from_list.df)

coverage_from_list.df.plot(ax=demo_area.df.plot(), color="orange");

### From a shapefile

The `from_shapefile()` method is useful for reading in existing surveys as `Coverage` objects. These could be the locations of survey units from a completed field survey or maybe survey units that are not shaped according to one of the built-in methods (transects and radial units).

area_from_shp = prospect.Area.from_shapefile(
    name="area_shp", 
    path="./data/demo_area.shp"
)

coverage_from_shp = prospect.Coverage.from_shapefile(
    "./data/demo_coverage.shp",
    name="demo_coverage_from_shp",
    area=area_from_shp,
    surveyunit_type="polygon",
    spacing=None,
    orient_axis=None,
    min_time_per_unit=20
)

coverage_from_shp.df

coverage_from_shp.df.plot(ax=area_from_shp.df.plot(), color="orange");

### From a `GeoDataFrame`

The `from_GeoDataFrame()` method is intended to be used much like the `from_shapefile()` method: when you have the spatial properties of the survey units already defined (in this case in a `GeoDataFrame`), even if they are irregular, you can quickly create a `Coverage` object from them.

A `GeoDataFrame` can also be useful when your spatial data is stored in some format other than a shapefile. You can use any package (e.g., `shapely`) to read from the native format to something useable by `geopandas` (e.g., WKT format). `geopandas` can then read this to a `GeoDataFrame` for use in `prospect`.

For the sake of example, let's load the shapefile we used above, convert it to well-known text (WKT) format, then load into a `GeoDataFrame`.

import fiona
from shapely.geometry import shape, Polygon

polys = fiona.open("./data/demo_coverage.shp")
collection_of_polys = [shape(item['geometry']) for item in polys]
units = [Polygon(poly.exterior.coords).wkt for poly in collection_of_polys]

Let's look at an example of the units.

units[0]

type(units[0])

Next, we can put this string representation in a `pandas` `DataFrame`.

import pandas as pd

wkt_df = pd.DataFrame(
    {
        "names": ["unit1", "unit2", "unit3", "unit4"],
        "coordinates":units
    }
)

wkt_df

Confirm that the entries in the new column `"coordinates"` are strings.

type(wkt_df['coordinates'][0])

from shapely import wkt
import geopandas as gpd
wkt_df["geo_coordinates"] = wkt_df["coordinates"].apply(wkt.loads)
wkt_geodf = gpd.GeoDataFrame(wkt_df, geometry="geo_coordinates")

wkt_geodf

`"coordinates"` and `"geo_coordinates"` look similar, but the latter now contains `shapely` `Polygon` objects instead of strings and the whole thing is a `GeoDataFrame` suitable for `prospect`.

type(wkt_geodf['geo_coordinates'][0])

type(wkt_geodf)

Let's complete the cycle by turning this into a `prospect` `Coverage` object.

area_from_shp = prospect.Area.from_shapefile(
    name="area_shp", 
    path="./data/demo_area.shp"
)

coverage_from_gdf = prospect.Coverage.from_GeoDataFrame(
    gdf=wkt_geodf,
    name="demo_coverage_from_gdf",
    area=area_from_shp,
    surveyunit_type="polygon",
    min_time_per_unit=20
)

coverage_from_gdf.df.plot(ax=area_from_shp.df.plot(), color="orange");

### Bulk-create transects

Transects are probably the most common type of survey strategy in use in the field. As such, `prospect` includes a `from_transects()` method to easily create a transect-based survey approach.

This method for constructing `Coverage` objects comes with a few special parameters that help `prospect` create the appropriate transects for the given `Area`.

- `spacing`: Distance between transects (the default is 10.0)
- `sweep_width`: Buffer distance around transects (the default is 2.0)
- `orientation`: Angle of the predominant axis of the transects (the default is 0.0)
- `optimize_orient_by` (`'area_coverage'` or `'area_orient'`): Metric to optimize in determining the orientation of transects. `'area_coverage'` chooses the orientation that maximizes the area covered by the transects. `'area_orient'` chooses the orientation that best parallels the `orient_axis` of the area. The default is `None`, in which case the `orientation` parameter is used directly.
- `orient_increment`: Step size (in degrees) to use when testing different orientations. (the default is 5.0)
- `orient_axis` (`'long'` or `'short'`): Axis of the area along which to orient the survey units (the default is `'long'`, which creates rows parallel to the longest axis of the area's minimum rotated rectangle)
- `min_time_per_unit`: Minimum amount of time required to complete one "unit" of survey, given no surveyor speed penalty and no time penalty for recording features. The default is 0.0. *Because transects can differ in length, transect coverages should specify this term as time per one unit of distance (e.g., seconds per meter).*

The `from_transects()` method has a series of possible customizations. We will explore them one-by-one using the same `Area` object we have been using.

area_from_shp = prospect.Area.from_shapefile(
    name="area_shp", 
    path="./data/demo_area.shp"
)

Let's start, however, with a simple version of a transect `Coverage`.

simple_transects = prospect.Coverage.from_transects(
    name="demo_simple_transects", 
    area=area_from_shp, 
    spacing=10, 
    sweep_width=2, 
    min_time_per_unit=20
)

simple_transects.df.plot(ax=area_from_shp.df.plot(), color="orange");

We can vary the spacing and the width of the transects.

simple_transects_spacing = prospect.Coverage.from_transects(
    name="demo_simple_transects_spacing", 
    area=area_from_shp, 
    spacing=20, 
    sweep_width=1, 
    min_time_per_unit=20
)

simple_transects_spacing.df.plot(ax=area_from_shp.df.plot(), color="orange");

Notice that by default, the transects are oriented directly north-south. If you know what orientation you would like to use, you can specify that directly with the `orientation` parameter. Here we rotate them 90 degrees to an east-west orientation.

transects_orientation = prospect.Coverage.from_transects(
    name="demo_transects_orientation", 
    area=area_from_shp,
    spacing=20, 
    sweep_width=1, 
    orientation=90,
    min_time_per_unit=20
)

transects_orientation.df.plot(ax=area_from_shp.df.plot(), color="orange");

There are also ways to optimize the orientation of the transects. First, you can choose to find the orientation that maximizes the areal extent of the survey units (`'area_coverage'`).

The `orient_increment` parameter determines the orientations that `prospect` will iterate through. This is useful to specify if you are planning to put a team in the field. It may be impractical to orient a team to fractions of a degree or even a single degree. You might prefer to stick to increments of 5 or 10 degrees. Below, we check every 5 degrees, which is the default.

transects_orientation_areal_cov = prospect.Coverage.from_transects(
    name="demo_transects_orientation_areal_cov", 
    area=area_from_shp,
    spacing=20, 
    sweep_width=1, 
    optimize_orient_by="area_coverage",
    orient_increment=5,
    min_time_per_unit=20
)

transects_orientation_areal_cov.df.plot(ax=area_from_shp.df.plot(), color="orange");

You can then examine the orientation that was chosen via the `orientation` attribute

transects_orientation_areal_cov.orientation

The other optimization option is `'area_orient'`, which chooses the orientation that best parallels the `orient_axis` of the area. You can choose to follow the `'long'` or `'short'` axis.

transects_orientation_areal_orient = prospect.Coverage.from_transects(
    name="demo_transects_orientation_areal_orient", 
    area=area_from_shp,
    spacing=20, 
    sweep_width=1, 
    optimize_orient_by="area_orient",
    orient_axis="long",
    min_time_per_unit=20
)

transects_orientation_areal_orient.df.plot(ax=area_from_shp.df.plot(), color="orange");

transects_orientation_areal_orient.orientation

In this example, optimizing by the long axis yields an orientation of -42 degrees (e.g., 318 degrees).

transects_orientation_areal_orient_short = prospect.Coverage.from_transects(
    name="demo_transects_orientation_areal_orient_short", 
    area=area_from_shp,
    spacing=20, 
    sweep_width=1, 
    optimize_orient_by="area_orient",
    orient_axis="short",
    min_time_per_unit=20
)

transects_orientation_areal_orient_short.df.plot(ax=area_from_shp.df.plot(), color="orange");

transects_orientation_areal_orient_short.orientation

### Bulk-create radial units

The `from_radials()` method creates a regularly-spaced grid of circular survey plots. It has all of the same special parameters as the `from_transects()` method with the exception of the following:

- Instead of `sweep_width`, radials have a `radius` (naturally) that controls how large the survey plots will be.
- The `min_time_per_unit` can be specified as the minimum time it takes to survey one circular plot.

Let's start, however, with a simple version of a radials `Coverage`. The default radius is 1.78, which gives you radials with roughly 10 square units of area.

simple_radials = prospect.Coverage.from_radials(
    name="demo_simple_radials", 
    area=area_from_shp, 
    spacing=10,
    radius=1.78,
    min_time_per_unit=20
)

simple_radials.df.plot(ax=area_from_shp.df.plot(), color="orange");

Notice that, like the transects, by default, the transects are oriented directly north-south. If we were to rotate them 90 degrees as we did for the transects, we would get much the same result.

radials_orientation = prospect.Coverage.from_radials(
    name="demo_radials_orientation", 
    area=area_from_shp,
    spacing=10, 
    radius=1.78, 
    orientation=90,
    min_time_per_unit=20
)

radials_orientation.df.plot(ax=area_from_shp.df.plot(), color="orange");

radials_orientation.orientation

The same orientation optimization parameters are available for radial survey units as were available for transects.

First, `area_coverage`:

radials_orientation_areal_cov = prospect.Coverage.from_radials(
    name="demo_radials_orientation_areal_cov", 
    area=area_from_shp,
    spacing=10, 
    radius=1.78, 
    optimize_orient_by="area_coverage",
    orient_increment=5,
    min_time_per_unit=20
)

radials_orientation_areal_cov.df.plot(ax=area_from_shp.df.plot(), color="orange");

You can then examine the orientation that was chosen via the `orientation` attribute

radials_orientation_areal_cov.orientation

Likewise, `area_orient`:

radials_orientation_areal_orient = prospect.Coverage.from_radials(
    name="demo_radials_orientation_areal_orient", 
    area=area_from_shp,
    spacing=10, 
    radius=1.78, 
    optimize_orient_by="area_orient",
    orient_axis="long",
    min_time_per_unit=20
)

radials_orientation_areal_orient.df.plot(ax=area_from_shp.df.plot(), color="orange");

radials_orientation_areal_orient.orientation

```{admonition} Look!
:class: hint
This is the exact same value as we calculated for the transects!
```

Now for the short axis:

radials_orientation_areal_orient_short = prospect.Coverage.from_radials(
    name="demo_radials_orientation_areal_orient_short", 
    area=area_from_shp,
    spacing=10, 
    radius=1.78, 
    optimize_orient_by="area_orient",
    orient_axis="short",
    min_time_per_unit=20
)

radials_orientation_areal_orient_short.df.plot(ax=area_from_shp.df.plot(), color="orange");

radials_orientation_areal_orient_short.orientation

Again, this value matches the one for the transects.

## `min_time_per_unit` parameter

This parameter is used to model the base level of time it takes to survey one unit. For variable-length units like transects, this parameter needs to be an amount of time per unit of distance (e.g., 5 seconds per meter). For fixed-size units like radial units or square units, this can be a single base time.

This parameter should be specified under the following assumptions:
- no surveyor speed penalty (from the Surveyor)
- no time penalty for recording (from the Assemblage)

In other words, it represents only the search time for an expert surveyor who doesn't stop to record any artifacts or features.

With enough prior experience, `min_time_per_unit` can be modeled as a single value constant. If `min_time_per_unit` is being modeled as a distribution, it makes most sense to have it bounded at zero.

```{tip}
The truncated normal distribution is a good choice for this.
```

import seaborn as sns
dist_trunc = prospect.utils.truncnorm(mean=30, sd=30, lower=0, upper=200)

hist_trunc = sns.distplot(dist_trunc.rvs(100000), kde=False)  # draw 100k random values and plot
hist_trunc.set_xlim(-100,150);

```{note}
While the truncated normal distribution is a good choice generally, `prospect` allows you to use whatever `scipy` distribution you think fits your case best.
```

