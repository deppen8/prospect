"""
Create and modify Area objects
"""
# TODO: clean up with @classmethod, @staticmethod
# TODO: coordinate systems and projections...UGGGGGHHH

from typing import Tuple
from shapely.geometry import box, Polygon
import geopandas as gpd

class Area:
    '''Define the space where the survey will occur    
    '''

    def __init__(self, name: str, shape: Polygon, vis: float = 1.0):

        self.name = name
        self.vis = vis
        self.vis_type = "scalar"
        self.shape = shape
        self.data = gpd.GeoDataFrame({'area_name':[self.name],
                                      'visibility': [self.vis],
                                      'geometry': self.shape}, 
                                      geometry='geometry'
                                    )

    
    def __repr__(self):
        return f"Area({repr(self.name)}, {repr(self.shape)}, {repr(self.vis)})"


    def __str__(self):
        return f"Area object named '{self.name}'"
    

    @classmethod
    def from_shapefile(cls, name: str, path: str):
        # TODO: check that shapefile only has one feature (e.g., tmp_gdf.shape[0]==1)
        tmp_gdf = gpd.read_file(path)
        return cls(name, tmp_gdf['geometry'].iloc[0])
    
    
    @classmethod
    def from_shapely_polygon(cls, name: str, polygon: Polygon):
        return cls(name, polygon)
    

    @classmethod
    def from_area_value(cls, name: str, value: float, origin: Tuple[float, float] = (0.0, 0.0)):
        from math import sqrt
        side = sqrt(value)
        square_area = box(origin[0], origin[1], origin[0]+side, origin[1]+side)
        return cls(name, square_area)


    def set_visibility(self):
        # TODO: pass in distribution parameters
        # TODO: accept a scalar OR distribution parameters
        pass
