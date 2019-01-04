"""
Create a survey methodology
"""
# TODO:

from .area import Area
# from typing import List, Dict, Any
import pandas as pd
import geopandas as gpd
import numpy as np

class Coverage:
    """Create a method
    """

    def __init__(self, area: Area, spacing: float):
        pass

    @classmethod
    def make_transects(cls, area: Area, spacing: float, sweep_width: float, angle: float = 0, min_time: float = 1):
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
        lines_gs = lines_gs.rotate(angle, origin = Point(centroid.x, centroid.y))  # rotate
        lines_gdf = gpd.GeoDataFrame({'geometry': lines_gs}, 
                                    geometry='geometry')

        # clip lines by area
        poly = area.data.geometry.unary_union
        spatial_index = lines_gdf.sindex  
        bbox = poly.bounds
        sidx = list(spatial_index.intersection(bbox))
        lines_sub = lines_gdf.iloc[sidx]
        clipped = lines_sub.copy()
        clipped['geometry'] = lines_sub.intersection(poly)
        lines_clipped = clipped[clipped.geometry.notnull()]


        transects_buffer = lines_clipped.buffer(sweep_width)  # buffer transects
        buffer_gdf = gpd.GeoDataFrame({'angle_deg':[angle] * transects_buffer.shape[0],
                                    'length': lines_clipped.length,
                                    'geometry': transects_buffer}, 
                                    geometry='geometry')

        transects = gpd.overlay(buffer_gdf, area.data, how='intersection')
        transects['area'] = transects.area
        transects['min_search_time'] = min_time * transects['length']
        # add su_id column
        transects['su_id'] = [i for i in range(transects.shape[0])]
        transects = transects.loc[:, ['su_id', 'angle_deg', 'length', 'area_name', 'visibility', 'geometry', 'area', 'min_search_time']]  

        return cls(transects)
