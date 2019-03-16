
import surveysim

import pytest

from pathlib import Path
from shapely.geometry import Point, LineString, Polygon


@pytest.fixture(scope='module')
def tmp_db_path(tmp_path_factory):
    """Create a temporary path where the test db and other outputs can be stored.
    """

    return tmp_path_factory.mktemp('databases')


# `Simulation` FIXTURES


@pytest.fixture(scope='module')
def a_simulation(tmp_db_path):
    """Create SimSession session on the temporary path.
    """

    return surveysim.SimSession(engine_str=f'sqlite:///{tmp_db_path}/test_session.db')


# `Survey` FIXTURES


@pytest.fixture(scope='module')
def a_survey():
    return surveysim.Survey(name='test_survey')


# `Area` FIXTURES


POLYGONS = [
    Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)]),
    Polygon([(0, 0), (1, 1), (1, 0)]),
    Polygon([(0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0)]),
    Polygon([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, -1.0), (0.0, 0.0),
             (0.25, 0.25), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25), (0.25, 0.25)])
]


@pytest.fixture(params=POLYGONS, scope='module')
def an_area(request):
    return surveysim.Area(name=f'test_area', survey_name='test_survey',
                          shape=request.param, vis=1.0)


# `Feature` FIXTURES


FEATURE_SHAPES = [
    Point(1.0, 1.0),
    LineString([(2, 0), (2, 4), (3, 4)]),
    Polygon([(1, 1), (1, 3), (4, 3), (4, 1), (1, 1)])
]


@pytest.fixture(params=FEATURE_SHAPES, scope='module')
def a_feature(request):
    return surveysim.Feature(name='test_feature', layer_name='test_layer', shape=request.param, time_penalty=0.0, ideal_obs_rate=1.0)


# `Layer` FIXTURES


@pytest.fixture(scope='module')
def a_layer(an_area, a_feature):
    return surveysim.Layer(name='test_layer', area=an_area, assemblage_name='test_parent_assemblage', feature_list=[a_feature], time_penalty=0.0, ideal_obs_rate=0.0)


# `Assemblage` FIXTURES


@pytest.fixture(scope='module')
def an_assemblage(a_survey, an_area, a_layer):
    return surveysim.Assemblage(name='test_assemblage', survey_name=a_survey.name, area_name=an_area.name, layer_list=[a_layer])


# `SurveyUnit` FIXTURES


@pytest.fixture(params=POLYGONS, scope='module')
def a_surveyunit(request):
    return surveysim.SurveyUnit(name='test_surveyunit', coverage_name='test_coverage', shape=request.param, surveyunit_type='radial', length=None, radius=10.0, min_time_per_unit=0.0)


# `Coverage` FIXTURES


@pytest.fixture(scope='module')
def a_coverage(an_area, a_surveyunit):
    return surveysim.Coverage(name='test_coverage', area=an_area, survey_name='test_survey', surveyunit_list=[a_surveyunit], orientation=0.0, spacing=10.0, sweep_width=None, radius=None)


# `Surveyor` FIXTURES


@pytest.fixture(scope='module')
def a_surveyor():
    return surveysim.Surveyor(name='test_surveyor', team_name='test_team', surveyor_type='test_type', skill=1.0, speed_penalty=0.0)


# `Team` FIXTURES


@pytest.fixture(scope='module')
def a_team(a_surveyor):
    return surveysim.Team(name='test_team', survey_name='test_survey', surveyor_list=[a_surveyor])

    # LEIAP_AREA_PATHS = ['leiap_field1.shp', 'leiap_field2.shp', 'leiap_field3.shp', 'leiap_field4.shp',
    #                     'leiap_field5.shp', 'leiap_field6.shp', 'leiap_field7.shp', 'leiap_field8.shp']

    # @pytest.fixture(params=LEIAP_AREA_PATHS, ids=LEIAP_AREA_PATHS, scope='session')
    # def an_area_shapefile_path(request):
    #     return Path(f'tests/test_datasets/shapefiles/areas/{request.param}')

    # @pytest.fixture(params=LEIAP_AREA_PATHS, ids=LEIAP_AREA_PATHS, scope='session')
    # def an_area_from_shapefile(request):
    #     area = surveysim.Area.from_shapefile(name='test_area_from_shapefile', path=Path(
    #         f'tests/test_datasets/shapefiles/areas/{request.param}'))
    #     return area

    # # `Layer` FIXTURES FOR USE IN OTHER MODULES

    # LEIAP_LAYER_PATHS = [
    #     'leiap_field1_points.shp',
    #     'leiap_field2_points.shp',
    #     'leiap_field3_points.shp',
    #     'leiap_field4_points.shp',
    #     'leiap_field5_polygons.shp',
    #     'leiap_field6_polygons_overlap_edges.shp',
    #     'leiap_field7_points.shp',
    #     'leiap_field8_polygon_single.shp'

    # ]

    # area_layer_tuples = list(zip(LEIAP_AREA_PATHS, LEIAP_LAYER_PATHS))

    # @pytest.fixture(params=LEIAP_LAYER_PATHS, ids=LEIAP_LAYER_PATHS, scope='session')
    # def a_layer_shapefile_path(request):
    #     return Path(f'tests/test_datasets/shapefiles/layers/{request.param}')

    # @pytest.fixture(params=area_layer_tuples, scope='session')
    # def a_layer_from_shapefile(request):
    #     area = surveysim.Area.from_shapefile(name='test_area4layer', path=Path(
    #         f'tests/test_datasets/shapefiles/areas/{request.param[0]}'))
    #     layer = surveysim.Layer.from_shapefile(path=Path(
    #         f'tests/test_datasets/shapefiles/layers/{request.param[1]}'), area=area, name='test_layer', feature_type=None)
    #     return layer

    # @pytest.fixture(params=[area_layer_tuples], scope='session')
    # def a_layer_list(request):
    #     layer_list = []
    #     for a, l in request.param:
    #         area = surveysim.Area.from_shapefile(name='test_area4layer', path=Path(
    #             f'tests/test_datasets/shapefiles/areas/{a}'))
    #         layer = surveysim.Layer.from_shapefile(path=Path(
    #             f'tests/test_datasets/shapefiles/layers/{l}'), area=area, name='test_layer', feature_type=None)
    #         layer_list.append(layer)
    #     return layer_list

    # # `Assemblage` FIXTURES FOR USE IN OTHER MODULES

    # @pytest.fixture(scope='session')
    # def an_assemblage(a_layer_list):
    #     return surveysim.Assemblage(name='test_assemblage', layers=a_layer_list)
