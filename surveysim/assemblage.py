"""A collection of `Layer` objects

"""


from .simulation import Base
from .layer import Layer

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship

from typing import List

from geopandas import GeoDataFrame
import pandas as pd


class Assemblage(Base):
    __tablename__ = 'assemblages'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    area_name = Column('area_name', String(50), ForeignKey('areas.name'))
    df = Column('df', PickleType)

    # relationships
    survey = relationship("Survey", back_populates='assemblage')
    area = relationship("Area", back_populates='assemblages')
    layers = relationship("Layer", back_populates='assemblage')
    # features = relationship("Feature", back_populates='assemblage')

    def __init__(self, name: str, survey_name: str, area_name: str, layer_list: List[Layer]):
        self.name = name
        self.survey_name = survey_name
        self.area_name = area_name
        self.df: GeoDataFrame = pd.concat(
            [layer.df for layer in layer_list]).reset_index(drop=True)
