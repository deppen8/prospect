
from .simulation import Base
from .area import Area
from .assemblage import Assemblage
from .coverage import Coverage
from .team import Team

from typing import Union, List

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

    def __init__(self,
                 name: str,
                 area: Area = None,
                 assemblage: Assemblage = None,
                 coverage: Coverage = None,
                 team: Team = None
                 ):
        """Create `Survey` instance
        """

        self.name = name
        self.area = area
        self.assemblage = assemblage
        self.coverage = coverage
        self.team = team

    def add_bb(self, bb: List[Union[Area,
                                    Assemblage,
                                    Coverage,
                                    Team]
                              ]):
        """Attach building blocks to survey.

        Parameters
        ----------
        bb : List[Union[Area, Assemblage, Coverage, Team]]
            List of building block objects

        """
        # TODO: check that bb is a list
        for block in bb:
            if isinstance(block, Area):
                self.area = block
            elif isinstance(block, Assemblage):
                self.assemblage = block
            elif isinstance(block, Coverage):
                self.coverage = block
            elif isinstance(block, Team):
                self.team = block
