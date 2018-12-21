"""
Create and modify Layer objects
"""
# TODO: add docs

from .area import Area

import geopandas as gpd
from shapely.geometry import Point, Polygon

import numpy as np
from scipy.stats import uniform, poisson, norm

class Layer:
    '''Define artifacts/features that will seed the survey `Area`
    
    Attributes
    -------
    area_name : str
        Name of the `Area` where the `Layer` resides
    bounds : numpy array
        Limits of the bounding box of the `Area`
    name : str
        Unique name for `Layer`
    features : numpy `ndarray` or geopandas `GeoDataSeries`
        An object containing all of the shapely objects that make up the Layer
    n_features : int
        Number of artifacts/features in the `Layer`
    time_penalty : float
        Extra time associated with collecting/recording one artifact/feature from this `Layer`
    ideal_obs_rate : float
        The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
            - It lies inside or intersects the `Coverage`
            - Surface visibility is 100%
            - The surveyor is highly skilled
    '''

    def __init__(self, area: Area, name: str, features = None, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        '''Create a `Layer` object
        
        Parameters
        ----------
        area : Area
            `Area` where the `Layer` is to be located
        name : str
            Unique name for the `Layer`
        features : numpy ndarray or geopandas GeoDataSeries, optional
            An object containing all of the shapely objects that will make up the Layer. Technically optional, but `Layer` creation will fail without it.
        time_penalty : float, optional
            Extra time associated with collecting/recording one artifact/feature from this `Layer` (the default is 0.0, which indicates an unrealistic scenario where recording an artifact/feature takes no time at all)
        ideal_obs_rate : float, optional
            The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
                - It lies inside or intersects the `Coverage`
                - Surface visibility is 100%
                - The surveyor is highly skilled 
            (the default is 1.0, which would indicate it is always recorded when encountered)
        '''

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
    def from_shapefile(cls, path: str, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0) -> 'Layer':
        '''Create a `Layer` of artifacts/features from a shapefile
        
        Parameters
        ----------
        path : str
            Filepath to the shapefile
        area : Area
            `Area` where the `Layer` is to be located
        name : str
            Unique name for the `Layer`
        time_penalty : float, optional
            Extra time associated with collecting/recording one artifact/feature from this `Layer` (the default is 0.0, which indicates an unrealistic scenario where recording an artifact/feature takes no time at all)
        ideal_obs_rate : float, optional
            The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
                - It lies inside or intersects the `Coverage`
                - Surface visibility is 100%
                - The surveyor is highly skilled 
            (the default is 1.0, which would indicate it is always recorded when encountered)
        '''

        tmp_gdf = gpd.read_file(path)
        return cls(area, name, tmp_gdf['geometry'], time_penalty, ideal_obs_rate)


    @classmethod
    def from_pseudorandom_points(cls, n: int, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0) -> 'Layer':
        '''Create a `Layer` of pseudorandom points
        
        Parameters
        ----------
        n : int
            Number of points to create
        area : Area
            `Area` where the `Layer` is to be located
        name : str
            Unique name for the `Layer`
        time_penalty : float, optional
            Extra time associated with collecting/recording one artifact/feature from this `Layer` (the default is 0.0, which indicates an unrealistic scenario where recording an artifact/feature takes no time at all)
        ideal_obs_rate : float, optional
            The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
                - It lies inside or intersects the `Coverage`
                - Surface visibility is 100%
                - The surveyor is highly skilled 
            (the default is 1.0, which would indicate it is always recorded when encountered)
        '''

        bounds = area.data.total_bounds
        xs = (np.random.random(n) * (bounds[2] - bounds[0])) + bounds[0]
        ys = (np.random.random(n) * (bounds[3] - bounds[1])) + bounds[1]
        points_gds = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])

        return cls(area, name, points_gds, time_penalty, ideal_obs_rate)


    @classmethod
    def from_poisson_points(cls, rate: float, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0) -> 'Layer':
        '''Create a `Layer` of points with a Poisson point process

        Parameters
        ----------
        rate : float
            Theoretical events per unit area across the whole space. See Notes in `poisson_points()` for more details
        area : Area
            `Area` where the `Layer` is to be located
        name : str
            Unique name for the `Layer`
        time_penalty : float, optional
            Extra time associated with collecting/recording one artifact/feature from this `Layer` (the default is 0.0, which indicates an unrealistic scenario where recording an artifact/feature takes no time at all)
        ideal_obs_rate : float, optional
            The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
                - It lies inside or intersects the `Coverage`
                - Surface visibility is 100%
                - The surveyor is highly skilled 
            (the default is 1.0, which would indicate it is always recorded when encountered)
        
        See Also
        --------
        poisson_points : includes details on Poisson point process
        from_pseudorandom_points : faster, naive point creation
        from_thomas_points : good for clusters with centers from Poisson points
        from_matern_points : good for clusters with centers from Poisson points
        '''

        points = cls.poisson_points(area, rate)
        points_gds = gpd.GeoSeries([Point(xy) for xy in points])
        
        return cls(area, name, points_gds, time_penalty, ideal_obs_rate)


    @classmethod
    def from_thomas_points(cls, parent_rate: float, child_rate: float, gauss_var: float, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0) -> 'Layer':
        '''Create a `Layer` with a Thomas point process. It has a Poisson number of clusters, each with a Poisson number of points distributed with an isotropic Gaussian distribution of a given variance.

        Parameters
        ----------
        parent_rate : float
            Theoretical clusters per unit area across the whole space. See Notes in `poisson_points()` for more details
        child_rate : float
            Theoretical child points per unit area per cluster across the whole space.
        gauss_var : float
            Variance of the isotropic Gaussian distributions around the cluster centers
        area : Area
            `Area` where the `Layer` is to be located
        name : str
            Unique name for the `Layer`
        time_penalty : float, optional
            Extra time associated with collecting/recording one artifact/feature from this `Layer` (the default is 0.0, which indicates an unrealistic scenario where recording an artifact/feature takes no time at all)
        ideal_obs_rate : float, optional
            The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
                - It lies inside or intersects the `Coverage`
                - Surface visibility is 100%
                - The surveyor is highly skilled 
            (the default is 1.0, which would indicate it is always recorded when encountered)
        
        See Also
        --------
        poisson_points : includes details on Poisson point process
        from_pseudorandom_points : faster, naive point creation
        from_poisson_points : simple Poisson points `Layer`
        from_matern_points : similar process, good for clusters with centers from Poisson points
        
        Notes
        -----
        Parents (cluster centers) are NOT created as points in the output
        '''

        parents = cls.poisson_points(area, parent_rate)
        M = parents.shape[0]

        points = list()    
        for i in range(M):
            N = poisson(child_rate).rvs()
            for __ in range(N):            
                pdf = norm(loc=parents[i,:2], scale=(gauss_var,gauss_var))
                points.append(list(pdf.rvs(2)))
        points = np.array(points)
        points_gds = gpd.GeoSeries([Point(xy) for xy in points])

        return cls(area, name, points_gds, time_penalty, ideal_obs_rate)


    @classmethod
    def from_matern_points(cls, parent_rate: float, child_rate: float, radius: float, area: Area, name: str, time_penalty: float = 0.0, ideal_obs_rate: float = 1.0):
        '''Create a `Layer` with a Matérn point process. It has a Poisson number of clusters, each with a Poisson number of points distributed uniformly across a disk of a given radius.

        Parameters
        ----------
        parent_rate : float
            Theoretical clusters per unit area across the whole space. See Notes in `poisson_points()` for more details
        child_rate : float
            Theoretical child points per unit area per cluster across the whole space.
        radius : float
            Radius of the disk around the cluster centers
        area : Area
            `Area` where the `Layer` is to be located
        name : str
            Unique name for the `Layer`
        time_penalty : float, optional
            Extra time associated with collecting/recording one artifact/feature from this `Layer` (the default is 0.0, which indicates an unrealistic scenario where recording an artifact/feature takes no time at all)
        ideal_obs_rate : float, optional
            The frequency with which an artifact or feature from this `Layer` will be recorded, assuming the following ideal conditions: 
                - It lies inside or intersects the `Coverage`
                - Surface visibility is 100%
                - The surveyor is highly skilled 
            (the default is 1.0, which would indicate it is always recorded when encountered)
        
        See Also
        --------
        poisson_points : includes details on Poisson point process
        from_pseudorandom_points : faster, naive point creation
        from_poisson_points : simple Poisson points `Layer`
        from_thomas_points : similar process, good for clusters with centers from Poisson points
        uniform_disk : function used to specify point locations around parents
        
        Notes
        -----
        Parents (cluster centers) are NOT created as points in the output
        '''

        parents = cls.poisson_points(area, parent_rate)
        M = parents.shape[0]
        
        points = list()
        for i in range(M):
            N = poisson(child_rate).rvs()
            for __ in range(N):
                x, y = cls.uniform_disk(parents[i,0], parents[i,1], radius)
                points.append([x, y])
        points = np.array(points)
        points_gds = gpd.GeoSeries([Point(xy) for xy in points])

        return cls(area, name, points_gds, time_penalty, ideal_obs_rate)


    @staticmethod
    def poisson_points(area: Area, rate: float):
        '''Create points from a Poisson process
        
        Parameters
        ----------
        area : Area
            `Area` where the points will be located
        rate : float
            Theoretical events per unit area across the whole space. See Notes for more details
        
        Returns
        -------
        numpy ndarray of tuples
            An array of xy coordinate pairs
        
        See Also
        --------
        from_poisson_points : creates `Layer` with Poisson process
        from_pseudorandom_points : faster, naive point creation
        from_thomas_points : good for clusters with centers from Poisson points
        from_matern_points : good for clusters with centers from Poisson points

        Notes
        -----
        A Poisson point process is usually said to be more "purely" random than most random number generators (like the one used in `from_pseudorandom_points()`)

        The rate (usually called "lambda") of the Poisson point process represents the number of events per unit of area per unit of time across some theoretical space of which our `Area` is some subset. In this case, we only have one unit of time, so the rate really represents a theoretical number of events per unit area. For example, if the specified rate is 5, in any 1x1 square, the number of points observed will be drawn randomly from a Poisson distribution with a shape parameter of 5. In practical terms, this means that over many 1x1 areas (or many observations of the same area), the mean number of points observed in that area will approximate 5.
        '''
        
        bounds = area.data.total_bounds        
        dx = bounds[2] - bounds[0]
        dy = bounds[3] - bounds[1]

        N = poisson(rate * dx * dy).rvs()
        xs = uniform.rvs(0, dx, ((N,1)))
        ys = uniform.rvs(0, dy, ((N,1)))
        return np.hstack((xs, ys))


    @staticmethod
    def uniform_disk(x, y, r):
        '''Randomly locate a point within a disk of specified radius

        Parameters
        ----------
        x, y : float
            Coordinates of disk center
        r : float
            Radius of the disk

        Returns
        -------
        tuple of floats
            Random point within the disk
        '''

        r = uniform(0, r**2.0).rvs()
        theta = uniform(0, 2*np.pi).rvs()
        xt = np.sqrt(r) * np.cos(theta)
        yt = np.sqrt(r) * np.sin(theta)
        return x+xt, y+yt


    # TODO: this.
    @classmethod
    def make_polygons(cls):
        # random centroid?
        # random rotation?
        # n_polygons?
        pass
