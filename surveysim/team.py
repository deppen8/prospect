# START HERE: document Team class
from .simulation import Base
from .surveyor import Surveyor

from typing import List

from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship

import pandas as pd


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    surveyor_list = Column('surveyor_list', PickleType)

    # relationships
    survey = relationship("Survey", back_populates='team')
    surveyors = relationship("Surveyor", back_populates='team')

    def __init__(self, name: str, survey_name: str, surveyor_list: List[Surveyor]):
        self.name = name
        self.survey_name = survey_name
        self.surveyor_list = surveyor_list

        self.df = pd.DataFrame([surveyor.to_dict()
                                for surveyor in self.surveyor_list])
