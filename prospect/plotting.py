
from .area import Area
from .assemblage import Assemblage
from .coverage import Coverage

from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def bb_plot(area: Area, assemblage: Assemblage, coverage: Coverage, title_size:
            int = 20, figsize: Tuple[float, float] = (8.0, 20.0), **kwargs
            ) -> Figure:
    """Make basic plot to explore spatial building blocks.

    Parameters
    ----------
    area : Area
    assemblage : Assemblage
    coverage : Coverage
    title_size : int, optional
        Font size for the  (the default is 20, which [default_description])
    figsize : Tuple[float, float]
        Figure size in inches

    Returns
    -------
    matplotlib.figure.Figure
        Large plot with three subplots of the spatial building blocks
    """

    # function to create basemap of polygon outline
    def _make_outline(gdf, ax):
        return gdf.plot(ax=ax, facecolor='white', edgecolor='black')

    fig, axarr = plt.subplots(3, 1, figsize=figsize, sharex=True, sharey=True)

    # add Area, Assemblage, and Coverage subplots
    area.df.plot(ax=_make_outline(area.df, axarr[0]))
    axarr[0].set_title(f'{area.name} (Area)', fontsize=title_size)

    assemblage.df.plot(ax=_make_outline(
        area.df, axarr[1]), column='layer_name', legend=True,
        legend_kwds={'loc': (1, 0)})
    axarr[1].set_title(f'{assemblage.name} (Assemblage)', fontsize=title_size)

    coverage.df.plot(ax=_make_outline(area.df, axarr[2]))
    axarr[2].set_title(
        f'{coverage.name} (Coverage)', fontsize=title_size)

    for ax in axarr:        # remove axis lines
        ax.set_axis_off()

    plt.close()  # close the plot so that Jupyter won't print it twice

    return fig
