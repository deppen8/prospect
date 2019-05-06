from .simulation import Base
from .area import Area
from .assemblage import Assemblage
from .coverage import Coverage
from .team import Team

from typing import Union, List, Tuple
from itertools import cycle
import collections

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from scipy.stats._distn_infrastructure import rv_frozen
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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

    name = Column(
        "name",
        String(50),
        primary_key=True,
        sqlite_on_conflict_unique="IGNORE",
    )
    area_name = Column("area", String(50), ForeignKey("areas.name"))
    assemblage_name = Column(
        "assemblage", String(50), ForeignKey("assemblages.name")
    )
    coverage_name = Column(
        "coverage", String(50), ForeignKey("coverages.name")
    )
    team_name = Column("team", String(50), ForeignKey("teams.name"))

    # relationships
    area = relationship("Area")
    assemblage = relationship("Assemblage")
    coverage = relationship("Coverage")
    team = relationship("Team")

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

    def run(
        self,
        n_runs: int,
        start_run_id: int = 0,
        discovery_threshold: float = 0.0,
        overwrite: bool = True,
    ):
        # TODO:
        # add run_id column to output
        # add parameters
        # threshold probability
        # n_runs
        # start_run_id
        # append_to
        stop_run_id = start_run_id + n_runs
        for run in range(start_run_id, stop_run_id):
            self._resolve(run_id=run)

            # take output from resolve, reassemble into attributes of Survey
            # if overwrite == True: initialize output gdfs
            # if overwrite == False: update output gdfs

        pass

    # START HERE: figure out what _resolve should return. NamedTuple?
    def _resolve(self, run_id: int):
        """Determine input parameters, resolve discovery probabilities, and calculate search times
        """

        def _get_floats_or_distr_vals(item):
            """Duplicate value or randomly select value from distribution,
            depending on type
            """
            if isinstance(item, rv_frozen):
                return item.rvs(size=1)[0]
            elif isinstance(float(item), float):
                return item
            else:
                return np.nan

        def _extract_values(df, input_col):
            return df.loc[:, input_col].apply(_get_floats_or_distr_vals)

        # Create inputs df of features from assemblage
        assemblage_inputs = self.assemblage.df.copy()

        # Extract obs_rate values
        assemblage_inputs.loc[:, "obs_rate"] = _extract_values(
            assemblage_inputs, "ideal_obs_rate"
        )

        # Extract feature time_penalty values
        assemblage_inputs.loc[:, "time_penalty_obs"] = _extract_values(
            assemblage_inputs, "time_penalty"
        )

        # Extract surface visibility values
        # TODO: if raster, extract value from raster
        assemblage_inputs.loc[:, "vis_obs"] = [
            _get_floats_or_distr_vals(self.area.vis)
            for i in range(assemblage_inputs.shape[0])
        ]

        # get survey units
        coverage_inputs = self.coverage.df.copy()

        # extract min_time_per_unit
        coverage_inputs.loc[:, "min_time_per_unit_obs"] = _extract_values(
            coverage_inputs, "min_time_per_unit"
        )

        # calculate search_time
        coverage_inputs.loc[:, "base_search_time"] = np.where(
            coverage_inputs.loc[:, "surveyunit_type"] == "transect",
            coverage_inputs.loc[:, "min_time_per_unit"]
            * coverage_inputs.loc[:, "length"],
            coverage_inputs.loc[:, "min_time_per_unit"],
        )

        # Allocate surveyors to survey units based on method
        # def _assign_surveyors(team, coverage):
        if self.team.assignment == "naive":
            people = cycle(self.team.df.loc[:, "surveyor_name"])
            coverage_inputs["surveyor_name"] = [
                next(people) for i in range(coverage_inputs.shape[0])
            ]
        elif self.team.assignment == "speed":
            # minimize total team time
            # TODO: figure out how to optimize assignment
            # Can calculate:
            # - total search time,
            # - individual surveyor's fraction of the total team time
            pass
        elif self.team.assignment == "random":
            pass

        # Map surveyors to inputs df based on survey units
        coverage_team = coverage_inputs.merge(
            self.team.df, how="left", on="surveyor_name"
        )

        # Extract surveyor speed penalty values
        coverage_team.loc[:, "speed_penalty_obs"] = _extract_values(
            coverage_team, "speed_penalty"
        )

        self.coverage_team = coverage_team

        # Find features that intersect coverage
        assem_cov_team = gpd.sjoin(
            assemblage_inputs, coverage_team, how="left"
        )

        # record which survey unit it intersects (or NaN)
        # if intersects, set proximity to 1.0
        # else set proximity to 0.0
        assem_cov_team.loc[:, "proximity_obs"] = np.where(
            ~assem_cov_team.loc[:, "surveyunit_name"].isna(), 1.0, 0.0
        )

        # Extract surveyor skill values
        assem_cov_team.loc[:, "skill_obs"] = _extract_values(
            assem_cov_team, "skill"
        )

        # Calculate final probability of discovery
        assem_cov_team.loc[:, "discovery_prob"] = (
            assem_cov_team.loc[:, "obs_rate"]
            * assem_cov_team.loc[:, "vis_obs"]
            * assem_cov_team.loc[:, "proximity_obs"]
            * assem_cov_team.loc[:, "skill_obs"]
        )

        assem_cov_team.loc[:, "run"] = run_id

        self.raw = assem_cov_team

        discovery_df = assem_cov_team.loc[
            :,
            [
                "run",
                "feature_name",
                "shape",
                "obs_rate",
                "vis_obs",
                "proximity_obs",
                "skill_obs",
                "discovery_prob",
            ],
        ]

        self.discovery = discovery_df

        # Calculate time stats
        # TODO: Duplicate calculations for threshold and no threshold

        # def _total_time_calc(
        #     df,
        #     out_col="total",
        #     base_col="base_search_time",
        #     t_pen_col="time_penalty_obs",
        #     speed_pen_col="speed_penalty_obs",
        # ):
        #     base_pen = df.loc[:, base_col] + df.loc[:, t_pen_col]
        #     df.loc[:, out_col] = (base_pen) + (
        #         base_pen * df.loc[:, speed_pen_col]
        #     )
        #     return df

        # groupby survey unit
        time_per_surveyunit = (
            self.raw.groupby(
                ["surveyunit_name", "surveyor_name", "base_search_time"]
            )
            .agg({"time_penalty_obs": "sum", "speed_penalty_obs": "mean"})
            .reset_index()
            .rename(columns={"time_penalty_obs": "sum_time_penalty_obs"})
        )

        # base penalty = base search time + sum(artifact penalties)

        # surveyor penalty =
        # base penalty * surveyor penalty factor

        # total time =
        # base penalty + surveyor penalty

        base_pen = (
            time_per_surveyunit.loc[:, "base_search_time"]
            + time_per_surveyunit.loc[:, "sum_time_penalty_obs"]
        )

        surveyor_pen = (
            base_pen * time_per_surveyunit.loc[:, "speed_penalty_obs"]
        )

        # multiply above base
        time_per_surveyunit.loc[:, "total_time_per_surveyunit"] = (
            base_pen + surveyor_pen
        )

        time_per_surveyunit.loc[:, "run"] = run_id

        self.time_surveyunit = time_per_surveyunit.loc[
            :,
            [
                "run",
                "surveyunit_name",
                "surveyor_name",
                "base_search_time",
                "sum_time_penalty_obs",
                "speed_penalty_obs",
                "total_time_per_surveyunit",
            ],
        ]

        self.total_time = self.time_surveyunit.loc[
            :, "total_time_per_surveyunit"
        ].sum()

        # per surveyor
        time_per_surveyor = (
            self.time_surveyunit.groupby("surveyor_name")
            .agg(
                {
                    "base_search_time": "sum",
                    "sum_time_penalty_obs": "sum",
                    "speed_penalty_obs": "mean",
                    "total_time_per_surveyunit": "sum",
                }
            )
            .reset_index()
            .rename(
                columns={
                    "base_search_time": "sum_base_search_time",
                    "total_time_per_surveyunit": "total_time_per_surveyor",
                }
            )
        )

        time_per_surveyor.loc[:, "run"] = run_id

        self.time_surveyor = time_per_surveyor.loc[
            :,
            [
                "run",
                "surveyor_name",
                "sum_base_search_time",
                "sum_time_penalty_obs",
                "speed_penalty_obs",
                "total_time_per_surveyor",
            ],
        ]

    def discovery_plot(
        self,
        title_size: int = 20,
        figsize: Tuple[float, float] = (8.0, 20.0),
        **kwargs,
    ) -> Figure:

        # function to create basemap of polygon outline
        def _make_outline(gdf, ax):
            return gdf.plot(ax=ax, facecolor="white", edgecolor="black")

        fig, axarr = plt.subplots(1, 1, figsize=figsize)

        self.discovery.plot(
            ax=_make_outline(self.area.df, axarr),
            column="discovery_prob",
            legend=False,
            legend_kwds={"loc": (1, 0)},
        )
        axarr.set_title(f"{self.name} (Survey)", fontsize=title_size)

        axarr.set_axis_off()

        plt.close()  # close the plot so that Jupyter won't print it twice

        return fig

    def add_to(self, session):
        self.area.add_to(session)
        self.assemblage.add_to(session)
        self.coverage.add_to(session)
        self.team.add_to(session)
        session.merge(self)
