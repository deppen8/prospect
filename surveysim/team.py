"""
Create a survey team
"""

from .surveyor import Surveyor
import pandas as pd
from typing import List

class Team:
    def __init__(self, name: str, surveyors: List['Surveyor']):
        self.name = name
        self.data = pd.DataFrame({'surveyor_name': [],
                                  'surveyor_type': [],
                                  'skill': [],
                                  'speed_penalty': []
                                  })
        pass

    def add_surveyor(self, surveyor_name: str, surveyor_type: str, skill: float, speed_penalty: float):
        surveyor = Surveyor(surveyor_name, surveyor_type, skill, speed_penalty)
        self.data = pd.concat([self.data, surveyor.data]).reset_index(drop=True)
    
    def remove_surveyor(self, surveyor_name: str):
        """Convenience function to remove a surveyor by name
        
        Parameters
        ----------
        surveyor_name : str
            Name of the surveyor to drop
        
        """
        self.data = self.data.drop(self.data[self.data['name']==surveyor_name])

