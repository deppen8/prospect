
import prospect


def test_returns_SurveyUnit(a_surveyunit):
    assert isinstance(a_surveyunit, prospect.SurveyUnit)


def test_has_desired_attributes(a_surveyunit):
    for a in ['name', 'coverage_name', 'shape', 'surveyunit_type', 'surveyunit_area', 'length', 'radius', 'min_time_per_unit']:
        assert hasattr(a_surveyunit, a)
