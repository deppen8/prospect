"""
Create and modify Area objects
"""

from shapely.geometry import box
import geopandas as gpd

class Area(object):
    '''Define the space where the survey will occur    
    '''

    def __init__(self,
                 name='area',
                 xmin=0.0, ymin=0.0, xmax=1.0, ymax=1.0,
                 vis=1.0
                 ):
        '''Create simple rectangular `Area`
        
        Parameters
        ----------
        name : str, optional
            Unique name for this area
        xmin : float, optional
            Minimum horizontal bound
        ymin : float, optional
            Minimum vertical bound
        xmax : float, optional
            Maximum horizontal bound
        ymax : float, optional
            Maximum vertical bound
        vis : float, optional
            Scalar value for surface visibility
        '''
        rect = box(xmin, ymin, xmax, ymax)
        self.data = gpd.GeoDataFrame({'area_name':[name],
                                      'visibility': [vis],
                                      'geometry': rect}, 
                                      geometry='geometry'
                                    )

    def from_shapefile(self, path):
        """Read shapefile as Area
        
        Parameters
        ----------
        path : str
            File path to shapefile
        """

        tmp_gdf = gpd.read_file(path)
        self.data.geometry = tmp_gdf.geometry
        

# class Area:
#     def __init__(self):
#         self.polygon = None
#         self.bounds = None
#         self.area = None
#         self.total_bounds = None


# class Rectangle(Area):
#     def __init__(self, xmin=0, ymin=0, xmax=1, ymax=1):
#         super().__init__()

#         from shapely.geometry import box
#         import geopandas as gpd
#         rect = box(xmin, ymin, xmax, ymax)
#         gds = gpd.GeoSeries(rect)
#         self.polygon = gds
#         self.bounds = gds.bounds
#         self.area = gds.area
#         self.total_bounds = gds.total_bounds


# class Shapefile(Area):
#     def __init__(self, fpath):
#         super().__init__()

#         import geopandas as gpd
#         gdf = gpd.read_file(fpath)
#         self.polygon = gdf
#         self.bounds = gdf.bounds
#         self.area = gdf.area
#         self.total_bounds = gdf.total_bounds
