
import prospect

from shapely.geometry import Point, LineString, Polygon
from scipy.stats._distn_infrastructure import rv_frozen


def test_returns_Feature(a_feature):
    assert isinstance(a_feature, prospect.Feature)


def test_has_desired_attributes(a_feature):
    for a in ['name', 'layer_name', 'shape', 'time_penalty', 'ideal_obs_rate']:
        assert hasattr(a_feature, a)


def test_name_attribute_str(a_feature):
    assert isinstance(a_feature.name, str)


def test_layer_name_attribute_str(a_feature):
    assert isinstance(a_feature.layer_name, str)


def test_shape_attribute_shapely_shape(a_feature):
    assert isinstance(a_feature.shape, (Point, LineString, Polygon))


def test_time_penalty_attribute_float_rv_frozen(a_feature):
    assert isinstance(a_feature.time_penalty, (float, rv_frozen))


def test_ideal_obs_rate_attribute_float_rv_frozen(a_feature):
    assert isinstance(a_feature.ideal_obs_rate, (float, rv_frozen))
