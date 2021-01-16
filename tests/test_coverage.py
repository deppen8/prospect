import prospect


def test_returns_Coverage(a_coverage):
    assert isinstance(a_coverage, prospect.Coverage)


def test_has_desired_attributes(a_coverage):
    for a in [
        "name",
        "area_name",
        "surveyunit_list",
        "orientation",
        "spacing",
        "sweep_width",
        "radius",
        "df",
    ]:
        assert hasattr(a_coverage, a)
