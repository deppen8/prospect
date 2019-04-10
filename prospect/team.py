from .simulation import Base
from .surveyor import Surveyor

from typing import List

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship

import pandas as pd


class Team(Base):
    """A collection of `Surveyor` objects.

    Parameters
    ----------
    name : str
        Unique name for the team
    survey_name : str
        Name of the survey
    surveyor_list : List[Surveyor]
        List of surveyors that make up the team
    assignment : {'naive', 'speed', 'random'}
        Strategy for assigning team members to survey units.
        
        * 'naive' - cycle through `Team.df` in index order, assigning surveyors
          to survey units in `Coverage.df` in index order until all survey
          units have a surveyor.
        * 'speed' - calculate the total base time required for the coverage and
          allocate survey units proportional to surveyor speed.
        * 'random' - for each survey unit, randomly select (with replacement)
          a surveyor from the team

    Attributes
    ----------
    name : str
        Unique name for the team
    survey_name : str
        Name of the survey
    surveyor_list : List[Surveyor]
        List of surveyors that make up the team
    assignment : str
        Strategy for assigning team members to survey units. 
    df : pandas DataFrame
        `DataFrame` with a row for each surveyor
    """

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(50), unique=True)
    survey_name = Column("survey_name", String(50), ForeignKey("surveys.name"))
    surveyor_list = Column("surveyor_list", PickleType)

    # relationships
    survey = relationship("Survey", back_populates="team")
    surveyors = relationship("Surveyor", back_populates="team")

    def __init__(
        self,
        name: str,
        survey_name: str,
        surveyor_list: List[Surveyor],
        assignment: str = "naive",
    ):
        """Create a `Team` instance.
        """

        self.name = name
        self.survey_name = survey_name
        self.surveyor_list = surveyor_list
        self.assignment = assignment  # TODO

        self.df = pd.DataFrame([surveyor.to_dict() for surveyor in self.surveyor_list])
