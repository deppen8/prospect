from typing import List

import pandas as pd

from .surveyor import Surveyor


class Team:
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

    def __init__(
        self, name: str, surveyor_list: List[Surveyor], assignment: str = "naive",
    ):
        """Create a `Team` instance."""

        self.name = name
        self.surveyor_list = surveyor_list
        self.assignment = assignment  # TODO

        self.df = pd.DataFrame([surveyor.to_dict() for surveyor in self.surveyor_list])

    def add_surveyors(self, surveyors: List[Surveyor]):
        """Update the Team with a new surveyor or surveyors

        Parameters
        ----------
        surveyors : list of Surveyor objects
        """
        self.surveyor_list += surveyors

        self.df = pd.DataFrame([surveyor.to_dict() for surveyor in self.surveyor_list])

    def drop_surveyors(self, surveyors: List[str]):
        """Remove a surveyor or surveyors from the Team

        Parameters
        ----------
        surveyors : list of str
            List of surveyor.name attributes for the surveyors you want to remove
        """
        self.surveyor_list = [s for s in self.surveyor_list if s.name not in surveyors]

        self.df = self.df[~self.df["surveyor_name"].isin(surveyors)]
