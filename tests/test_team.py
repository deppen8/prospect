import prospect


def test_returns_Team(a_team):
    assert isinstance(a_team, prospect.Team)


def test_has_desired_attributes(a_team):
    for a in ["name", "surveyor_list", "assignment", "df"]:
        assert hasattr(a_team, a)
