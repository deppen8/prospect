"""
Create an assemblage of artifacts
"""
# TODO: 
# - accept list (numpy array?) of Layers
# - create dict(?) or df(?) of Layer attributes
# - concat Layer.data objects

from .layer import Layer
from typing import List, Dict, Any
import pandas as pd
import geopandas as gpd

class Assemblage:
    """Collect `Layer` objects
    """
    def __init__(self, name: str, layers: List[Layer]):
        self.name = name

        self.layer_info: Dict[str, Dict[str, Any]] = {}
        for layer in layers:
            self.layer_info[layer.name] = {
                'features': layer.features,
                'n_features': layer.n_features,
                'feature_type': layer.feature_type,
                'time_penalty': layer.time_penalty,
                'ideal_obs_rate': layer.ideal_obs_rate,
            }
        
        self.data: pd.DataFrame = pd.concat([l.data for l in layers]).reset_index(drop=True)
        
