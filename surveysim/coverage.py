"""
Create a survey methodology
"""
# DONE: function to optimize orientation of transects
# DONE: refactor make_* functions with helper functions 
# DONE: implement a make_radial classmethod
# TODO: implement a from_shapefile classmethod
# TODO: use minimum_rotated_angle from shapely (see Jupyter Notebook)

from .area import Area
from .utils import clip_lines_polys
from typing import List, Dict
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString

class Coverage:
    """Define a survey method
    """

    def __init__(self, area: Area, name: str, su_gdf: gpd.GeoDataFrame, su_type: str, spacing: float = 10, orientation: float = 0, min_time_per_unit: float = 1):
        
        self.area_name = area.name
        self.name = name
        self.survey_units = su_gdf.geometry
        self.n_survey_units = su_gdf.geometry.shape[0]
        self.survey_unit_type = su_type
        self.orientation = orientation
        self.min_time_per_unit = min_time_per_unit
        self.spacing = spacing
        self.sweep_width = None
        self.radius = None

        extra_cols: List
        if self.survey_unit_type == 'transect':
            self.sweep_width = su_gdf['sweep_width'].iloc[0]
            su_gdf['min_search_time'] = self.min_time_per_unit * su_gdf['length']
            extra_cols = ['length', 'sweep_width']
        elif self.survey_unit_type in ['quadrat', 'radial']:
            su_gdf['min_search_time'] = self.min_time_per_unit
            if self.survey_unit_type == 'radial':
                self.radius = su_gdf['radius'].iloc[0]
                extra_cols = ['radius']  # TODO: implement a make_radial class method

        su_gdf['area'] = su_gdf.area  # calculate area of the survey unit
        su_gdf['su_id'] = [i for i in range(su_gdf.shape[0])]  # add unique su_id

        cols = ['su_id', 'area', 'min_search_time'] + extra_cols + ['geometry']
        su_gdf = su_gdf.loc[:, cols]  # set column order

        self.data = su_gdf


    @classmethod
    def make_transects(cls, area: Area, name: str, spacing: float = 10, sweep_width: float = 2, orientation: float = 0, optimize_orient: bool = False, orient_increment: float = 5, min_time_per_unit: float = 1):

        centroid = area.data.boundary.centroid.iloc[0]

        lines_gs = get_unit_bases(survey_unit_type='transect', area=area, spacing=spacing)

        if optimize_orient:  # set orientation to maximize area
            orientation = optimize_orientation(lines_gs, Point(centroid.x, centroid.y), area=area, buffer=sweep_width, increment=orient_increment)
        
        lines_gs = lines_gs.rotate(orientation, origin = Point(centroid.x, centroid.y))  # rotate
        lines_gdf = gpd.GeoDataFrame({'geometry': lines_gs}, 
                                    geometry='geometry')

        lines_clipped = clip_lines_polys(lines_gdf, area.data)  # clip lines by area

        transects_buffer = lines_clipped.buffer(sweep_width)  # buffer transects
        buffer_gdf = gpd.GeoDataFrame({'orientation':[orientation] * transects_buffer.shape[0],
                                    'length': lines_clipped.length,
                                    'sweep_width': [sweep_width] * transects_buffer.shape[0],
                                    'geometry': transects_buffer}, 
                                    geometry='geometry')            

        transects = gpd.overlay(buffer_gdf, area.data, how='intersection')
        transects = transects.loc[:, ['orientation', 'length', 'sweep_width', 'geometry']]

        return cls(area=area, name=name, su_gdf=transects, su_type='transect', spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)


    @classmethod
    def make_radials(cls, area: Area, name: str, spacing: float = 10, radius: float = 2, orientation: float = 0, optimize_orient: bool = False, orient_increment: float = 5, min_time_per_unit: float = 1):
        """[summary]
        
        """
        
        centroid = area.data.boundary.centroid.iloc[0]

        points_gs = get_unit_bases(survey_unit_type='radial', area=area, spacing=spacing)
        points_gs.plot()
        if optimize_orient:  # set orientation to maximize area
            orientation = optimize_orientation(points_gs, Point(centroid.x, centroid.y), area=area, buffer=radius, increment=orient_increment)

        points_gs = points_gs.rotate(orientation, origin = Point(centroid.x, centroid.y))  # rotate
        points_gdf = gpd.GeoDataFrame({'geometry': points_gs}, 
                                      geometry='geometry')
        
        points_clipped = clip_lines_polys(points_gdf, area.data)  # clip points by area

        points_buffer = points_clipped.buffer(radius)  # buffer points
        buffer_gdf = gpd.GeoDataFrame({'orientation':[orientation] * points_buffer.shape[0],
                                    'radius': [radius] * points_buffer.shape[0],
                                    'geometry': points_buffer}, 
                                    geometry='geometry')

        radials = gpd.overlay(buffer_gdf, area.data, how='intersection')
        radials = radials.loc[:, ['orientation', 'radius', 'geometry']]

        return cls(area=area, name=name, su_gdf=radials, su_type='radial', spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)


