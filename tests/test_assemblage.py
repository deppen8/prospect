
import prospect


def test_returns_Assemblage(an_assemblage):
    assert isinstance(an_assemblage, prospect.Assemblage)


def test_has_desired_attributes(an_assemblage):
    for a in ['name', 'survey_name', 'area_name', 'df']:
        assert hasattr(an_assemblage, a)
