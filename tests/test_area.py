from surveysim import Area
from geopandas import GeoDataFrame
from shapely.geometry import Polygon
from scipy.stats._distn_infrastructure import rv_frozen


# TEST FOR DEFAULT CONSTRUCTION


def test_default_params_returns_Area(a_default_Area):
    assert isinstance(a_default_Area, Area)


def test_default_df_is_GeoDataFrame(a_default_Area):
    assert isinstance(a_default_Area.df, GeoDataFrame)


def test_default_df_is_length_1(a_default_Area):
    assert a_default_Area.df.shape[0] == 1


def test_default_shape_is_None(a_default_Area):
    assert a_default_Area.shape is None


def test_default_default_columns_exist(a_default_Area):
    for col in ['area_name', 'vis', 'geometry']:
        assert col in a_default_Area.df.columns


# TESTS FOR `from_shapefile()` METHOD


def test_from_shapefile_path_returns_Area(an_area_shapefile_path):
    '''Test that `from_shapefile()` factory function returns an `Area` object'''
    area = Area.from_shapefile(name='test_name', path=an_area_shapefile_path)
    assert isinstance(area, Area)


def test_from_shapefile_df_is_GeoDataFrame(an_area_from_shapefile):
    assert isinstance(an_area_from_shapefile.df, GeoDataFrame)


def test_from_shapefile_df_is_length_1(an_area_from_shapefile):
    assert an_area_from_shapefile.df.shape[0] == 1


def test_from_shapefile_shape_is_Polygon(an_area_from_shapefile):
    assert isinstance(an_area_from_shapefile.shape, Polygon)


def test_from_shapefile_default_columns_exist(an_area_from_shapefile):
    for col in ['area_name', 'vis', 'geometry']:
        assert col in an_area_from_shapefile.df.columns


# TESTS FOR `from_shapely_polygon()` METHOD


def test_from_shapely_polygon_returns_Area(a_shapely_polygon):
    '''Test that `from_shapely_polygon()` factory function returns an `Area` object'''
    area = Area.from_shapely_polygon(
        name='test_name', polygon=a_shapely_polygon)
    assert isinstance(area, Area)


def test_from_shapely_polygon_df_is_GeoDataFrame(an_area_from_shapely_polygon):
    assert isinstance(an_area_from_shapely_polygon.df, GeoDataFrame)


def test_from_shapely_polygon_df_is_length_1(an_area_from_shapely_polygon):
    assert an_area_from_shapely_polygon.df.shape[0] == 1


def test_from_shapely_polygon_shape_is_Polygon(an_area_from_shapely_polygon):
    assert isinstance(an_area_from_shapely_polygon.shape, Polygon)


def test_from_shapely_polygon_default_columns_exist(an_area_from_shapely_polygon):
    for col in ['area_name', 'vis', 'geometry']:
        assert col in an_area_from_shapely_polygon.df.columns


# TESTS FOR `from_area_value()` METHOD


def test_from_area_value_returns_Area(an_area_origin_pair):
    '''Test that `from_area_value()` factory function returns an `Area` object'''
    area = Area.from_area_value(
        name='test_name', value=an_area_origin_pair[0], origin=an_area_origin_pair[1])
    assert isinstance(area, Area)


def test_from_area_value_df_is_GeoDataFrame(an_area_from_area_origin_pair):
    assert isinstance(an_area_from_area_origin_pair.df, GeoDataFrame)


def test_from_area_value_df_is_length_1(an_area_from_area_origin_pair):
    assert an_area_from_area_origin_pair.df.shape[0] == 1


def test_from_area_value_shape_is_Polygon(an_area_from_area_origin_pair):
    assert isinstance(an_area_from_area_origin_pair.shape, Polygon)


def test_from_area_value_default_columns_exist(an_area_from_area_origin_pair):
    for col in ['area_name', 'vis', 'geometry']:
        assert col in an_area_from_area_origin_pair.df.columns


# TESTS FOR `set_vis_beta_dist()` METHOD


def test_set_vis_beta_dist_creates_rv_continuous(an_area_from_shapefile):
    area = an_area_from_shapefile
    area.set_vis_beta_dist(alpha=9, beta=1)
    assert isinstance(area.vis, rv_frozen)