def get_unit_bases(survey_unit_type: str, area: Area, spacing: float = 10) -> gpd.GeoSeries:
    '''Return Points or LineStrings as GeoSeries'''
    from math import sqrt
    # find longest dimension (longest diagonal of bounding box)
    bounds = area.data.bounds
    width = bounds.maxx.max() - bounds.minx.min()
    height = bounds.maxy.max() - bounds.miny.max()
    diag_dist = sqrt(width**2 + height**2)

    n_transects = int(diag_dist // spacing)

    centroid = area.data.boundary.centroid.iloc[0]

    # calculate x values
    xs = coord_vals_from_centroid_val(centroid.x, n_transects, spacing)
    
    # calculate y values
    if survey_unit_type == 'transect':
        # calculate single y value per x
        y_max = centroid.y + diag_dist / 2
        y_min = centroid.y - diag_dist / 2
        # make ends of lines
        top_coords = list(zip(xs, np.full_like(xs, fill_value=y_max)))
        bottom_coords = list(zip(xs, np.full_like(xs, fill_value=y_min)))
        # return LineStrings
        gs = gpd.GeoSeries([LineString(coord_pair) for coord_pair in zip(top_coords, bottom_coords)])
    
    elif survey_unit_type == 'radial':
        ys = coord_vals_from_centroid_val(centroid.y, n_transects, spacing)
        coord_pairs = np.array(np.meshgrid(xs, ys)).T.reshape(-1, 2)
        # return Points
        gs = gpd.GeoSeries([Point(xy) for xy in coord_pairs])
    
    return gs

def coord_vals_from_centroid_val(centroid_val, n_transects, spacing):
    if n_transects % 2 == 0:  # even num units
        lower_start = centroid_val - spacing/2
        upper_start = centroid_val + spacing/2
        lower_vals = lower_start - (np.arange(0, n_transects/2) * spacing)
        upper_vals = upper_start + (np.arange(0, n_transects/2) * spacing)
        vals = np.sort(np.concatenate([lower_vals, upper_vals]))
    else:  # odd num units
        start_val = centroid_val
        lower_vals = start_val - (np.arange(1, n_transects/2) * spacing)
        upper_vals = start_val + (np.arange(1, n_transects/2) * spacing)
        vals = np.sort(np.insert(np.concatenate([lower_vals, upper_vals]), 1, start_val))
    return vals


# TODO: optimize by dominant orientation
def optimize_orientation(survey_units: gpd.GeoSeries, rotation_pt: Point, area: Area, buffer: float = 0, increment: float = 5) -> float:
    """Find the orientation value that allows maximum area
    
    Parameters
    ----------
    survey_units : gpd.GeoSeries
        GeoSeries of the survey units
    rotation_pt : shapely.Point
        Origin of the rotation
    area : `Area`
        `Area` object in which to place survey units
    buffer : float
        Buffer around the transect or point
    increment : float, optional
        Number of degrees added per iteration. Default is 5, which means looping through orientation values [0, 5, 10, 15, ..., 170, 175].
    
    Returns
    -------
    float
        Value for orientation that maximizes area of the `Coverage`
    """

    deg_val: Dict[int, float] = {}
    for deg in range(0, 180, increment):
        survey_units_gs = survey_units.rotate(deg, origin = rotation_pt)  # rotate
        survey_units_gdf = gpd.GeoDataFrame({'geometry': survey_units_gs}, 
                                    geometry='geometry')

        # clip survey_units by area
        survey_units_clipped = clip_lines_polys(survey_units_gdf, area.data)
        survey_units_buffer = survey_units_clipped.buffer(buffer)  # buffer survey_units
        deg_val[deg] = survey_units_buffer.area.sum()

    return max(deg_val, key=lambda k: deg_val[k])
