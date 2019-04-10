import prospect
from geopandas import GeoDataFrame


def test_assemblage_returns(an_assemblage):
    assert isinstance(an_assemblage, prospect.Assemblage)
    assert isinstance(an_assemblage.layer_dict, dict)
    assert isinstance(an_assemblage.df, GeoDataFrame)
