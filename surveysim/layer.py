"""
Create and modify Layer objects
"""

from shapely.geometry import Point
import geopandas as gpd
from .area import Area

class Layer:

    def __init__(self, area: Area, name: str, features=None, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        self.area_name = area.name
        self.bounds = area.data.total_bounds
        self.name = name
        self.features = features
        self.n_features = features.shape[0]
        self.time_penalty = time_penalty
        self.ideal_obs_rate = ideal_obs_rate

        self.data = gpd.GeoDataFrame({'layer_name': [self.name] * self.n_features,
                                    'fid': [f'{self.name}_{i}' for i in range(self.n_features)],
                                    'time_penalty': [self.time_penalty] * self.n_features,
                                    'ideal_obs_rate': [self.ideal_obs_rate] * self.n_features,
                                    'geometry': self.features},
                                    geometry = 'geometry'
                                    )


    @classmethod
    def from_shapefile(cls, path: str, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        tmp_gdf = gpd.read_file(path)
        return cls(area, name, tmp_gdf['geometry'], time_penalty, ideal_obs_rate)


    @classmethod
    def from_poisson_points(cls, rate: float, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        from scipy.stats import poisson, uniform
        bounds = area.total_bounds        
        dx = bounds[2] - bounds[0]
        dy = bounds[3] - bounds[1]
        
        n = poisson(rate * dx * dy ).rvs()
        xs = uniform.rvs(0, dx, ((n,1)))
        ys = uniform.rvs(0, dy, ((n,1)))
        
        points = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])
        
        return cls(area, name, points, time_penalty, ideal_obs_rate)


    @classmethod
    def make_polygons(cls):
        pass
