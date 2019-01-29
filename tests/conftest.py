import pytest
import surveysim
from pathlib import Path


# `Area` FIXTURES FOR USE IN OTHER MODULES

leiap_area_paths = ['leiap_field1.shp', 'leiap_field2.shp', 'leiap_field3.shp', 'leiap_field4.shp',
                    'leiap_field5.shp', 'leiap_field6.shp', 'leiap_field7.shp', 'leiap_field8.shp']


@pytest.fixture(params=leiap_area_paths, ids=leiap_area_paths, scope='session')
def an_area_shapefile_path(request):
    return Path(f'test_datasets/shapefiles/areas/{request.param}')


# FIXTURES FOR `Layer`


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
    default_Area = surveysim.Area.from_area_value(
        name='test_area4layer', value=1.0)
    layer = surveysim.Layer.from_shapefile(path=Path(
        f'test_datasets/shapefiles/layers/{request.param}'), area=default_Area, name='test_layer', feature_type=None)
    return layer
