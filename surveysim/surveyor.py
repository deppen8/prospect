
from .simulation import Base

from typing import Dict, Union

from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from scipy.stats._distn_infrastructure import rv_frozen


class Surveyor(Base):
    """Represents an individual who will participate in the survey.

    Parameters
    ----------
    name : str
        Unique name for the surveyor
    team_name : str
        Name of the parent team
    surveyor_type : str
        A helpful way of grouping surveyors with like traits (e.g., 'student' or 'expert')
    skill : Union[float, rv_frozen], optional
        Assuming perfect visibility and ideal observation rate, what is the expected probability that this person would identify any feature that crossed their survey unit. The default is 1.0, which would mean this surveyor recorded everything they encountered (after controlling for other factors).
    speed_penalty : Union[float, rv_frozen], optional
        Time factor added to each of this surveyor's survey units. The default is 0.0, which applies no penalty. Penalties should range between 0.0 and 1.0.

    Attributes
    ----------
    name : str
        Unique name for the surveyor
    team_name : str
        Name of the parent team
    surveyor_type : str
        A helpful way of grouping surveyors with like traits (e.g., 'student' or 'expert')
    skill : Union[float, rv_frozen]
        Assuming perfect visibility and ideal observation rate, what is the expected probability that this person would identify any feature that crossed their survey unit.
    speed_penalty : Union[float, rv_frozen]
        Time factor added to each of this surveyor's survey units.
    """

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
        """[summary]
        """

        self.name = name
        self.team_name = team_name
        self.surveyor_type = surveyor_type
        self.skill = skill
        self.speed_penalty = speed_penalty

    def to_dict(self) -> Dict:
        """Create dictionary from attributes to allow easy DataFrame creation by `Team`.

        Returns
        -------
        dict
            Dictionary containing pairs of class attributes and their values
        """

        return {
            'surveyor_name': self.name,
            'team_name': self.team_name,
            'surveyor_type': self.surveyor_type,
            'skill': self.skill,
            'speed_penalty': self.speed_penalty
        }
