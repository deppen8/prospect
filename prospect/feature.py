from .simulation import Base

from typing import Union, Dict

from sqlalchemy import Column, Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from shapely.geometry import Point, LineString, Polygon
from scipy.stats._distn_infrastructure import rv_frozen


class Feature(Base):
    """Represents an observable thing like an artifact or landscape feature.

    This class is not normally used directly. It is usually more efficient to use the constructor methods of the `Layer` class to create many `Feature` objects at once.

    Parameters
    ----------
    name : str
        Unique name for the feature
    layer_name : str
        Name of the parent layer
    shape : Union[Point, LineString, Polygon]
        Geographic specification
    time_penalty : Union[float, rv_frozen], optional
        Minimum amount of time it takes to record a feature (the default is 0.0, which indicates no time cost for feature recording)
    ideal_obs_rate : Union[float, rv_frozen], optional
        Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

        - It lies inside or intersects the Coverage
        - Surface visibility is 100%
        - The surveyor is highly skilled

        The default is 1.0, which indicates that when visibility and surveyor skill allow, the feature will always be recorded.

    Attributes
    ----------
    name : str
        Unique name for the feature
    layer_name : str
        Name of parent layer
    shape : Union[Point, LineString, Polygon]
        Geographic specification
    time_penalty : Union[float, rv_frozen]
        Minimum amount of time it takes to record a feature
    ideal_obs_rate : Union[float, rv_frozen]
        Ideal observation rate: the frequency with which an artifact or feature will be recorded, assuming the following ideal conditions:

        - It lies inside or intersects the Coverage
        - Surface visibility is 100%
        - The surveyor is highly skilled
    """

    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(50), unique=True)
    # assemblage_name = Column('assemblage_name', String(
    #     50), ForeignKey('assemblages.name'))
    layer_name = Column("layer_name", String(50), ForeignKey("layers.name"))
    shape = Column("shape", PickleType)
    time_penalty = Column("time_penalty", PickleType)
    ideal_obs_rate = Column("ideal_obs_rate", PickleType)

    # relationships
    # assemblage = relationship('Assemblage', back_populates='features')
    layer = relationship("Layer", back_populates="features")

    def __init__(
        self,
        name: str,
        layer_name: str,
        shape: Union[Point, LineString, Polygon],
        time_penalty: Union[float, rv_frozen] = 0.0,
        ideal_obs_rate: Union[float, rv_frozen] = 1.0,
    ):
        """Create a `Feature` instance.
        """

        self.name = name
        self.layer_name = layer_name
        self.shape = shape
        self.time_penalty = time_penalty
        self.ideal_obs_rate = ideal_obs_rate

    def to_dict(self) -> Dict:
        """Create dictionary from attributes to allow easy DataFrame creation by `Layer`.

        Returns
        -------
        dict
            Dictionary containing pairs of class attributes and their values
        """

        return {
            "feature_name": self.name,
            "layer_name": self.layer_name,
            "shape": self.shape,
            "time_penalty": self.time_penalty,
            "ideal_obs_rate": self.ideal_obs_rate,
        }
