
from .simulation import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Survey(Base):
    """Unique index for a set of `Area`, `Assemblage`, `Coverage`, and `Team`

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

    def __init__(self, name: str):
        """Create `Survey` instance
        """

        self.name = name

    def plot(self, area=None, assemblage=None, layers=None, features=None, coverage=None, surveyunits=None, team=None):
        """method to create plot matrix for all building blocks

        Useful for quick inspections of the survey elements

        """

        pass
