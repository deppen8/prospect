
from .simulation import Base

from typing import Union, Tuple

from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from scipy.stats._distn_infrastructure import rv_frozen
from shapely.geometry import box, Polygon
import geopandas as gpd


class Area(Base):
    """Spatial extent of the survey

    Attributes
    ----------
    name : str
        Name of the area
    survey_name : str
        Name of the associated `Survey`
    shape : Polygon
        Geographic specification
    vis : Union[float, rv_frozen]
        Surface visibility
    df : geopandas GeoDataFrame
        GeoDataFrame with one row that summarizes the area's attributes
    """

    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.id'))
    shape = Column('shape', PickleType)
    vis = Column('vis', PickleType)
    df = Column('df', PickleType)

    # relationships
    survey = relationship("Survey", back_populates='area')
    assemblages = relationship("Assemblage", back_populates='area')
    layers = relationship("Layer", back_populates='area')
    coverage = relationship("Coverage", back_populates='area')

    def __init__(self, name: str, survey_name: str, shape: Polygon, vis: Union[float, rv_frozen] = 1.0):
        """Create an `Area` instance

        Parameters
        ----------
        name : str
            Unique name for the area
        survey_name : str
            Name of the associated `Survey`
        shape : Polygon
            Geographic specification
        vis : Union[float, rv_frozen], optional
            Surface visibility (the default is 1.0, which means perfect surface visibility)
        """

        self.name = name
        self.survey_name = survey_name
        self.shape = shape
        self.vis = vis
        self.df = gpd.GeoDataFrame(
            {'name': [self.name], 'survey_name': [self.survey_name], 'shape': self.shape, 'vis': [self.vis]}, geometry='shape')

    def __repr__(self):
        return f"Area(name={repr(self.name)}, survey_name={repr(self.survey_name)}, shape={repr(self.shape)}, vis={repr(self.vis)})"

    def __str__(self):
        return f"Area object '{self.name}'"

    @classmethod
    def from_shapefile(cls, name: str, survey_name: str, path: str, vis: Union[float, rv_frozen] = 1.0) -> 'Area':
        """Create an `Area` object from a shapefile

        Parameters
        ----------
        name : str
            Unique name for the area
        survey_name : str
            Name of the associated survey
        path : str
            File path to the shapefile
        vis : Union[float, rv_frozen]
            Surface visibility

        Returns
        -------
        Area
        """

        # TODO: check that shapefile only has one feature (e.g., tmp_gdf.shape[0]==1)
        tmp_gdf = gpd.read_file(path)
        return cls(name=name, survey_name=survey_name, shape=tmp_gdf.geometry.iloc[0], vis=vis)

    @classmethod
    def from_area_value(cls, name: str, survey_name: str, value: float, origin: Tuple[float, float] = (0.0, 0.0), vis: Union[float, rv_frozen] = 1.0) -> 'Area':
        """Create a square `Area` object by specifying its area

        Parameters
        ----------
        name : str
            Unique name for the area
        survey_name : str
            Name of the associated survey
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
        square_area = box(origin[0], origin[1],
                          origin[0] + side, origin[1] + side)
        return cls(name=name, survey_name=survey_name, shape=square_area, vis=vis)

    def set_vis_beta_dist(self, alpha: int, beta: int):
        """Define a beta distribution from which to sample visibility values

        Parameters
        ----------
        alpha, beta : int
            Values to define the shape of the beta distribution
        """

        from .utils import make_beta_distribution

        if alpha + beta == 10:
            self.vis = make_beta_distribution(alpha, beta)
            self.df['vis'] = self.vis
        else:
            # TODO: warn or error message
            print('alpha and beta do not sum to 10')

    def set_vis_raster(self, raster):
        """placeholder for future raster support

        Parameters
        ----------
        raster
        """

        pass
