
import surveysim


def test_returns_Surveyor(a_surveyor):
    assert isinstance(a_surveyor, surveysim.Surveyor)


def test_has_desired_attributes(a_surveyor):
    for a in ['name', 'team_name', 'surveyor_type', 'skill', 'speed_penalty']:
        assert hasattr(a_surveyor, a)
