"""
Create an assemblage of artifacts
"""
# TODO: separate point layer creation into its own class that is called by Assemblage?


class Assemblage(object):
    """A collection of shapes representing artifacts
    """
    def __init__(self, area):
        """
        Create an empty dictionary for storing different groups and types of shapes
        """
        self.layers = {}
        self.area = area

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

    def add_poisson_points(self):
        # http://socviz.co/lookatdata.html
        # http://connor-johnson.com/2014/02/25/spatial-point-processes/
        pass

    def add_matern_points(self):
        # http://socviz.co/lookatdata.html
        # http://connor-johnson.com/2014/02/25/spatial-point-processes/
        pass

    def add_thomas_points(self):
        # http://connor-johnson.com/2014/02/25/spatial-point-processes/
        pass
