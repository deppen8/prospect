import prospect


def test_returns_Layer(a_layer):
    assert isinstance(a_layer, prospect.Layer)


def test_has_desired_attributes(a_layer):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer, a)
