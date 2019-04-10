
import prospect


def test_returns_Survey(a_survey):
    assert isinstance(a_survey, prospect.Survey)


def test_has_name_attribute(a_survey):
    assert hasattr(a_survey, 'name')
