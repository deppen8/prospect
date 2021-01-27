import prospect


def test_returns_Coverage(a_coverage):
    assert isinstance(a_coverage, prospect.Coverage)


def test_has_desired_attributes(a_coverage):
    for a in [
        "name",
        "surveyunit_list",
        "orientation",
        "spacing",
        "sweep_width",
        "radius",
        "df",
    ]:
        assert hasattr(a_coverage, a)


def test_from_transects_simple_returns_Coverage(an_area_from_shapefile):
    coverage = prospect.Coverage.from_transects(
        name="test_Coverage_from_transects",
        area=an_area_from_shapefile,
        spacing=10,
        sweep_width=2,
    )
    assert isinstance(coverage, prospect.Coverage)


def test_from_transects_simple_has_desired_attributes(an_area_from_shapefile):
    coverage = prospect.Coverage.from_transects(
        name="test_Coverage_from_transects",
        area=an_area_from_shapefile,
        spacing=10,
        sweep_width=2,
    )

    for a in [
        "name",
        "surveyunit_list",
        "orientation",
        "spacing",
        "sweep_width",
        "radius",
        "df",
    ]:
        assert hasattr(coverage, a)


def test_from_transects_defaults_creates_expected(a_rectangular_area):
    coverage = prospect.Coverage.from_transects(
        name="test_Coverage_from_transects",
        area=a_rectangular_area,
    )

    assert coverage.orientation == 0.0
    assert coverage.spacing == 10
    assert coverage.sweep_width == 2
    assert coverage.radius is None
    assert coverage.df.shape == (201, 8)


def test_from_transects_optimize_area_coverage_short_creates_expected(
    a_rectangular_area,
):
    coverage = prospect.Coverage.from_transects(
        name="test_Coverage_from_transects",
        area=a_rectangular_area,
        optimize_orient_by="area_coverage",
        orient_axis="short",
    )

    assert coverage.orientation == 90.0
    assert coverage.spacing == 10
    assert coverage.sweep_width == 2
    assert coverage.radius is None
    assert coverage.df.shape == (101, 8)
