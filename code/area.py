"""
Description of file
"""


class Area:
    def __init__(self):
        self.polygon = None
        self.bounds = None
        self.area = None
        self.total_bounds = None


class Rectangle(Area):
    def __init__(self, xmin=0, ymin=0, xmax=1, ymax=1):
        super().__init__()

        from shapely.geometry import box
        import geopandas as gpd
        rect = box(xmin, ymin, xmax, ymax)
        gds = gpd.GeoSeries(rect)
        self.polygon = gds
        self.bounds = gds.bounds
        self.area = gds.area
        self.total_bounds = gds.total_bounds


class Shapefile(Area):
    def __init__(self, fpath):
        super().__init__()

        import geopandas as gpd
        gdf = gpd.read_file(fpath)
        self.polygon = gdf
        self.bounds = gdf.bounds
        self.area = gdf.area
        self.total_bounds = gdf.total_bounds
