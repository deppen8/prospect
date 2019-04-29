from .simulation import Base

from typing import Union, Tuple
import warnings

from sqlalchemy import Column, String, PickleType
# from sqlalchemy.orm import relationship

from scipy.stats._distn_infrastructure import rv_frozen
from shapely.geometry import box, Polygon
import geopandas as gpd


class Area(Base):
    """Spatial extent of the survey

    Parameters
    ----------
    name : str
        Unique name for the area
    shape : Polygon
        Geographic specification
    vis : Union[float, rv_frozen], optional
        Surface visibility (the default is 1.0, which means perfect surface
        visibility)

    Attributes
    ----------
    name : str
        Name of the area
    shape : Polygon
        Geographic specification
    vis : Union[float, rv_frozen]
        Surface visibility
    df : geopandas GeoDataFrame
        GeoDataFrame with one row that summarizes the area's attributes
    """

    __tablename__ = "areas"

    name = Column(
        "name",
        String(50),
        primary_key=True,
        sqlite_on_conflict_unique="IGNORE",
    )
    shape = Column("shape", PickleType)
    vis = Column("vis", PickleType)
    df = Column("df", PickleType)

    # relationships
    # assemblages = relationship("Assemblage")
    # layers = relationship("Layer")
    # coverage = relationship("Coverage")

    def __init__(
        self, name: str, shape: Polygon, vis: Union[float, rv_frozen] = 1.0
    ):
        """Create an `Area` instance
        """

        self.name = name
        self.shape = shape
        self.vis = vis
        self.df = gpd.GeoDataFrame(
            {"name": [self.name], "shape": self.shape, "vis": [self.vis]},
            geometry="shape",
        )

    def __repr__(self):
        return f"Area(name={repr(self.name)}, shape={repr(self.shape)}, \
        vis={repr(self.vis)})"

    def __str__(self):
        return f"Area object '{self.name}'"

    @classmethod
    def from_shapefile(
        cls, name: str, path: str, vis: Union[float, rv_frozen] = 1.0
    ) -> "Area":
        """Create an `Area` object from a shapefile

        Parameters
        ----------
        name : str
            Unique name for the area
        path : str
            File path to the shapefile
        vis : Union[float, rv_frozen]
            Surface visibility

        Returns
        -------
        Area
        """

        tmp_gdf = gpd.read_file(path)

        if tmp_gdf.shape[0] > 1:
            warnings.warn(
                "Shapefile has more than one feature. Using only the first."
            )

        return cls(name=name, shape=tmp_gdf.geometry.iloc[0], vis=vis)

    @classmethod
    def from_area_value(
        cls,
        name: str,
        value: float,
        origin: Tuple[float, float] = (0.0, 0.0),
        vis: Union[float, rv_frozen] = 1.0,
    ) -> "Area":
        """Create a square `Area` object by specifying its area

        Parameters
        ----------
        name : str
            Unique name for the area
        value : float
            Area of the output shape
        origin : Tuple[float, float]
            Location of the bottom left corner of square
        vis : Union[float, rv_frozen]
            Surface visibility

        Returns
        -------
        Area
        """

        from math import sqrt

        side = sqrt(value)
        square_area = box(
            origin[0], origin[1], origin[0] + side, origin[1] + side
        )
        return cls(name=name, shape=square_area, vis=vis)

    def set_vis_beta_dist(self, alpha: int, beta: int):
        """Define a beta distribution from which to sample visibility values

        Parameters
        ----------
        alpha, beta : int
            Values to define the shape of the beta distribution
        """

        from .utils import beta_dist

        if alpha + beta == 10:
            self.vis = beta_dist(alpha, beta)
            self.df["vis"] = self.vis
        else:
            # TODO: warn or error message
            print("alpha and beta do not sum to 10")

    def set_vis_raster(self, raster):
        """placeholder for future raster support

        Parameters
        ----------
        raster
        """

        pass

    def add_to(self, session):
        session.merge(self)
