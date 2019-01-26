"""
Create a survey methodology
"""
# DONE: function to optimize orientation of transects
# DONE: refactor make_* functions with helper functions
# DONE: implement a make_radial classmethod
# DONE: use minimum_rotated_angle from shapely (see Jupyter Notebook)
# DONE: handle problem where n_transects < 2
# DONE: implement a from_shapefile classmethod
# DONE: implement a from_GeoDataFrame classmethod
# TODO: implement a make_quadrats classmethod
# TODO: documentation

from .area import Area
from .utils import clip_lines_polys
from typing import List, Dict
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon


class Coverage:
    """Define a survey method
    """

    def __init__(self, area: Area, name: str, su_gdf: gpd.GeoDataFrame, su_type: str, spacing: float = None, orientation: float = None, min_time_per_unit: float = 1.0):

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
            # TODO: move this calculation to run during the simulation
            su_gdf['min_search_time'] = self.min_time_per_unit * \
                su_gdf['length']
            extra_cols = ['length', 'sweep_width']
        elif self.survey_unit_type in ['quadrat', 'radial']:
            su_gdf['min_search_time'] = self.min_time_per_unit
            if self.survey_unit_type == 'radial':
                self.radius = su_gdf['radius'].iloc[0]
                extra_cols = ['radius']

        su_gdf['area'] = su_gdf.area  # calculate area of the survey unit
        su_gdf['su_id'] = [i for i in range(
            su_gdf.shape[0])]  # add unique su_id

        cols = ['su_id', 'area', 'min_search_time'] + extra_cols + ['geometry']
        su_gdf = su_gdf.loc[:, cols]  # set column order

        self.df = su_gdf

    @classmethod
    def from_shapefile(cls, area: Area, name: str, path: str, su_type: str, spacing: float, orient_axis: str = 'long', min_time_per_unit: float = 1.0):

        temp_gdf = gpd.read_file(path)

        min_rot_rect = area.df.geometry[0].minimum_rotated_rectangle
        orientation = cls.optimize_orientation_by_area_orient(
            min_rect=min_rot_rect, axis=orient_axis)

        return cls(area=area, name=name, su_gdf=temp_gdf, su_type=su_type, spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)

    @classmethod
    def from_GeoDataFrame(cls, area: Area, name: str, gdf: gpd.GeoDataFrame, su_type: str, spacing: float, orient_axis: str = 'long', min_time_per_unit: float = 1.0):
        min_rot_rect = area.df.geometry[0].minimum_rotated_rectangle
        orientation = cls.optimize_orientation_by_area_orient(
            min_rect=min_rot_rect, axis=orient_axis)

        return cls(area=area, name=name, su_gdf=gdf, su_type=su_type, spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)

    @classmethod
    def make_transects(cls, area: Area, name: str, spacing: float = 10, sweep_width: float = 2, orientation: float = 0, optimize_orient_by: str = '', orient_increment: float = 5, orient_axis: str = '', min_time_per_unit: float = 1.0):

        min_rot_rect = area.df.geometry[0].minimum_rotated_rectangle
        centroid = min_rot_rect.centroid

        lines_gs = cls.get_unit_bases(
            survey_unit_type='transect', area=area, centroid=centroid, spacing=spacing)

        if optimize_orient_by == 'area_coverage':  # set orientation to maximize area
            orientation = cls.optimize_orientation_by_area_coverage(
                lines_gs, centroid, area=area, buffer=sweep_width, increment=orient_increment)
        elif optimize_orient_by == 'area_orient':
            orientation = cls.optimize_orientation_by_area_orient(
                min_rect=min_rot_rect, axis=orient_axis)

        lines_gs = lines_gs.rotate(orientation, origin=centroid)  # rotate
        lines_gdf = gpd.GeoDataFrame(
            {'geometry': lines_gs}, geometry='geometry')

        lines_clipped = clip_lines_polys(
            lines_gdf, area.df)  # clip lines by area

        transects_buffer = lines_clipped.buffer(
            sweep_width)  # buffer transects
        buffer_gdf = gpd.GeoDataFrame({'orientation': [orientation] * transects_buffer.shape[0], 'length': lines_clipped.length, 'sweep_width': [
                                      sweep_width] * transects_buffer.shape[0], 'geometry': transects_buffer}, geometry='geometry')

        transects = gpd.overlay(buffer_gdf, area.df, how='intersection')
        transects = transects.loc[:, ['orientation',
                                      'length', 'sweep_width', 'geometry']]

        return cls(area=area, name=name, su_gdf=transects, su_type='transect', spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)

    @classmethod
    def make_radials(cls, area: Area, name: str, spacing: float = 10, radius: float = 2, orientation: float = 0, optimize_orient_by: str = '', orient_increment: float = 5, orient_axis: str = '', min_time_per_unit: float = 1.0):
        """[summary]

        """

        min_rot_rect = area.df.geometry[0].minimum_rotated_rectangle
        centroid = min_rot_rect.centroid

        points_gs = cls.get_unit_bases(
            survey_unit_type='radial', area=area, centroid=centroid, spacing=spacing)

        if optimize_orient_by == 'area_coverage':  # set orientation to maximize area
            orientation = cls.optimize_orientation_by_area_coverage(
                points_gs, centroid, area=area, buffer=radius, increment=orient_increment)
        elif optimize_orient_by == 'area_orient':
            orientation = cls.optimize_orientation_by_area_orient(
                min_rect=min_rot_rect, axis=orient_axis)

        points_gs = points_gs.rotate(orientation, origin=centroid)  # rotate
        points_gdf = gpd.GeoDataFrame(
            {'geometry': points_gs}, geometry='geometry')

        points_clipped = clip_lines_polys(
            points_gdf, area.df)  # clip points by area

        points_buffer = points_clipped.buffer(radius)  # buffer points
        buffer_gdf = gpd.GeoDataFrame({'orientation': [orientation] * points_buffer.shape[0], 'radius': [
                                      radius] * points_buffer.shape[0], 'geometry': points_buffer}, geometry='geometry')

        radials = gpd.overlay(buffer_gdf, area.df, how='intersection')
        radials = radials.loc[:, ['orientation', 'radius', 'geometry']]

        return cls(area=area, name=name, su_gdf=radials, su_type='radial', spacing=spacing, orientation=orientation, min_time_per_unit=min_time_per_unit)

    @staticmethod
    def get_unit_bases(survey_unit_type: str, area: Area, centroid: Point, spacing: float = 10) -> gpd.GeoSeries:
        '''Return Points or LineStrings as GeoSeries'''
        from math import sqrt
        # find longest dimension (longest diagonal of bounding box)
        # use diagonal distance for transect length
        # use centroid of minimum_rotated_rectangle

        bounds = area.df.bounds
        width = bounds.maxx.max() - bounds.minx.min()
        height = bounds.maxy.max() - bounds.miny.max()
        diag_dist = sqrt(width**2 + height**2)

        n_transects = int(diag_dist // spacing)
        if n_transects < 2:
            n_transects = 3

        # calculate x values
        xs = Coverage.coord_vals_from_centroid_val(
            centroid.x, n_transects, spacing)

        # calculate y values
        if survey_unit_type == 'transect':
            # calculate single y value per x
            y_max = centroid.y + diag_dist / 2
            y_min = centroid.y - diag_dist / 2
            # make ends of lines
            top_coords = list(zip(xs, np.full_like(xs, fill_value=y_max)))
            bottom_coords = list(zip(xs, np.full_like(xs, fill_value=y_min)))
            # return LineStrings
            gs = gpd.GeoSeries([LineString(coord_pair)
                                for coord_pair in zip(top_coords, bottom_coords)])

        elif survey_unit_type == 'radial':
            ys = Coverage.coord_vals_from_centroid_val(
                centroid.y, n_transects, spacing)
            coord_pairs = np.array(np.meshgrid(xs, ys)).T.reshape(-1, 2)
            # return Points
            gs = gpd.GeoSeries([Point(xy) for xy in coord_pairs])

        return gs

    @staticmethod
    def coord_vals_from_centroid_val(centroid_val, n_transects, spacing):
        if n_transects % 2 == 0:  # even num units
            lower_start = centroid_val - spacing / 2
            upper_start = centroid_val + spacing / 2
            lower_vals = lower_start - \
                (np.arange(0, n_transects / 2) * spacing)
            upper_vals = upper_start + \
                (np.arange(0, n_transects / 2) * spacing)
            vals = np.sort(np.concatenate([lower_vals, upper_vals]))
        else:  # odd num units
            start_val = centroid_val
            lower_vals = start_val - (np.arange(1, n_transects / 2) * spacing)
            upper_vals = start_val + (np.arange(1, n_transects / 2) * spacing)
            vals = np.sort(np.insert(np.concatenate(
                [lower_vals, upper_vals]), 1, start_val))
        return vals

    @staticmethod
    def optimize_orientation_by_area_coverage(survey_units: gpd.GeoSeries, rotation_pt: Point, area: Area, buffer: float = 0, increment: float = 5) -> float:
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
        for deg in np.arange(0, 180, increment):
            survey_units_gs = survey_units.rotate(
                deg, origin=rotation_pt)  # rotate
            survey_units_gdf = gpd.GeoDataFrame(
                {'geometry': survey_units_gs}, geometry='geometry')

            # clip survey_units by area
            survey_units_clipped = clip_lines_polys(
                survey_units_gdf, area.df)
            survey_units_buffer = survey_units_clipped.buffer(
                buffer)  # buffer survey_units
            deg_val[deg] = survey_units_buffer.area.sum()

        return max(deg_val, key=lambda k: deg_val[k])

    @staticmethod
    def optimize_orientation_by_area_orient(min_rect: Polygon, axis: str) -> float:

        import math
        coords = pd.DataFrame(np.array(min_rect.exterior.coords), columns=[
                              'x', 'y'])  # all corners

        pt_ymin = list(coords.loc[coords['y'] == coords['y'].min()].itertuples(
            index=False, name=None))[0]
        pt_xmax = list(coords.loc[coords['x'] == coords['x'].max()].itertuples(
            index=False, name=None))[0]
        pt_xmin = list(coords.loc[coords['x'] == coords['x'].min()].itertuples(
            index=False, name=None))[0]

        opp = pt_xmax[1] - pt_ymin[1]  # sides of the "triangle"
        adj = pt_xmax[0] - pt_ymin[0]

        right_side = math.sqrt((adj)**2 + (opp)**2)
        left_side = math.sqrt(
            (pt_ymin[0] - pt_xmin[0])**2 + (pt_ymin[1] - pt_xmin[1])**2)

        temp_angle = math.degrees(math.atan(opp / adj))  # angle of rotation

        if (axis == 'long' and right_side <= left_side) or (axis == 'short' and right_side > left_side):
            angle = temp_angle
        elif (axis == 'long' and right_side > left_side) or (axis == 'short' and right_side <= left_side):
            angle = -1 * (90 - temp_angle)

        return angle

    def set_min_time_truncnorm_dist(self, mean: float, sd: float, lower: float, upper: float):
        from .utils import make_truncnorm_distribution

        self.min_time_per_unit = make_truncnorm_distribution(
            mean, sd, lower, upper)
        self.df['min_search_time'] = self.min_time_per_unit
