# |￣￣￣￣￣￣ | 
# |    HERE   | 
# |    LIES   | 
# |    OLD    | 
# |    CODE   | 
# | ＿＿＿＿＿ | 
# (\__/) || 
# (•ㅅ•) || 
# / 　 づ

##########################################################################

# |￣￣￣￣￣￣￣￣￣￣ | 
# |    PRE-         | 
# |  @CLASSMETHOD   | 
# |    AREA         | 
# |    MODULE       | 
# | ＿＿＿＿＿＿＿＿＿ | 
# (\__/) || 
# (•ㅅ•) || 
# / 　 づ

    def __init__(self,
                 name,
                 xmin=0.0, ymin=0.0, xmax=1.0, ymax=1.0,
                 vis=1.0
                 ):
        '''Create simple rectangular `Area`
        
        Parameters
        ----------
        name : str
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
        self.name = name
        self.vis = vis
        self.vis_type = 'scalar'
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.shape = self.make_rectangle(self.xmin, self.ymin, self.xmax, self.ymax)

        self.data = gpd.GeoDataFrame({'area_name':[self.name],
                                      'visibility': [self.vis],
                                      'geometry': self.shape}, 
                                      geometry='geometry'
                                    )
    @classmethod
    def from_shapefile(cls, path):
        """Read shapefile as Area
        
        Parameters
        ----------
        path : str
            File path to shapefile
        """
        # TODO: check that shapefile only has one feature (e.g., tmp_gdf.shape[0]==1)
        tmp_gdf = gpd.read_file(path)
        self.data['geometry'] = tmp_gdf['geometry']
        self.shape = self.data['geometry'].iloc[0]
        
        self.update_bounds(self.data)

    def from_shapely_polygon(self, polygon):
        self.shape = polygon
        self.data['geometry'] = self.shape
        self.update_bounds(self.data)
    
    def from_area_value(self, value, origin=(0,0)):
        from math import sqrt
        side = sqrt(value)
        self.xmin = origin[0]
        self.ymin = origin[1]
        self.xmax = self.xmin + side
        self.ymax = self.ymin + side
        self.shape = self.make_rectangle(self.xmin, self.ymin, self.xmax, self.ymax)
        self.data['geometry'] = self.shape
        self.update_bounds(self.data)

    def make_rectangle(self, xmin, ymin, xmax, ymax):
        shape = box(xmin, ymin, xmax, ymax)
        return shape

    def update_bounds(self, gdf):
        bnds = gdf.total_bounds
        self.xmin = bnds[0]
        self.ymin = bnds[1]
        self.xmax = bnds[2]
        self.ymax = bnds[3]


##########################################################################

# |￣￣￣￣￣￣￣￣￣￣￣￣ | 
# |    HERE LIES         | 
# |  A TOO-COMPLICATED   | 
# |    LAYER CLASS       | 
# |    STRUCTURE         | 
# | ＿＿＿＿＿＿＿＿＿＿＿＿ | 
# (\__/) || 
# (•ㅅ•) || 
# / 　 づ

class PointLayer(Layer):
    layer_type = 'point'

    def __init__(self, area: Area, name: str, features=None, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        super().__init__(area, name, features, time_penalty, ideal_obs_rate)        
    
    @classmethod
    def from_shapefile(cls, path: str, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        shp = gpd.read_file(path)
        return cls(area, name, shp['geometry'], time_penalty, ideal_obs_rate)


class PoissonPointLayer(PointLayer):

    layer_type = 'poisson_point'

    def __init__(self, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0, rate: float = 0.2):
        from scipy.stats import poisson, uniform

        super().__init__(area, name, time_penalty, ideal_obs_rate)
        
        dx = self.bounds[2] - self.bounds[0]
        dy = self.bounds[3] - self.bounds[1]
        n = poisson(rate * dx * dy ).rvs()
        xs = uniform.rvs(0, dx, ((n,1)))
        ys = uniform.rvs(0, dy, ((n,1)))
        self.features = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])
        n_points = self.features.shape[0]
        self.data = gpd.GeoDataFrame({'layer_name': [self.name] * n_points,
                                    'fid': [f'{self.name}_{i}' for i in range(n_points)],
                                    'time_penalty': [self.time_penalty] * n_points,
                                    'ideal_obs_rate': [self.ideal_obs_rate] * n_points,
                                    'geometry': self.features},
                                    geometry = 'geometry'
                                    )
