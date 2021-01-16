import pytest
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


def test_df_column_names(an_area):
    assert an_area.df.columns.to_list() == ["name", "shape", "vis"]


def test_from_shapefile_returns_Area(an_area_shapefile_path):
    area = prospect.Area.from_shapefile(
        name="test_area_from_shapefile", path=an_area_shapefile_path
    )

    assert isinstance(area, prospect.Area)


def test_from_shapefile_has_desired_attributes(an_area_from_shapefile):
    for a in ["name", "shape", "vis", "df"]:
        assert hasattr(an_area_from_shapefile, a)


def test_from_shapefile_name_attribute_str(an_area_from_shapefile):
    assert isinstance(an_area_from_shapefile.name, str)


def test_from_shapefile_shape_attribute_Polygon(an_area_from_shapefile):
    assert isinstance(an_area_from_shapefile.shape, Polygon)


def test_from_shapefile_vis_attribute_float_rv_frozen(an_area_from_shapefile):
    assert isinstance(an_area_from_shapefile.vis, (float, rv_frozen))


def test_from_shapefile_df_attribute_gdf(an_area_from_shapefile):
    assert isinstance(an_area_from_shapefile.df, GeoDataFrame)


def test_from_shapefile_df_column_names(an_area_from_shapefile):
    assert an_area_from_shapefile.df.columns.to_list() == ["name", "shape", "vis"]


VALUE_ORIGIN_PARAMS = [(100, (0.0, 0.0)), (0, (0.0, 0.0)), (100, (-10.0, -10.0))]


@pytest.mark.parametrize("value,origin", VALUE_ORIGIN_PARAMS)
def test_from_area_value_returns_Area(value, origin):
    area = prospect.Area.from_area_value(
        name="test_area_from_area_value", value=value, origin=origin
    )

    assert isinstance(area, prospect.Area)


def test_from_area_value_has_desired_attributes(an_area_from_area_value):
    for a in ["name", "shape", "vis", "df"]:
        assert hasattr(an_area_from_area_value, a)


def test_from_area_value_name_attribute_str(an_area_from_area_value):
    assert isinstance(an_area_from_area_value.name, str)


def test_from_area_value_shape_attribute_Polygon(an_area_from_area_value):
    assert isinstance(an_area_from_area_value.shape, Polygon)


def test_from_area_value_vis_attribute_float_rv_frozen(an_area_from_area_value):
    assert isinstance(an_area_from_area_value.vis, (float, rv_frozen))


def test_from_area_value_df_attribute_gdf(an_area_from_area_value):
    assert isinstance(an_area_from_area_value.df, GeoDataFrame)


def test_from_area_value_df_column_names(an_area_from_area_value):
    assert an_area_from_area_value.df.columns.to_list() == ["name", "shape", "vis"]


def test_from_area_value_returns_correct_area_value():
    area = prospect.Area.from_area_value(name="test_area_from_area_value", value=100)
    assert area.df.area[0] == 100
