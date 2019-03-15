
import surveysim

from shapely.geometry import Polygon
from scipy.stats._distn_infrastructure import rv_frozen
from geopandas import GeoDataFrame


def test_returns_Area(an_area):
    assert isinstance(an_area, surveysim.Area)


def test_has_name_attribute(an_area):
    assert hasattr(an_area, 'name')


def test_name_attribute_str(an_area):
    assert isinstance(an_area.name, str)


def test_has_survey_name_attribute(an_area):
    assert hasattr(an_area, 'survey_name')


def test_survey_name_attribute_str(an_area):
    assert isinstance(an_area.survey_name, str)


def test_has_shape_attribute(an_area):
    assert hasattr(an_area, 'shape')


def test_shape_attribute_Polygon(an_area):
    assert isinstance(an_area.shape, Polygon)


def test_has_vis_attribute(an_area):
    assert hasattr(an_area, 'vis')


def test_vis_attribute_float_rv_frozen(an_area):
    assert isinstance(an_area.vis, (float, rv_frozen))


def test_has_df_attribute(an_area):
    assert hasattr(an_area, 'df')


def test_df_attribute_gdf(an_area):
    assert isinstance(an_area.df, GeoDataFrame)
