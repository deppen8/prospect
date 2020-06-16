from geopandas import GeoDataFrame
from scipy.stats._distn_infrastructure import rv_frozen
from shapely.geometry import Polygon

import prospect


def test_returns_Area(an_area):
    assert isinstance(an_area, prospect.Area)


def test_has_desired_attributes(an_area):
    for a in ["name", "shape", "vis", "df"]:
        assert hasattr(an_area, a)


def test_name_attribute_str(an_area):
    assert isinstance(an_area.name, str)


def test_shape_attribute_Polygon(an_area):
    assert isinstance(an_area.shape, Polygon)


def test_vis_attribute_float_rv_frozen(an_area):
    assert isinstance(an_area.vis, (float, rv_frozen))


def test_df_attribute_gdf(an_area):
    assert isinstance(an_area.df, GeoDataFrame)
