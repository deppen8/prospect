import pytest
import surveysim
from pathlib import Path


# `Area` FIXTURES FOR USE IN OTHER MODULES


LEIAP_AREA_PATHS = ['leiap_field1.shp', 'leiap_field2.shp', 'leiap_field3.shp', 'leiap_field4.shp',
                    'leiap_field5.shp', 'leiap_field6.shp', 'leiap_field7.shp', 'leiap_field8.shp']


@pytest.fixture(params=LEIAP_AREA_PATHS, ids=LEIAP_AREA_PATHS, scope='session')
def an_area_shapefile_path(request):
    return Path(f'test_datasets/shapefiles/areas/{request.param}')


@pytest.fixture(params=LEIAP_AREA_PATHS, ids=LEIAP_AREA_PATHS, scope='session')
def an_area_from_shapefile(request):
    area = surveysim.Area.from_shapefile(name='test_area_from_shapefile', path=Path(
        f'test_datasets/shapefiles/areas/{request.param}'))
    return area


# `Layer` FIXTURES FOR USE IN OTHER MODULES


LEIAP_LAYER_PATHS = [
    'leiap_field1_points.shp',
    'leiap_field2_points.shp',
    'leiap_field3_points.shp',
    'leiap_field4_points.shp',
    'leiap_field5_polygons.shp',
    'leiap_field6_polygons_overlap_edges.shp',
    'leiap_field7_points.shp',
    'leiap_field8_polygon_single.shp'
]

area_layer_tuples = list(zip(LEIAP_AREA_PATHS, LEIAP_LAYER_PATHS))


@pytest.fixture(params=LEIAP_LAYER_PATHS, ids=LEIAP_LAYER_PATHS, scope='session')
def a_layer_shapefile_path(request):
    return Path(f'test_datasets/shapefiles/layers/{request.param}')


@pytest.fixture(params=area_layer_tuples, ids=area_layer_tuples, scope='session')
def a_layer_from_shapefile(request):
    area = surveysim.Area.from_shapefile(name='test_area4layer', path=Path(
        f'test_datasets/shapefiles/areas/{request.param[0]}'))
    layer = surveysim.Layer.from_shapefile(path=Path(
        f'test_datasets/shapefiles/layers/{request.param[1]}'), area=area, name='test_layer', feature_type=None)
    return layer


@pytest.fixture(params=[area_layer_tuples], scope='session')
def a_layer_list(request):
    layer_list = []
    for a, l in request.param:
        area = surveysim.Area.from_shapefile(name='test_area4layer', path=Path(
            f'test_datasets/shapefiles/areas/{a}'))
        layer = surveysim.Layer.from_shapefile(path=Path(
            f'test_datasets/shapefiles/layers/{l}'), area=area, name='test_layer', feature_type=None)
        layer_list.append(layer)
    return layer_list


# `Assemblage` FIXTURES FOR USE IN OTHER MODULES


@pytest.fixture(scope='session')
def an_assemblage(a_layer_list):
    return surveysim.Assemblage(name='test_assemblage', layers=a_layer_list)