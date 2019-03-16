
import surveysim


def test_returns_Coverage(a_coverage):
    assert isinstance(a_coverage, surveysim.Coverage)


def test_has_desired_attributes(a_coverage):
    for a in ['name', 'survey_name', 'area_name', 'surveyunit_list', 'orientation', 'spacing', 'sweep_width', 'radius', 'df']:
        assert hasattr(a_coverage, a)
