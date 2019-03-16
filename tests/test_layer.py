
import surveysim


def test_returns_Layer(a_layer):
    assert isinstance(a_layer, surveysim.Layer)


def test_has_desired_attributes(a_layer):
    for a in ['name', 'area_name', 'assemblage_name', 'feature_list', 'df']:
        assert hasattr(a_layer, a)
