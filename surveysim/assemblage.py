
from .simulation import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Assemblage(Base):
    __tablename__ = 'assemblages'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)

    # relationships
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    survey = relationship("Survey", back_populates='assemblage')

    area_name = Column('area_name', String(50), ForeignKey('areas.name'))
    area = relationship("Area", back_populates='assemblages')

    layers = relationship("Layer", back_populates='assemblage')

    # features = relationship("Feature", back_populates='assemblage')
