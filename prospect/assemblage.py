from .simulation import Base
from .layer import Layer

from typing import List

from sqlalchemy import Column, String, PickleType, ForeignKey
# from sqlalchemy.orm import relationship

from geopandas import GeoDataFrame
import pandas as pd


class Assemblage(Base):
    """A collection of all `Layer` objects for a survey

    Parameters
    ----------
    name : str
        Unique name for the assemblage
    area_name : str
        Name of the containing area
    layer_list : list of Layer
        List of layers that make up the assemblage

    Attributes
    ----------
    name : str
        Name of the assemblage
    area_name : str
        Name of the containing area
    df : geopandas GeoDataFrame
        `GeoDataFrame` with a row for each feature in the assemblage
    """

    __tablename__ = "assemblages"

    name = Column(
        "name",
        String(50),
        primary_key=True,
        sqlite_on_conflict_unique="IGNORE",
    )
    area_name = Column("area_name", String(50), ForeignKey("areas.name"))
    df = Column("df", PickleType)

    # relationships
    # area = relationship("Area")
    # layers = relationship("Layer")
    # features = relationship("Feature", back_populates='assemblage')

    def __init__(self, name: str, area_name: str, layer_list: List[Layer]):
        """Create an `Assemblage` instance
        """

        self.name = name
        self.area_name = area_name
        self.layer_list = layer_list
        self.df: GeoDataFrame = pd.concat(
            [layer.df for layer in self.layer_list]
        ).reset_index(drop=True)

    def __repr__(self):
        return f"Assemblage(name={repr(self.name)}, area_name={repr(self.area_name)}, layer_list={repr(self.layer_list)})"

    def __str__(self):
        return f"Assemblage object '{self.name}'"

    def add_to(self, session):
        for layer in self.layer_list:
            layer.add_to(session)
        session.merge(self)
