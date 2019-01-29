import pytest
import surveysim
from pathlib import Path
from shapely.geometry import Polygon
import itertools

# define `Area` fixtures


@pytest.fixture(scope='session')
def a_default_Area():
    """Create `Area` with defaults"""
    return surveysim.Area()


# FIXTURES FOR THE `Area.from_shapefile()` METHOD


leiap_area_paths = ['leiap_field1.shp', 'leiap_field2.shp', 'leiap_field3.shp', 'leiap_field4.shp',
                    'leiap_field5.shp', 'leiap_field6.shp', 'leiap_field7.shp', 'leiap_field8.shp']


@pytest.fixture(params=leiap_area_paths, ids=leiap_area_paths, scope='session')
def an_area_shapefile_path(request):
    return Path(f'test_datasets/shapefiles/areas/{request.param}')


@pytest.fixture(params=leiap_area_paths, ids=leiap_area_paths, scope='session')
def an_area_from_shapefile(request):
    area = surveysim.Area.from_shapefile(name='test_area_from_shapefile', path=Path(
        f'test_datasets/shapefiles/areas/{request.param}'))
    return area


# FIXTURES FOR THE `Area.from_shapely_polygon()` METHOD


shapely_polys = [
    Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)]),
    Polygon([(0, 0), (1, 1), (1, 0)]),
    Polygon([(0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0)]),
    Polygon([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, -1.0), (0.0, 0.0),
             (0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25), (0.25, 0.25)])
]


@pytest.fixture(params=shapely_polys, scope='session')
def a_shapely_polygon(request):
    return request.param


@pytest.fixture(params=shapely_polys, scope='session')
def an_area_from_shapely_polygon(request):
    area = surveysim.Area.from_shapely_polygon(
        name='test_area_from_shapely', polygon=request.param)
    return area


# FIXTURES FOR THE `Area.from_area_value()` METHOD


area_values = [1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000]
origins = [
    (0.0, 0.0),
    (10.0, 0.0),
    (0.0, 10.0),
    (10.0, 10.0),
    (10, 10),
    (-10.0, 0.0),
    (0.0, -10.0),
    (-10.0, -10.0),
    (0.5, 0.5),
    (5, 5.0),
]

area_origin_pairs = list(itertools.product(area_values, origins))


@pytest.fixture(params=area_origin_pairs, scope='session')
def an_area_origin_pair(request):
    return request.param


@pytest.fixture(params=area_origin_pairs, scope='session')
def an_area_from_area_origin_pair(request):
    area = surveysim.Area.from_area_value(
        name='test_area_from_area_value', value=request.param[0], origin=request.param[1])
    return area


# FIXTURES FOR `Layer`


@pytest.fixture(scope='session')
def a_default_Layer():
    """Create `Layer` with defaults"""
    default_Area = surveysim.Area.from_area_value(name='test_area4layer', value=1.0)
    return surveysim.Layer(area=default_Area)


leiap_layer_paths = [
    'leiap_field1_points.shp',
    'leiap_field2_points.shp',
    'leiap_field3_points.shp',
    'leiap_field4_points.shp',
    'leiap_field5_polygons.shp',
    'leiap_field6_polygons_overlap_edges.shp',
    'leiap_field7_points.shp',
    'leiap_field8_polygon_single.shp'
]


@pytest.fixture(params=leiap_layer_paths, ids=leiap_layer_paths, scope='session')
def a_layer_shapefile_path(request):
    return Path(f'test_datasets/shapefiles/layers/{request.param}')


@pytest.fixture(params=leiap_layer_paths, ids=leiap_layer_paths, scope='session')
def a_layer_from_shapefile(request):
    default_Area = surveysim.Area.from_area_value(name='test_area4layer', value=1.0)
    layer = surveysim.Layer.from_shapefile(path=Path(
        f'test_datasets/shapefiles/layers/{request.param}'), area=default_Area, name='test_layer', feature_type=None)
    return layer
