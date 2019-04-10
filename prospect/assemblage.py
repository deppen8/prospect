from .simulation import Base
from .layer import Layer

from typing import List

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship

from geopandas import GeoDataFrame
import pandas as pd


class Assemblage(Base):
    """A collection of all `Layer` objects for a survey

    Parameters
    ----------
    name : str
        Unique name for the assemblage
    survey_name : str
        Name of the survey
    area_name : str
        Name of the containing area
    layer_list : list of Layer
        List of layers that make up the assemblage

    Attributes
    ----------
    name : str
        Name of the assemblage
    survey_name : str
        Name of the survey
    area_name : str
        Name of the containing area
    df : geopandas GeoDataFrame
        `GeoDataFrame` with a row for each feature in the assemblage
    """

    __tablename__ = "assemblages"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(50), unique=True)
    survey_name = Column("survey_name", String(50), ForeignKey("surveys.name"))
    area_name = Column("area_name", String(50), ForeignKey("areas.name"))
    df = Column("df", PickleType)

    # relationships
    survey = relationship("Survey", back_populates="assemblage")
    area = relationship("Area", back_populates="assemblages")
    layers = relationship("Layer", back_populates="assemblage")
    # features = relationship("Feature", back_populates='assemblage')

    def __init__(
        self, name: str, survey_name: str, area_name: str, layer_list: List[Layer]
    ):
        """Create an `Assemblage` instance
        """

        self.name = name
        self.survey_name = survey_name
        self.area_name = area_name
        self.df: GeoDataFrame = pd.concat(
            [layer.df for layer in layer_list]
        ).reset_index(drop=True)
