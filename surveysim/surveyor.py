"""
Create survey team members
"""
# TODO: documentation

import pandas as pd

class Surveyor:
    """
    Create a person

    This class might not be necessary as a separate object now, but I figure it might be useful in the future, so I gave its own class and module
    """

    def __init__(self, name: str, surveyor_type: str, skill: float, speed_penalty: float) -> 'Surveyor':
        self.name = name
        self.surveyor_type = surveyor_type
        self.skill = skill
        self.speed_penalty = speed_penalty
        self.data = pd.DataFrame({'name': [self.name],
                                  'surveyor_type': [self.surveyor_type],
                                  'skill': [self.skill],
                                  'speed_penalty': [self.speed_penalty]
                                  })
