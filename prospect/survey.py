import collections
from itertools import cycle
from typing import List, Tuple, Union

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats._distn_infrastructure import rv_frozen

from .area import Area
from .assemblage import Assemblage
from .coverage import Coverage
from .team import Team


class Survey:
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

    def __init__(
        self,
        name: str,
        area: Area = None,
        assemblage: Assemblage = None,
        coverage: Coverage = None,
        team: Team = None,
    ):
        """Create `Survey` instance"""

        self.name = name
        self.area = area
        self.assemblage = assemblage
        self.coverage = coverage
        self.team = team

        # initialize empty outputs
        self.raw = None
        self.discovery = None
        self.time_surveyunit = None
        self.time_surveyor = None
        self.total_time = 0

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
        overwrite: bool = False,
    ):

        stop_run_id = start_run_id + n_runs

        if overwrite:
            self.raw = None
            self.discovery = None
            self.time_surveyunit = None
            self.time_surveyor = None
            self.total_time = 0

        resolved_runs = [
            _resolve(self, run_id=run_id) for run_id in range(start_run_id, stop_run_id)
        ]

        # first concat outputs, then concat those with class attributes
        # From pandas.concat() docs: Any None objects will be dropped silently unless they are all None in which case a ValueError will be raised
        raws = pd.concat([run.raw for run in resolved_runs], ignore_index=True)
        self.raw = pd.concat([self.raw, raws], ignore_index=True)

        discoveries = pd.concat(
            [run.discovery for run in resolved_runs], ignore_index=True
        )
        self.discovery = pd.concat([self.discovery, discoveries], ignore_index=True)

        time_surveyunits = pd.concat(
            [run.time_surveyunit for run in resolved_runs], ignore_index=True
        )
        self.time_surveyunit = pd.concat(
            [self.time_surveyunit, time_surveyunits], ignore_index=True
        )

        time_surveyors = pd.concat(
            [run.time_surveyor for run in resolved_runs], ignore_index=True
        )
        self.time_surveyor = pd.concat(
            [self.time_surveyor, time_surveyors], ignore_index=True
        )

        for i in range(len(resolved_runs)):
            self.total_time += resolved_runs[i].total_time

    def discovery_plot(
        self,
        title_size: int = 20,
        figsize: Tuple[float, float] = (8.0, 20.0),
        **kwargs,
    ) -> Figure:

        # TODO: raise error if self.discovery is None
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


def _resolve(survey, run_id: int):
    """Determine input parameters, resolve discovery probabilities, and calculate search times"""

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

    ResolvedRun = collections.namedtuple(
        "ResolvedRun", "raw discovery time_surveyunit time_surveyor total_time",
    )

    # Create inputs df of features from assemblage
    assemblage_inputs = survey.assemblage.df.copy()

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
        _get_floats_or_distr_vals(survey.area.vis)
        for i in range(assemblage_inputs.shape[0])
    ]

    # get survey units
    coverage_inputs = survey.coverage.df.copy()

    # extract min_time_per_unit
    coverage_inputs.loc[:, "min_time_per_unit_obs"] = _extract_values(
        coverage_inputs, "min_time_per_unit"
    )

    # calculate search_time
    coverage_inputs.loc[:, "base_search_time"] = np.where(
        coverage_inputs.loc[:, "surveyunit_type"] == "transect",
        coverage_inputs.loc[:, "min_time_per_unit"] * coverage_inputs.loc[:, "length"],
        coverage_inputs.loc[:, "min_time_per_unit"],
    )

    # Allocate surveyors to survey units based on method
    # def _assign_surveyors(team, coverage):
    if survey.team.assignment == "naive":
        people = cycle(survey.team.df.loc[:, "surveyor_name"])
        coverage_inputs["surveyor_name"] = [
            next(people) for i in range(coverage_inputs.shape[0])
        ]
    elif survey.team.assignment == "speed":
        # minimize total team time
        # TODO: figure out how to optimize assignment
        # Can calculate:
        # - total search time,
        # - individual surveyor's fraction of the total team time
        pass
    elif survey.team.assignment == "random":
        pass

    # Map surveyors to inputs df based on survey units
    coverage_team = coverage_inputs.merge(
        survey.team.df, how="left", on="surveyor_name"
    )

    # Extract surveyor speed penalty values
    coverage_team.loc[:, "speed_penalty_obs"] = _extract_values(
        coverage_team, "speed_penalty"
    )

    # self.coverage_team = coverage_team

    # Find features that intersect coverage
    assem_cov_team = gpd.sjoin(assemblage_inputs, coverage_team, how="left")
    assert (
        assem_cov_team.shape[0] == assemblage_inputs.shape[0]
    ), "Problem with spatial join. Check for accidental spatial overlap in Coverage."

    # record which survey unit it intersects (or NaN)
    # if intersects, set proximity to 1.0
    # else set proximity to 0.0
    assem_cov_team.loc[:, "proximity_obs"] = np.where(
        ~assem_cov_team.loc[:, "surveyunit_name"].isna(), 1.0, 0.0
    )

    # Extract surveyor skill values
    assem_cov_team.loc[:, "skill_obs"] = _extract_values(assem_cov_team, "skill")

    # Calculate final probability of discovery
    assem_cov_team.loc[:, "discovery_prob"] = (
        assem_cov_team.loc[:, "obs_rate"]
        * assem_cov_team.loc[:, "vis_obs"]
        * assem_cov_team.loc[:, "proximity_obs"]
        * assem_cov_team.loc[:, "skill_obs"]
    )

    assem_cov_team.loc[:, "run"] = run_id

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
        assem_cov_team.groupby(["surveyunit_name", "surveyor_name", "base_search_time"])
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

    surveyor_pen = base_pen * time_per_surveyunit.loc[:, "speed_penalty_obs"]

    # multiply above base
    time_per_surveyunit.loc[:, "total_time_per_surveyunit"] = base_pen + surveyor_pen

    time_per_surveyunit.loc[:, "run"] = run_id

    time_surveyunit = time_per_surveyunit.loc[
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

    total_time = time_surveyunit.loc[:, "total_time_per_surveyunit"].sum()

    # per surveyor
    time_per_surveyor = (
        time_surveyunit.groupby("surveyor_name")
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

    time_surveyor = time_per_surveyor.loc[
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

    return ResolvedRun(
        raw=assem_cov_team,
        discovery=discovery_df,
        time_surveyunit=time_surveyunit,
        time_surveyor=time_surveyor,
        total_time=total_time,
    )
