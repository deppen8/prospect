
from .simulation import Base

from sqlalchemy import Column, Integer, String, Float, ForeignKey, PickleType
from sqlalchemy.orm import relationship


class SurveyUnit(Base):
    __tablename__ = 'surveyunits'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    min_time_per_unit = Column('min_time_per_unit', Float)
    shape = Column('shape', PickleType)

    # relationships
    coverage_name = Column('coverage_name', String(50),
                           ForeignKey('coverages.name'))
    coverage = relationship('Coverage', back_populates='surveyunit')
