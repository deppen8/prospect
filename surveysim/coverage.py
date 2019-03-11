
from .simulation import Base

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Coverage(Base):
    __tablename__ = 'coverages'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    survey_unit_type = Column('survey_unit_type', String(50))
    orientation = Column('orientation', Float)
    spacing = Column('spacing', Float)
    sweep_width = Column('sweep_width', Float, default=None)
    radius = Column('radius', Float, default=None)

    # relationships
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    survey = relationship("Survey", back_populates='coverage')

    area_name = Column('area_name', String(50), ForeignKey('areas.name'))
    area = relationship("Area", back_populates='coverage')

    surveyunit = relationship('SurveyUnit', back_populates='coverage')
