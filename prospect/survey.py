from .simulation import Base
from .area import Area
from .assemblage import Assemblage
from .coverage import Coverage
from .team import Team

from typing import Union, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

import numpy as np
from scipy.stats._distn_infrastructure import rv_frozen


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

    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(50), unique=True)

    # relationships
    area = relationship("Area", uselist=False, back_populates="survey")
    assemblage = relationship(
        "Assemblage", uselist=False, back_populates="survey"
    )
    coverage = relationship("Coverage", uselist=False, back_populates="survey")
    team = relationship("Team", uselist=False, back_populates="survey")

    def __init__(
        self,
        name: str,
        area: Area = None,
        assemblage: Assemblage = None,
        coverage: Coverage = None,
        team: Team = None,
    ):
        """Create `Survey` instance
        """

        self.name = name
        self.area = area
        self.assemblage = assemblage
        self.coverage = coverage
        self.team = team

    def add_bb(self, bb: List[Union[Area, Assemblage, Coverage, Team]]):
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

    def run(self):
        """Determine input parameters, resolve discovery probabilities, and calculate search times
        """

        def _get_floats_or_distr_vals(item):
            """Duplicate value or randomly select value from distribution,
            depending on type
            """
            if isinstance(item, rv_frozen):
                return item.rvs(size=1)[0]
            else:
                return item

        # Create inputs df of features from assemblage
        assemblage = self.assemblage.df.copy()

        # Extract obs_rate values
        assemblage.loc[:, "obs_rate"] = assemblage.loc[
            :, "ideal_obs_rate"
        ].apply(_get_floats_or_distr_vals)

        # Extract feature time_penalty values
        assemblage.loc[:, "time_penalty_obs"] = assemblage.loc[
            :, "time_penalty"
        ].apply(_get_floats_or_distr_vals)

        # START HERE
        # Extract surface visibility values
        # if dist, randomly select
        # if scalar, assign
        # TODO: if raster, extract value from raster

        # Find features that intersect coverage
        # record which survey unit it intersects (or NaN)
        # if intersects
        # set proximity to 1.0
        # extract min_time_per_unit
        # if dist, randomly select
        # if scalar, assign
        # else
        # set proximity to 0.0
        # set min_time_per_unit to NaN
        # Allocate surveyors to survey units based on method
        # Map surveyors to inputs df based on survey units
        # Extract surveyor skill values
        # if surveyor name exists
        # if skill is dist, randomly select
        # if skill is scalar, assign
        # elif surveyor name doesn't exist
        # surveyor skill is NaN or 0.0?
        # Extract surveyor speed penalty values
        # if survey name exists
        # if speed penalty is dist, randomly select
        # if speed penalty is scalar, assign
        # elif surveyor name doesn't exist
        # speed penalty is NaN or 1.0?
        # Calculate final probability of discovery

        # Calculate time stats
        # per survey unit
        # per surveyor
        # total time

        pass
