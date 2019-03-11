
from .simulation import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)

    # relationships
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    survey = relationship("Survey", back_populates='team')

    surveyors = relationship("Surveyor", back_populates='team')
