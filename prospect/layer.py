from typing import List, Tuple, Union

import geopandas as gpd
import numpy as np
from scipy.stats import norm, poisson, uniform
from scipy.stats._distn_infrastructure import rv_frozen
from shapely.geometry import Point

from .area import Area
from .feature import Feature
from .utils import clip_points


class Layer:
    """A container for `Feature` objects

    The `Layer` class is mostly useful as a way to create groups of similar features.

    Parameters
    ----------
    name : str
        Unique name for the layer
    area : Area
        Containing area
    input_features : List[Feature]
        List of features that originally made up the Layer (before clipping)

    Attributes
    ----------
    name : str
        Name of the layer
    input_features : List[Feature]
        List of features that make up the layer
    df : geopandas GeoDataFrame
        `GeoDataFrame` with a row for each feature in the layer
    """

    def __init__(
        self,
        name: str,
        area: Area,
        input_features: List[Feature],
    ):
        """Create a `Layer` instance."""

        self.name = name
        self.input_features = input_features

        self.df = gpd.GeoDataFrame(
            [feature.to_dict() for feature in self.input_features],
            geometry="shape",
        )

        # clip by area
        if all(self.df.geom_type == "Point"):
            tmp_area = area
            self.df = clip_points(self.df, tmp_area.df)

    @classmethod
    def from_shapefile(
        cls,
        path: str,
        name: str,
        area: Area,
        time_penalty: Union[float, rv_frozen] = 0.0,
        ideal_obs_rate: Union[float, rv_frozen] = 1.0,
        **kwargs,
    ) -> "Layer":
        """Create a `Layer` instance from a shapefile.

        Parameters
        ----------
        path : str
            Filepath to the shapefile
        name : str
            Unique name for the layer
        area : Area
            Containing area
        time_penalty : Union[float, rv_frozen], optional
            Minimum amount of time it takes to record a feature (the default is 0.0, which indicates no time cost for feature recording)
        ideal_obs_rate : Union[float, rv_frozen], optional
            Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

            - It lies inside or intersects the Coverage
            - Surface visibility is 100%
            - The surveyor is highly skilled

            The default is 1.0, which indicates that when visibility and surveyor skill allow, the feature will always be recorded.

        Returns
        -------
        Layer
        """

        tmp_gdf = gpd.read_file(path, **kwargs)
        shape_list = tmp_gdf.geometry.tolist()
        feature_list = [
            Feature(
                name=f"{name}_{i}",
                layer_name=name,
                shape=shape_list[i],
                time_penalty=time_penalty,
                ideal_obs_rate=ideal_obs_rate,
            )
            for i in range(len(shape_list))
        ]

        return cls(
            name=name,
            area=area,
            input_features=feature_list,
        )

    @classmethod
    def from_pseudorandom_points(
        cls,
        n: int,
        name: str,
        area: Area,
        time_penalty: Union[float, rv_frozen] = 0.0,
        ideal_obs_rate: Union[float, rv_frozen] = 1.0,
    ) -> "Layer":
        """Create a `Layer` instance of pseudorandom points

        Parameters
        ----------
        n : int
            Number of points to generate
        name : str
            Unique name for the layer
        area : Area
            Containing area
        time_penalty : Union[float, rv_frozen], optional
            Minimum amount of time it takes to record a feature (the default is 0.0, which indicates no time cost for feature recording)
        ideal_obs_rate : Union[float, rv_frozen], optional
            Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

            - It lies inside or intersects the Coverage
            - Surface visibility is 100%
            - The surveyor is highly skilled

            The default is 1.0, which indicates that when visibility and surveyor skill allow, the feature will always be recorded.

        Returns
        -------
        Layer

        See Also
        --------
        from_poisson_points : simple Poisson points `Layer`
        from_thomas_points : good for clusters with centers from Poisson points
        from_matern_points : good for clusters with centers from Poisson points
        """

        tmp_area = area
        bounds = tmp_area.df.total_bounds

        n_pts: int = 0
        feature_list: List[Feature] = []
        while n_pts < n:
            xs = (np.random.random(1) * (bounds[2] - bounds[0])) + bounds[0]
            ys = (np.random.random(1) * (bounds[3] - bounds[1])) + bounds[1]
            points_gds = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])
            shape_list = points_gds.geometry.tolist()
            feature = Feature(
                name=f"{name}_{n_pts}",
                layer_name=name,
                shape=shape_list[0],
                time_penalty=time_penalty,
                ideal_obs_rate=ideal_obs_rate,
            )

            tmp_df = gpd.GeoDataFrame([feature.to_dict()], geometry="shape")

            # clip by area
            clipped_df = clip_points(tmp_df, tmp_area.df)
            if clipped_df.shape[0] > 0:
                feature_list.append(feature)
                n_pts += 1

        return cls(
            name=name,
            area=area,
            input_features=feature_list,
        )

    @classmethod
    def from_poisson_points(
        cls,
        rate: float,
        name: str,
        area: Area,
        time_penalty: Union[float, rv_frozen] = 0.0,
        ideal_obs_rate: Union[float, rv_frozen] = 1.0,
    ) -> "Layer":
        """Create a `Layer` instance of points with a Poisson point process

        Parameters
        ----------
        rate : float
            Theoretical events per unit area across the whole space. See Notes in `poisson_points()` for more details
        name : str
            Unique name for the layer
        area : Area
            Containing area
        time_penalty : Union[float, rv_frozen], optional
            Minimum amount of time it takes to record a feature (the default is 0.0, which indicates no time cost for feature recording)
        ideal_obs_rate : Union[float, rv_frozen], optional
            Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

            - It lies inside or intersects the Coverage
            - Surface visibility is 100%
            - The surveyor is highly skilled

            The default is 1.0, which indicates that when visibility and surveyor skill allow, the feature will always be recorded.

        Returns
        -------
        Layer

        See Also
        --------
        poisson_points : includes details on Poisson point process
        from_pseudorandom_points : faster, naive point creation
        from_thomas_points : good for clusters with centers from Poisson points
        from_matern_points : good for clusters with centers from Poisson points

        Notes
        -----
        The generated point coordinates are not guaranteed to fall within the given area, only within its bounding box. The generated GeoDataFrame, `df`, is clipped by the actual area bounds *after* they are generated, which can result in fewer points than expected. All points will remain in the `input_features`.
        """

        tmp_area = area
        points = cls.poisson_points(tmp_area, rate)
        points_gds = gpd.GeoSeries([Point(xy) for xy in points])
        shape_list = points_gds.geometry.tolist()
        # check to see that some points were created
        assert len(shape_list) > 0, "Parameters resulted in zero points"

        feature_list = [
            Feature(
                name=f"{name}_{i}",
                layer_name=name,
                shape=shape_list[i],
                time_penalty=time_penalty,
                ideal_obs_rate=ideal_obs_rate,
            )
            for i in range(len(shape_list))
        ]

        return cls(
            name=name,
            area=area,
            input_features=feature_list,
        )

    @classmethod
    def from_thomas_points(
        cls,
        parent_rate: float,
        child_rate: float,
        gauss_var: float,
        name: str,
        area: Area,
        time_penalty: Union[float, rv_frozen] = 0.0,
        ideal_obs_rate: Union[float, rv_frozen] = 1.0,
    ) -> "Layer":
        """Create a `Layer` instance with a Thomas point process.

        It has a Poisson number of clusters, each with a Poisson number of points distributed with an isotropic Gaussian distribution of a given variance.

        Parameters
        ----------
        parent_rate : float
            Theoretical clusters per unit area across the whole space. See Notes in `poisson_points()` for more details
        child_rate : float
            Theoretical child points per unit area per cluster across the whole space.
        gauss_var : float
            Variance of the isotropic Gaussian distributions around the cluster centers
        name : str
            Unique name for the layer
        area : Area
            Containing area
        time_penalty : Union[float, rv_frozen], optional
            Minimum amount of time it takes to record a feature (the default is 0.0, which indicates no time cost for feature recording)
        ideal_obs_rate : Union[float, rv_frozen], optional
            Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

            - It lies inside or intersects the Coverage
            - Surface visibility is 100%
            - The surveyor is highly skilled

            The default is 1.0, which indicates that when visibility and surveyor skill allow, the feature will always be recorded.

        Returns
        -------
        Layer

        See Also
        --------
        poisson_points : includes details on Poisson point process
        from_pseudorandom_points : faster, naive point creation
        from_poisson_points : simple Poisson points `Layer`
        from_matern_points : similar process, good for clusters with centers from Poisson points

        Notes
        -----
        1. Parents (cluster centers) are NOT created as points in the output

        2. The generated point coordinates are not guaranteed to fall within the given area, only within its bounding box. The generated GeoDataFrame, `df`, is clipped by the actual area bounds *after* they are generated, which can result in fewer points than expected. All points will remain in the `input_features`.
        """

        tmp_area = area
        parents = cls.poisson_points(tmp_area, parent_rate)
        M = parents.shape[0]

        points = list()
        for i in range(M):
            N = poisson(child_rate).rvs()
            for __ in range(N):
                pdf = norm(loc=parents[i, :2], scale=(gauss_var, gauss_var))
                points.append(list(pdf.rvs(2)))
        points = np.array(points)
        points_gds = gpd.GeoSeries([Point(xy) for xy in points])
        shape_list = points_gds.geometry.tolist()

        # check to see that some points were created
        assert len(shape_list) > 0, "Parameters resulted in zero points"

        feature_list = [
            Feature(
                name=f"{name}_{i}",
                layer_name=name,
                shape=shape_list[i],
                time_penalty=time_penalty,
                ideal_obs_rate=ideal_obs_rate,
            )
            for i in range(len(shape_list))
        ]

        return cls(
            name=name,
            area=area,
            input_features=feature_list,
        )

    @classmethod
    def from_matern_points(
        cls,
        parent_rate: float,
        child_rate: float,
        radius: float,
        name: str,
        area: Area,
        time_penalty: Union[float, rv_frozen] = 0.0,
        ideal_obs_rate: Union[float, rv_frozen] = 1.0,
    ) -> "Layer":
        """Create a `Layer` instance with a Matérn point process.

        It has a Poisson number of clusters, each with a Poisson number of points distributed uniformly across a disk of a given radius.

        Parameters
        ----------
        parent_rate : float
            Theoretical clusters per unit area across the whole space. See Notes in `poisson_points()` for more details
        child_rate : float
            Theoretical child points per unit area per cluster across the whole space.
        radius : float
            Radius of the disk around the cluster centers
        name : str
            Unique name for the layer
        area : Area
            Containing area
        time_penalty : Union[float, rv_frozen], optional
            Minimum amount of time it takes to record a feature (the default is 0.0, which indicates no time cost for feature recording)
        ideal_obs_rate : Union[float, rv_frozen], optional
            Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

            - It lies inside or intersects the Coverage (see below)
            - Surface visibility is 100%
            - The surveyor is highly skilled

            The default is 1.0, which indicates that when visibility and surveyor skill allow, the feature will always be recorded.

        Returns
        -------
        Layer

        See Also
        --------
        poisson_points : includes details on Poisson point process
        from_pseudorandom_points : faster, naive point creation
        from_poisson_points : simple Poisson points `Layer`
        from_thomas_points : similar process, good for clusters with centers from Poisson points
        uniform_disk : function used to specify point locations around parents

        Notes
        -----
        1. Parents (cluster centers) are NOT created as points in the output

        2. The generated point coordinates are not guaranteed to fall within the given area, only within its bounding box. The generated GeoDataFrame, `df`, is clipped by the actual area bounds *after* they are generated, which can result in fewer points than expected. All points will remain in the `input_features`.
        """

        tmp_area = area
        parents = cls.poisson_points(tmp_area, parent_rate)
        M = parents.shape[0]

        points = list()
        for i in range(M):
            N = poisson(child_rate).rvs()
            for __ in range(N):
                x, y = cls.uniform_disk(parents[i, 0], parents[i, 1], radius)
                points.append([x, y])
        points = np.array(points)
        points_gds = gpd.GeoSeries([Point(xy) for xy in points])
        shape_list = points_gds.geometry.tolist()

        # check to see that some points were created
        assert len(shape_list) > 0, "Parameters resulted in zero points"

        feature_list = [
            Feature(
                name=f"{name}_{i}",
                layer_name=name,
                shape=shape_list[i],
                time_penalty=time_penalty,
                ideal_obs_rate=ideal_obs_rate,
            )
            for i in range(len(shape_list))
        ]

        return cls(
            name=name,
            area=area,
            input_features=feature_list,
        )

    @staticmethod
    def poisson_points(area: Area, rate: float) -> np.ndarray:
        """Create point coordinates from a Poisson process.

        Parameters
        ----------
        area : Area
            Bounding area
        rate : float
            Theoretical events per unit area across the whole space. See Notes for more details

        Returns
        -------
        np.ndarray

        See Also
        --------
        from_poisson_points : creates `Layer` with Poisson process
        from_pseudorandom_points : faster, naive point creation
        from_thomas_points : good for clusters with centers from Poisson points
        from_matern_points : good for clusters with centers from Poisson points

        Notes
        -----
        1. A Poisson point process is usually said to be more "purely" random than most random number generators (like the one used in `from_pseudorandom_points()`)

        2. The rate (usually called "lambda") of the Poisson point process represents the number of events per unit of area per unit of time across some theoretical space of which our `Area` is some subset. In this case, we only have one unit of time, so the rate really represents a theoretical number of events per unit area. For example, if the specified rate is 5, in any 1x1 square, the number of points observed will be drawn randomly from a Poisson distribution with a shape parameter of 5. In practical terms, this means that over many 1x1 areas (or many observations of the same area), the mean number of points observed in that area will approximate 5.
        """

        bounds = area.df.total_bounds
        dx = bounds[2] - bounds[0]
        dy = bounds[3] - bounds[1]

        N = poisson(rate * dx * dy).rvs()
        xs = uniform.rvs(0, dx, ((N, 1))) + bounds[0]
        ys = uniform.rvs(0, dy, ((N, 1))) + bounds[1]
        return np.hstack((xs, ys))

    @staticmethod
    def uniform_disk(x: float, y: float, r: float) -> Tuple[float, float]:
        """Randomly locate a point within a disk of specified radius

        Parameters
        ----------
        x, y : float
            Coordinates of disk center
        r : float
            Radius of the disk

        Returns
        -------
        Tuple[float, float]
            Random point within the disk
        """

        r = uniform(0, r ** 2.0).rvs()
        theta = uniform(0, 2 * np.pi).rvs()
        xt = np.sqrt(r) * np.cos(theta)
        yt = np.sqrt(r) * np.sin(theta)
        return x + xt, y + yt

    # TODO: this.
    @classmethod
    def from_rectangles(cls, area: Area, n: int):
        # random centroid?
        # random rotation?
        # n_polygons?
        # TODO: centroid options: from Poisson, from pseudorandom
        # TODO: rotation: pseudorandom
        #
        #
        # create centroid coords from Poisson
        # create rectangle of given dimensions around centroids
        # rotate

        raise NotImplementedError(
            "`from_rectangles()` will be available in a future version of prospect"
        )
