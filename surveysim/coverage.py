"""
Create a survey methodology
"""
# TODO: function to optimize orientation of transects
# TODO: implement a make_radial class method

from .area import Area
from .utils import clip_lines_polys
from typing import List
import pandas as pd
import geopandas as gpd
import numpy as np

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
            self.sweep_width = su_gdf.iloc[0, ['sweep_width']]
            su_gdf['min_search_time'] = self.min_time_per_unit * su_gdf['length']
            extra_cols = ['length', 'sweep_width']
        elif self.survey_unit_type in ['quadrat', 'radial']:
            su_gdf['min_search_time'] = self.min_time_per_unit
            if self.survey_unit_type == 'radial':
                self.radius = su_gdf.iloc[0, ['radius']]
                extra_cols = ['radius']  # TODO: implement a make_radial class method

        su_gdf['area'] = su_gdf.area  # calculate area of the survey unit
        su_gdf['su_id'] = [i for i in range(su_gdf.shape[0])]  # add unique su_id

        cols = ['su_id', 'area', 'min_search_time'] + extra_cols + ['geometry']
        su_gdf = su_gdf.loc[:, cols]  # set column order

        self.data = su_gdf


    @classmethod
    def make_transects(cls, area: Area, name: str, spacing: float = 10, sweep_width: float = 10, orientation: float = 0, min_time_per_unit: float = 1):
        from math import sqrt
        from shapely.geometry import LineString, Point
        # find longest dimension (longest diagonal of bounding box)
        bounds = area.data.bounds
        width = bounds.maxx.max() - bounds.minx.min()
        height = bounds.maxy.max() - bounds.miny.max()
        diag_dist = sqrt(width**2 + height**2)        

        # calculate num of lines
        n_transects = int(diag_dist // spacing)

        # start at centroid of bounding box
        centroid = area.data.boundary.centroid.iloc[0]

        # create vertical lines
        # calculate x values
        if n_transects % 2 == 0:  # even num transects
            left_start = centroid.x - spacing/2
            right_start = centroid.x + spacing/2
            left_xs = left_start - (np.arange(0, n_transects/2) * spacing)
            right_xs = right_start + (np.arange(0, n_transects/2) * spacing)
            xs = np.sort(np.concatenate([left_xs, right_xs]))
        else:  # odd num transects
            start_x = centroid.x
            left_xs = start_x - (np.arange(1, n_transects/2) * spacing)
            right_xs = start_x + (np.arange(1, n_transects/2) * spacing)
            xs = np.sort(np.insert(np.concatenate([left_xs, right_xs]), 1, start_x))
        # calculate y values
        y_max = centroid.y + diag_dist / 2
        y_min = centroid.y - diag_dist / 2
        # make ends of lines
        top_coords = list(zip(xs, np.full_like(xs, fill_value=y_max)))
        bottom_coords = list(zip(xs, np.full_like(xs, fill_value=y_min)))

        lines_gs = gpd.GeoSeries([LineString(coord_pair) for coord_pair in zip(top_coords, bottom_coords)])
        lines_gs = lines_gs.rotate(orientation, origin = Point(centroid.x, centroid.y))  # rotate
        lines_gdf = gpd.GeoDataFrame({'geometry': lines_gs}, 
                                    geometry='geometry')

        # clip lines by area
        lines_clipped = clip_lines_polys(lines_gdf, area.data)

        transects_buffer = lines_clipped.buffer(sweep_width)  # buffer transects
        buffer_gdf = gpd.GeoDataFrame({'orientation':[orientation] * transects_buffer.shape[0],
                                    'length': lines_clipped.length,
                                    'sweep_width': [sweep_width] * transects_buffer.shape[0],
                                    'geometry': transects_buffer}, 
                                    geometry='geometry')

        transects = gpd.overlay(buffer_gdf, area.data, how='intersection')
        transects = transects.loc[:, ['orientation', 'length', 'sweep_width', 'geometry']]

        return cls(area=area, name=name, su_gdf=transects, su_type = 'transect', spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)


    def optimize_orientation(self, ):
        pass
