
import surveysim


def test_returns_Survey(a_survey):
    assert isinstance(a_survey, surveysim.Survey)


def test_has_name_attribute(a_survey):
    assert hasattr(a_survey, 'name')
