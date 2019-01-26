"""
Create survey team members
"""
# TODO: documentation

import pandas as pd


class Surveyor:
    """
    Create a person
    """

    def __init__(self, name: str, surveyor_type: str, skill: float, speed_penalty: float):
        self.name = name
        self.surveyor_type = surveyor_type
        self.skill = skill
        self.speed_penalty = speed_penalty
        self.df = pd.DataFrame({'surveyor_name': [self.name], 'surveyor_type': [
            self.surveyor_type], 'skill': [self.skill], 'speed_penalty': [self.speed_penalty]})

    def set_skill_beta_dist(self, alpha: int, beta: int):
        """Define a beta distribution from which to sample skill values

        Parameters
        ----------
        alpha, beta : int
            Values to define the shape of the beta distribution
        """

        from .utils import make_beta_distribution

        if alpha + beta == 10:
            self.skill = make_beta_distribution(alpha, beta)
            self.df['skill'] = self.skill
        else:
            # TODO: warn or error message
            print('alpha and beta do not sum to 10')

    def set_speed_penalty_truncnorm_dist(self, mean: float, sd: float, lower: float, upper: float):
        from .utils import make_truncnorm_distribution

        self.speed_penalty = make_truncnorm_distribution(
            mean, sd, lower, upper)
        self.df['speed_penalty'] = self.speed_penalty
