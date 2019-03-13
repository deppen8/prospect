
from .simulation import Base, SimSession
from .surveyunit import SurveyUnit
from .area import Area
from .utils import clip_lines_polys

from sqlalchemy import Column, Integer, String, Float, PickleType, ForeignKey
from sqlalchemy.orm import relationship

from typing import List, Dict, Union

import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
from scipy.stats._distn_infrastructure import rv_frozen
import numpy as np
import pandas as pd


class Coverage(Base):
    __tablename__ = 'coverages'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    survey_name = Column('survey_name', String(50), ForeignKey('surveys.name'))
    area_name = Column('area_name', String(50), ForeignKey('areas.name'))
    surveyunit_list = Column('surveyunit_list', PickleType)
    # survey_unit_type = Column('survey_unit_type', String(50))
    orientation = Column('orientation', Float)
    spacing = Column('spacing', Float)
    sweep_width = Column('sweep_width', Float, default=None)
    radius = Column('radius', Float, default=None)

    # relationships
    survey = relationship("Survey", back_populates='coverage')
    area = relationship("Area", back_populates='coverage')
    surveyunit = relationship('SurveyUnit', back_populates='coverage')

    def __init__(self, name: str, survey_name: str, area_name: str, surveyunit_list: List[SurveyUnit], orientation: float, spacing: float, sweep_width: float = None, radius: float = None):
        self.name = name
        self.survey_name = survey_name
        self.area_name = area_name
        self.surveyunit_list = surveyunit_list
        self.orientation = orientation
        self.spacing = spacing
        self.sweep_width = sweep_width
        self.radius = radius

        self.df = gpd.GeoDataFrame(
            [surveyunit.to_dict() for surveyunit in self.surveyunit_list], geometry='shape')

        # TODO: this needs to be calculated when the simulation is run to allow for a distribution to be used for min_time_per_unit

        # extra_cols: List
        # if all(self.df['surveyunit_type'] == 'transect'):
        #     self.df['search_time_base'] = self.min_time_per_unit * self.df['length']
        # elif all(self.df['surveyunit_type'] == 'radial'):
        #     self.df['search_time_base'] = self.min_time_per_unit

    @classmethod
    def from_shapefile(cls, name: str, sim: SimSession, survey_name: str, area_name: str, path: str, surveyunit_type: str, spacing: float, orient_axis: str = 'long', min_time_per_unit: Union[float, rv_frozen] = 0.0) -> 'Coverage':

        tmp_gdf = gpd.read_file(path)

        tmp_area = sim.session.query(Area).filter_by(name=area_name).first()

        min_rot_rect = tmp_area.df.geometry[0].minimum_rotated_rectangle
        orientation = cls.optimize_orientation_by_area_orient(
            min_rect=min_rot_rect, axis=orient_axis)

        tmp_gdf = tmp_gdf.reset_index()
        surveyunit_list: List = []
        for row in tmp_gdf.itertuples():
            surveyunit_list.append(SurveyUnit(name=f'{name}_{row.Index}', coverage_name=name, shape=row.geometry,
                                              surveyunit_type=surveyunit_type, min_time_per_unit=min_time_per_unit))

        return cls(name=name, survey_name=survey_name, area_name=area_name, surveyunit_list=surveyunit_list, orientation=orientation, spacing=spacing)

    @classmethod
    def from_GeoDataFrame(cls, name: str, sim: SimSession, survey_name: str, area_name: str, gdf: gpd.GeoDataFrame, surveyunit_type: str, spacing: float, orient_axis: str = 'long', min_time_per_unit: Union[float, rv_frozen] = 0.0) -> 'Coverage':

        tmp_area = sim.session.query(Area).filter_by(name=area_name).first()

        min_rot_rect = tmp_area.df.geometry[0].minimum_rotated_rectangle
        orientation = cls.optimize_orientation_by_area_orient(
            min_rect=min_rot_rect, axis=orient_axis)

        tmp_gdf = gdf.reset_index()
        surveyunit_list: List = []
        for row in tmp_gdf.itertuples():
            surveyunit_list.append(SurveyUnit(name=f'{name}_{row.Index}', coverage_name=name, shape=row.geometry,
                                              surveyunit_type=surveyunit_type, min_time_per_unit=min_time_per_unit))

        return cls(name=name, survey_name=survey_name, area_name=area_name, surveyunit_list=surveyunit_list, orientation=orientation, spacing=spacing)

    @classmethod
    def from_transects(cls, name: str, sim: SimSession, survey_name: str, area_name: str, spacing: float = 10.0, sweep_width: float = 2.0, orientation: float = 0.0, optimize_orient_by: str = None, orient_increment: float = 5, orient_axis: str = None, min_time_per_unit: Union[float, rv_frozen] = 0.0) -> 'Coverage':
        """
        """

        tmp_area = sim.session.query(Area).filter_by(name=area_name).first()
        min_rot_rect = tmp_area.df.geometry[0].minimum_rotated_rectangle
        centroid = min_rot_rect.centroid

        lines_gs = cls.get_unit_bases(
            surveyunit_type='transect', area=tmp_area, centroid=centroid, spacing=spacing)

        if optimize_orient_by == 'area_coverage':  # set orientation to maximize area
            orientation = cls.optimize_orientation_by_area_coverage(
                lines_gs, centroid, area=tmp_area, buffer=sweep_width, increment=orient_increment)
        elif optimize_orient_by == 'area_orient':
            orientation = cls.optimize_orientation_by_area_orient(
                min_rect=min_rot_rect, axis=orient_axis)

        lines_gs = lines_gs.rotate(orientation, origin=centroid)  # rotate
        lines_gdf = gpd.GeoDataFrame(
            {'geometry': lines_gs}, geometry='geometry')

        lines_clipped = clip_lines_polys(
            lines_gdf, tmp_area.df)  # clip lines by area

        transects_buffer = lines_clipped.buffer(
            sweep_width)  # buffer transects
        buffer_gdf = gpd.GeoDataFrame({'orientation': [orientation] * transects_buffer.shape[0], 'length': lines_clipped.length, 'sweep_width': [
                                      sweep_width] * transects_buffer.shape[0], 'geometry': transects_buffer}, geometry='geometry')

        transects = gpd.overlay(buffer_gdf, tmp_area.df, how='intersection')
        transects = transects.loc[:, ['orientation',
                                      'length', 'sweep_width', 'geometry']]

        transects = transects.reset_index()
        surveyunit_list: List = []
        for row in transects.itertuples():
            surveyunit_list.append(SurveyUnit(name=f'{name}_{row.Index}', coverage_name=name, shape=row.geometry,
                                              surveyunit_type='transect', length=row.length, min_time_per_unit=min_time_per_unit))

        return cls(name=name, survey_name=survey_name, area_name=area_name, surveyunit_list=surveyunit_list, orientation=orientation, spacing=spacing, sweep_width=sweep_width, radius=None)

    @classmethod
    def from_radials(cls, name: str, sim: SimSession, survey_name: str, area_name: str, spacing: float = 10.0, radius: float = 1.78, orientation: float = 0.0, optimize_orient_by: str = None, orient_increment: float = 5, orient_axis: str = None, min_time_per_unit: Union[float, rv_frozen] = 0.0) -> 'Coverage':
        """[summary]

        """

        tmp_area = sim.session.query(Area).filter_by(name=area_name).first()

        min_rot_rect = tmp_area.df.geometry[0].minimum_rotated_rectangle
        centroid = min_rot_rect.centroid

        points_gs = cls.get_unit_bases(
            surveyunit_type='radial', area=tmp_area, centroid=centroid, spacing=spacing)

        if optimize_orient_by == 'area_coverage':  # set orientation to maximize area
            orientation = cls.optimize_orientation_by_area_coverage(
                points_gs, centroid, area=tmp_area, buffer=radius, increment=orient_increment)
        elif optimize_orient_by == 'area_orient':
            orientation = cls.optimize_orientation_by_area_orient(
                min_rect=min_rot_rect, axis=orient_axis)

        points_gs = points_gs.rotate(orientation, origin=centroid)  # rotate
        points_gdf = gpd.GeoDataFrame(
            {'geometry': points_gs}, geometry='geometry')

        points_clipped = clip_lines_polys(
            points_gdf, tmp_area.df)  # clip points by area

        points_buffer = points_clipped.buffer(radius)  # buffer points
        buffer_gdf = gpd.GeoDataFrame({'orientation': [orientation] * points_buffer.shape[0], 'radius': [
                                      radius] * points_buffer.shape[0], 'geometry': points_buffer}, geometry='geometry')

        radials = gpd.overlay(buffer_gdf, tmp_area.df, how='intersection')
        radials = radials.loc[:, ['orientation', 'radius', 'geometry']]

        radials = radials.reset_index()
        surveyunit_list: List = []
        for row in radials.itertuples():
            surveyunit_list.append(SurveyUnit(name=f'{name}_{row.Index}', coverage_name=name, shape=row.geometry,
                                              surveyunit_type='radial', radius=radius, min_time_per_unit=min_time_per_unit))

        return cls(name=name, survey_name=survey_name, area_name=area_name, surveyunit_list=surveyunit_list, orientation=orientation, spacing=spacing, sweep_width=None, radius=radius)

    @staticmethod
    def get_unit_bases(surveyunit_type: str, area: Area, centroid: Point, spacing: float = 10.0) -> gpd.GeoSeries:
        """Return Points or LineStrings as GeoSeries
        """

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
        if surveyunit_type == 'transect':
            # calculate single y value per x
            y_max = centroid.y + diag_dist / 2
            y_min = centroid.y - diag_dist / 2
            # make ends of lines
            top_coords = list(zip(xs, np.full_like(xs, fill_value=y_max)))
            bottom_coords = list(zip(xs, np.full_like(xs, fill_value=y_min)))
            # return LineStrings
            gs = gpd.GeoSeries([LineString(coord_pair)
                                for coord_pair in zip(top_coords, bottom_coords)])

        elif surveyunit_type == 'radial':
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
    def optimize_orientation_by_area_orient(min_rect: Polygon, axis: str = None) -> float:
        """Find the angle that best matches the orientation of the `Area` object
        """

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

    # TODO: Move this to the SurveyUnit level?
    def set_min_time_truncnorm_dist(self, mean: float, sd: float, lower: float, upper: float):
        from .utils import make_truncnorm_distribution

        self.min_time_per_unit = make_truncnorm_distribution(
            mean, sd, lower, upper)
        self.df['min_time_per_unit'] = self.min_time_per_unit
