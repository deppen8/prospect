from typing import List

import pandas as pd
from geopandas import GeoDataFrame

from .layer import Layer


class Assemblage:
    """A collection of all `Layer` objects for a survey

    Parameters
    ----------
    name : str
        Unique name for the assemblage
    layer_list : list of Layer
        List of layers that make up the assemblage

    Attributes
    ----------
    name : str
        Name of the assemblage
    df : geopandas GeoDataFrame
        `GeoDataFrame` with a row for each feature in the assemblage
    """

    def __init__(self, name: str, layer_list: List[Layer]):
        """Create an `Assemblage` instance"""

        self.name = name
        self.layer_list = layer_list
        self.df: GeoDataFrame = pd.concat(
            [layer.df for layer in self.layer_list]
        ).reset_index(drop=True)

    def __repr__(self):
        return f"Assemblage(name={repr(self.name)}, layer_list={repr(self.layer_list)})"

    def __str__(self):
        return f"Assemblage object '{self.name}'"
