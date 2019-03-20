
from .simulation import Base
from .surveyor import Surveyor

from typing import List

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship

import pandas as pd


class Team(Base):
    """A collection of `Surveyor` objects.

    Attributes
    ----------
    name : str
        Unique name for the team
    survey_name : str
        Name of the survey
    surveyor_list : List[Surveyor]
        List of surveyors that make up the team
    df : pandas DataFrame
        `DataFrame` with a row for each surveyor
    """

    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    surveyor_list = Column('surveyor_list', PickleType)

    # relationships
    survey = relationship("Survey", back_populates='team')
    surveyors = relationship("Surveyor", back_populates='team')

    def __init__(self, name: str, survey_name: str, surveyor_list: List[Surveyor]):
        """Create a `Team` instance.

        Parameters
        ----------
        name : str
            Unique name for the team
        survey_name : str
            Name of the survey
        surveyor_list : List[Surveyor]
            List of surveyors that make up the team
        """

        self.name = name
        self.survey_name = survey_name
        self.surveyor_list = surveyor_list

        self.df = pd.DataFrame([surveyor.to_dict()
                                for surveyor in self.surveyor_list])
