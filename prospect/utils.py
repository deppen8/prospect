import geopandas as gpd
from scipy.stats._distn_infrastructure import rv_frozen
from scipy.stats import beta, truncnorm


def clip_points(points: gpd.GeoDataFrame, by: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Subset a GeoDataFrame of points based on the boundaries of another GeoDataFrame.

    Parameters
    ----------
    points : geopandas GeoDataFrame
        Point features to be clipped
    by : geopandas GeoDataFrame
        Boundaries to use for clipping

    Returns
    -------
    geopandas GeoDataFrame
        A subset of the original `points`

    References
    ----------
    Earth Analytics Python course, https://doi.org/10.5281/zenodo.2209415
    """

    poly = by.geometry.unary_union
    return points[points.geometry.intersects(poly)]


def clip_lines_polys(
    lines_polys: gpd.GeoDataFrame, by: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Subset a GeoDataFrame of lines or polygons based on the boundaries of another GeoDataFrame.

    Parameters
    ----------
    lines_polys : geopandas GeoDataFrame
        Features to be clipped
    by : geopandas GeoDataFrame
        Boundaries to use for clipping

    Returns
    -------
    geopandas GeoDataFrame
        A subset of the original `lines_polys`

    References
    ----------
    Earth Analytics Python course, https://doi.org/10.5281/zenodo.2209415
    """

    # Create a single polygon object for clipping
    poly = by.geometry.unary_union
    spatial_index = lines_polys.sindex

    # Create a box for the initial intersection
    bbox = poly.bounds

    # Get a list of id's for each object that overlaps the bounding box and subset the data to just those objects
    sidx = list(spatial_index.intersection(bbox))
    thing_sub = lines_polys.iloc[sidx]

    # Clip the data - with these data
    clipped = thing_sub.copy()
    clipped["geometry"] = thing_sub.intersection(poly)

    # Return the clipped layer with no null geometry values
    return clipped[clipped.geometry.notnull()]


def make_beta_distribution(a: float, b: float) -> rv_frozen:
    """Create a fixed beta distribution.

    Parameters
    ----------
    a, b : float
        Shape parameters

    Returns
    -------
    rv_frozen
        Fixed beta distribution
    """

    return beta(a=a, b=b)


def make_truncnorm_distribution(
    mean: float, sd: float, lower: float, upper: float
) -> rv_frozen:
    """Create a truncated normal distribution.

    Parameters
    ----------
    mean : float
        Mean of distribution
    sd : float
        Standard deviation of the distribution
    lower : float
        Lower bound
    upper : float
        Upper bound

    Returns
    -------
    rv_frozen
        Fixed truncated normal distribution
    """

    return truncnorm((lower - mean) / sd, (upper - mean) / sd, loc=mean, scale=sd)
