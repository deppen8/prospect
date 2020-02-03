from .simulation import Base
from .surveyor import Surveyor

from typing import List, Union

from sqlalchemy import Column, String, PickleType
from sqlalchemy.orm import relationship

import pandas as pd


class Team(Base):
    """A collection of `Surveyor` objects.

    Parameters
    ----------
    name : str
        Unique name for the team
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
    surveyor_list : List[Surveyor]
        List of surveyors that make up the team
    assignment : str
        Strategy for assigning team members to survey units.
    df : pandas DataFrame
        `DataFrame` with a row for each surveyor
    """

    __tablename__ = "teams"

    name = Column(
        "name",
        String(50),
        primary_key=True,
        sqlite_on_conflict_unique="IGNORE",
    )
    surveyor_list = Column("surveyor_list", PickleType)

    # relationships
    surveyors = relationship("Surveyor")

    def __init__(
        self,
        name: str,
        surveyor_list: List[Surveyor],
        assignment: str = "naive",
    ):
        """Create a `Team` instance.
        """

        self.name = name
        self.surveyor_list = surveyor_list
        self.assignment = assignment  # TODO

        self.df = pd.DataFrame(
            [surveyor.to_dict() for surveyor in self.surveyor_list]
        )

    def add_surveyor(self, new_surveyors: Union[Surveyor, List[Surveyor]]):
        """Update the Team with a new surveyor or surveyors

        Parameters
        ----------
        new_surveyors : Surveyor or list of Surveyor objects
            [description]
        """
        if isinstance(new_surveyors, list):
            self.surveyor_list += new_surveyors
        elif isinstance(new_surveyors, Surveyor):
            self.surveyor_list.append(new_surveyors)
        else:
            raise TypeError(
                "new_surveyors must be a Surveyor or list of Surveyor objects"
            )

        self.df = pd.DataFrame(
            [surveyor.to_dict() for surveyor in self.surveyor_list]
        )

    def add_to(self, session):
        """Add `Team` and constituent `Surveyor` objects to sqlalchemy session

        Parameters
        ----------
        session : [type]
            [description]
        """
        for surveyor in self.surveyor_list:
            surveyor.add_to(session)
        session.merge(self)
