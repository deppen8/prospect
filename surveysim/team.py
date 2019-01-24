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
        self.data = pd.DataFrame({'surveyor_name': [],
                                  'surveyor_type': [],
                                  'skill': [],
                                  'speed_penalty': []
                                  })

        for person in surveyors:
            self.data = pd.concat([self.data, person.data]).reset_index(drop=True)

    def remove_surveyor(self, surveyor_name: str):
        """Convenience function to remove a surveyor by name

        Parameters
        ----------
        surveyor_name : str
            Name of the surveyor to drop

        """
        self.data = self.data.drop(
            self.data[self.data['name'] == surveyor_name])
