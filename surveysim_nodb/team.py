"""
Create a survey team
"""
# TODO: documentation

from .surveyor import Surveyor
import pandas as pd
from typing import List


class Team:
    def __init__(self, name: str, surveyors: List[Surveyor]):
        self.name = name
        self.df = pd.DataFrame({'surveyor_name': [],
                                'surveyor_type': [],
                                'skill': [],
                                'speed_penalty': []
                                })

        for person in surveyors:
            self.df = pd.concat([self.df, person.df]
                                ).reset_index(drop=True)

    def remove_surveyor(self, surveyor_name: str):
        """Convenience function to remove a surveyor by name

        Parameters
        ----------
        surveyor_name : str
            Name of the surveyor to drop

        """
        self.df = self.df.drop(
            self.df[self.df['name'] == surveyor_name])
