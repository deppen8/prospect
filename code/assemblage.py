"""
Create an assemblage of artifacts
"""


class Assemblage(object):
    """A collection of shapes representing artifacts
    """
    def __init__(self):
        """
        Create an empty dictionary for storing different groups and types of shapes
        """
        self.layers = {}

    def add_random_points(self, name, n, xrange=(0, 1), yrange=(0, 1), s=5):
        """Randomly create a GeoSeries of XY points

        Parameters
        ----------
        name : str
            Name for the layer
        n : int
            Number of points
        xrange, yrange : tuples
            Min and max values for x and y dimensions
        s : int
            Random number seed

        Returns
        -------
        gds : geopandas GeoSeries
            GeoSeries of points
        """
        from numpy.random import seed, random
        from shapely.geometry import Point
        from geopandas import GeoSeries

        seed(s)
        xs = (random(n) * (xrange[1] - xrange[0])) + xrange[0]
        ys = (random(n) * (yrange[1] - yrange[0])) + yrange[0]
        gds = GeoSeries([Point(xy) for xy in zip(xs, ys)])

        self.layers[name] = gds
