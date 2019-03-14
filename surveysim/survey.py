
from .simulation import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Survey(Base):
    """Unique set of `Area`, `Assemblage`, `Coverage`, and `Team`

    Parameters
    ----------
    name : str
        Unique name for the survey

    Attributes
    ----------
    name : str
        Name of the survey

    """

    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)

    # relationships
    area = relationship("Area", uselist=False, back_populates='survey')
    assemblage = relationship(
        "Assemblage", uselist=False, back_populates='survey')
    coverage = relationship("Coverage", uselist=False, back_populates='survey')
    team = relationship("Team", uselist=False, back_populates='survey')

    def __init__(self, name):
        self.name = name
