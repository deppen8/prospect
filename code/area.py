"""
Description of file
"""


class Area(object):

    polygon = None

    def __init__(self):
        pass

    def make_rectangle(self, bounds=(0, 0, 1, 1)):
        from shapely.geometry import box
        import geopandas as gpd
        area = box(bounds[0], bounds[1], bounds[2], bounds[3])
        gds = gpd.GeoSeries(area)

        self.polygon = gds
