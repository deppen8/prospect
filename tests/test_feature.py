
import surveysim

from shapely.geometry import Point, LineString, Polygon
from scipy.stats._distn_infrastructure import rv_frozen


def test_returns_Feature(a_feature):
    assert isinstance(a_feature, surveysim.Feature)


def test_has_name_attribute(a_feature):
    assert hasattr(a_feature, 'name')


def test_name_attribute_str(a_feature):
    assert isinstance(a_feature.name, str)


def test_has_layer_name_attribute(a_feature):
    assert hasattr(a_feature, 'layer_name')


def test_layer_name_attribute_str(a_feature):
    assert isinstance(a_feature.layer_name, str)


def test_has_shape_attribute(a_feature):
    assert hasattr(a_feature, 'shape')


def test_shape_attribute_shapely_shape(a_feature):
    assert isinstance(a_feature.shape, (Point, LineString, Polygon))


def test_has_time_penalty_attribute(a_feature):
    assert hasattr(a_feature, 'time_penalty')


def test_time_penalty_attribute_float_rv_frozen(a_feature):
    assert isinstance(a_feature.time_penalty, (float, rv_frozen))


def test_has_ideal_obs_rate_attribute(a_feature):
    assert hasattr(a_feature, 'ideal_obs_rate')


def test_ideal_obs_rate_attribute_float_rv_frozen(a_feature):
    assert isinstance(a_feature.ideal_obs_rate, (float, rv_frozen))
