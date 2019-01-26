from surveysim import Area
from geopandas import GeoDataFrame


class TestArea(object):

    def setup_method(self):
        self.default = Area()

    def test_default_is_gdf(self):
        assert isinstance(self.default.df, GeoDataFrame)

    def test_default_area_measures(self):
        assert self.default.df.bounds.minx[0] == 0
        assert self.default.df.bounds.miny[0] == 0
        assert self.default.df.bounds.maxx[0] == 1
        assert self.default.df.bounds.maxy[0] == 1
        assert self.default.df.area[0] == 1

    def test_default_columns_exist(self):
        for col in ['area_name', 'visibility', 'geometry']:
            assert col in self.default.df.columns
