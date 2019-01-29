import pytest
import surveysim


@pytest.fixture(scope='module')
def a_default_Layer():
    """Create `Layer` with defaults"""
    default_Area = surveysim.Area.from_area_value(
        name='test_area4layer', value=1.0)
    return surveysim.Layer(area=default_Area)


# TEST FOR DEFAULT CONSTRUCTION


def test_default_params_returns_Layer(a_default_Layer):
    assert isinstance(a_default_Layer, surveysim.Layer)


def test_from_shapefile_path_returns_Layer(a_layer_shapefile_path, an_area_shapefile_path):
    '''Test that `from_shapefile()` factory function returns a `Layer` object'''
    area = surveysim.Area.from_shapefile(name='test_name', path=an_area_shapefile_path)
    layer = surveysim.Layer.from_shapefile(path=a_layer_shapefile_path, area=area, name='test_layer', feature_type=None)
    assert isinstance(layer, surveysim.Layer)
