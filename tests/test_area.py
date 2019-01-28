from surveysim import Area
from geopandas import GeoDataFrame
from shapely.geometry import Polygon


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
    area = Area.from_shapely_polygon(name='test_name', polygon=a_shapely_polygon)
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


# class TestArea(object):

#     def setup_method(self):
#         self.default = Area()

#     def test_default_construction(self):
#         assert self.default == Area(name='area', shape=None, vis=1.0)

#     def test_default_is_gdf(self):
#         assert isinstance(self.default.df, GeoDataFrame)

#     def test_default_area_measures(self):
#         assert self.default.df.bounds.minx[0] == 0
#         assert self.default.df.bounds.miny[0] == 0
#         assert self.default.df.bounds.maxx[0] == 1
#         assert self.default.df.bounds.maxy[0] == 1
#         assert self.default.df.area[0] == 1

#     def test_default_columns_exist(self):
#         for col in ['area_name', 'visibility', 'geometry']:
#             assert col in self.default.df.columns
