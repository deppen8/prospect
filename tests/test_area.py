from surveysim import Area
from geopandas import GeoDataFrame

class TestArea(object):

    def setup_method(self):
        self.default = Area()
    
    def test_default_is_gdf(self):
        assert isinstance(self.default.data, GeoDataFrame)

    def test_default_area_measures(self):
        assert self.default.data.bounds.minx[0] == 0
        assert self.default.data.bounds.miny[0] == 0
        assert self.default.data.bounds.maxx[0] == 1
        assert self.default.data.bounds.maxy[0] == 1
        assert self.default.data.area[0] == 1

    def test_default_columns_exist(self):
        for col in ['area_name', 'visibility', 'geometry']:
            assert col in self.default.data.columns
