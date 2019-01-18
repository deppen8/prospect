"""
Create and modify Area objects
"""
# TODO: get better/more example datasets
# TODO: coordinate systems and projections...UGGGGGHHH

from typing import Tuple
from shapely.geometry import box, Polygon
import geopandas as gpd

class Area:
    """Define the space where the survey will occur

    Attributes
    ----------
    name : str
        Unique name for the `Area`
    vis : float or other #TODO: update this when `set_vis()` is done
        Surface visibility specification
    vis_type : {'scalar', 'distribution', 'surface'}
        The nature of the visibility specification
    shape : shapely `Polygon`
        Shapely `Polygon` object that defines the spatial boundaries of the Area
    data : geopandas `GeoDataFrame`
        Handy container for the other attributes
    """

    def __init__(self, name: str = 'area', shape: Polygon = None, visibility: float = 1.0):
        """Initialize an `Area` object
        
        Parameters
        ----------
        name : str, optional
            Unique name for the `Area`
        shape : shapely `Polygon`, optional
            A shapely `Polygon` object
        visibility : float, optional
            Visibility scalar value. This is set to 1.0 when an `Area` is first created.
            More complicated visibility can be specified with the `set_vis()` method.
        """

        self.name = name
        self.vis = visibility
        self.vis_type = "scalar"
        self.shape = shape
        self.data = gpd.GeoDataFrame({'area_name':[self.name],
                                      'visibility': [self.vis],
                                      'geometry': self.shape}, 
                                      geometry='geometry'
                                    )

    
    def __repr__(self):
        return f"Area(name={repr(self.name)}, shape={repr(self.shape)}, vis={repr(self.vis)})"


    def __str__(self):
        return f"Area object named '{self.name}'"
    

    @classmethod
    def from_shapefile(cls, name: str, path: str) -> 'Area':
        """Create an `Area` object from a shapefile
        
        Parameters
        ----------
        name : str
            Unique name for the `Area`
        path : str
            File path to the shapefile
        """
        
        # TODO: check that shapefile only has one feature (e.g., tmp_gdf.shape[0]==1)
        tmp_gdf = gpd.read_file(path)
        return cls(name, tmp_gdf['geometry'].iloc[0])
    
    
    @classmethod
    def from_shapely_polygon(cls, name: str, polygon: Polygon) -> 'Area':
        """Create an `Area` object from a shapely `Polygon`
        
        Parameters
        ----------
        name : str
            Unique name for the `Area`
        polygon : shapely `Polygon`
            A shapely `Polygon` object
        """
        
        return cls(name, polygon)
    

    @classmethod
    def from_area_value(cls, name: str, value: float, origin: Tuple[float, float] = (0.0, 0.0)) -> 'Area':
        """Create a square `Area` object by specifying its area

        Parameters
        ----------
        name : str
            Unique name for the `Area`
        value : int or float
            Desired area in square units
        origin : tuple of floats
            Specify the lower left corner of the `Area`
        """
        
        from math import sqrt
        side = sqrt(value)
        square_area = box(origin[0], origin[1], origin[0]+side, origin[1]+side)
        return cls(name, square_area)


    def set_vis(self, visibility):
        # TODO: pass in distribution parameters
        from numpy import ndarray
        if isinstance(visibility, (int, float)):
            self.vis = visibility
            self.vis_type = "scalar"
            self.data['visibility'] = self.vis
        elif isinstance(visibility, ndarray):
            # TODO: accept raster or raster-like (e.g., ndarray)
            pass
