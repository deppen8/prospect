

from .simulation import Base

from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship


class Surveyor(Base):
    __tablename__ = 'surveyors'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    surveyor_type = Column('surveyor_type', String(50))
    skill = Column('skill', PickleType)
    speed_penalty = Column('speed_penalty', PickleType)

    # relationships
    team_name = Column('team_name', String(50), ForeignKey('teams.name'))
    team = relationship("Team", back_populates='surveyors')
