from typing import Dict, Union

from scipy.stats._distn_infrastructure import rv_frozen
from shapely.geometry import Polygon


class SurveyUnit:
    """Represents a spatial unit of survey like a transect or radial unit.

    This class is not normally used directly. It is usually more efficient to use the constructor methods of the `Coverage` class to create many `SurveyUnit` objects at once.

    Parameters
    ----------
    name : str
        Unique name for the survey unit
    coverage_name : str
        Name of the parent coverage
    shape : Polygon
        Geographic specification
    surveyunit_type : {'transect', 'radial'}
        Type of the unit
    length : float, optional
        Length of transect units (the default is None)
    radius : float, optional
        Radius of radial units (the default is None)
    min_time_per_unit : Union[float, rv_frozen], optional
        Minimum amount of time required to complete one "unit" of survey, given no surveyor speed penalty and no time penalty for recording features. The default is 0.0.

        Because transects can differ in length, transect coverages should specify this term as time per one unit of distance (e.g., seconds per meter).

        For radial survey units, this term should be specified more simply as time per one survey unit.

    Attributes
    ----------
    name : str
        Unique name for the survey unit
    coverage_name : str
        Name of the parent coverage
    shape : Polygon
        Geographic specification
    surveyunit_type : {'transect', 'radial'}
        Type of the unit
    surveyunit_area : float
        Area value calculated from the `shape`
    length : float
        Length of transect units
    radius : float
        Radius of radial units
    min_time_per_unit : Union[float, rv_frozen]
        Minimum amount of time required to complete one "unit" of survey, given no surveyor speed penalty and no time penalty for recording features.

        Because transects can differ in length, transect coverages should specify this term as time per one unit of distance (e.g., seconds per meter).

        For radial survey units, this term should be specified more simply as time per one survey unit.
    """

    def __init__(
        self,
        name: str,
        coverage_name: str,
        shape: Polygon,
        surveyunit_type: str,
        length: float = None,
        radius: float = None,
        min_time_per_unit: Union[float, rv_frozen] = 0.0,
    ):
        """[summary]"""

        self.name = name
        self.coverage_name = coverage_name
        self.shape = shape
        self.surveyunit_type = surveyunit_type
        self.surveyunit_area = self.shape.area
        self.length = length
        self.radius = radius
        self.min_time_per_unit = min_time_per_unit

    def to_dict(self) -> Dict:
        """Create dictionary from attributes to allow easy DataFrame creation by `Coverage`.

        Returns
        -------
        dict
            Dictionary containing pairs of class attributes and their values
        """

        return {
            "surveyunit_name": self.name,
            "coverage_name": self.coverage_name,
            "shape": self.shape,
            "surveyunit_type": self.surveyunit_type,
            "surveyunit_area": self.surveyunit_area,
            "length": self.length,
            "radius": self.radius,
            "min_time_per_unit": self.min_time_per_unit,
        }
