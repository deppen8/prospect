
from .simulation import Base

from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from typing import Dict, Union

from shapely.geometry import Polygon
from scipy.stats._distn_infrastructure import rv_frozen


class SurveyUnit(Base):
    __tablename__ = 'surveyunits'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    coverage_name = Column('coverage_name', String(50),
                           ForeignKey('coverages.name'))
    shape = Column('shape', PickleType)
    surveyunit_type = Column('surveyunit_type', String(50))
    min_time_per_unit = Column('min_time_per_unit', PickleType)
    base_time = Column('base_time', PickleType)

    # relationships
    coverage = relationship('Coverage', back_populates='surveyunit')

    def __init__(self, name: str, coverage_name: str, shape: Polygon, surveyunit_type: str, length: float = None, radius: float = None, min_time_per_unit: Union[float, rv_frozen] = 0.0):
        self.name = name
        self.coverage_name = coverage_name
        self.shape = shape
        self.surveyunit_type = surveyunit_type
        self.surveyunit_area = self.shape.area
        self.length = length
        self.radius = radius
        self.min_time_per_unit = min_time_per_unit
        self.base_time = None

    def to_dict(self) -> Dict:
        return {'surveyunit_name': self.name, 'coverage_name': self.coverage_name, 'shape': self.shape, 'surveyunit_type': self.surveyunit_type, 'surveyunit_area': self.surveyunit_area, 'length': self.length, 'radius': self.radius, 'min_time_per_unit': self.min_time_per_unit}
