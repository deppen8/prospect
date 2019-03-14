
from .simulation import Base

from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from typing import Dict, Union

from scipy.stats._distn_infrastructure import rv_frozen


class Surveyor(Base):
    __tablename__ = 'surveyors'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    team_name = Column('team_name', String(50), ForeignKey('teams.name'))
    surveyor_type = Column('surveyor_type', String(50))
    skill = Column('skill', PickleType)
    speed_penalty = Column('speed_penalty', PickleType)

    # relationships
    team = relationship("Team", back_populates='surveyors')

    def __init__(self, name: str, team_name: str, surveyor_type: str, skill: Union[float, rv_frozen] = 1.0, speed_penalty: Union[float, rv_frozen] = 0.0):
        self.name = name
        self.team_name = team_name
        self.surveyor_type = surveyor_type
        self.skill = skill
        self.speed_penalty = speed_penalty

    def to_dict(self) -> Dict:
        return {
            'surveyor_name': self.name,
            'team_name': self.team_name,
            'surveyor_type': self.surveyor_type,
            'skill': self.skill,
            'speed_penalty': self.speed_penalty
        }
