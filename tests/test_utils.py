import pytest
from geopandas import GeoDataFrame
from shapely.geometry import LineString, MultiLineString, MultiPolygon

import prospect


@pytest.fixture(scope="module")
def a_clipped_points_gdf(a_points_gdf_for_clip, a_polygon_gdf_for_clip):
    return prospect.utils.clip_points(
        points=a_points_gdf_for_clip, by=a_polygon_gdf_for_clip
    )


def test_clip_points_returns_GeoDataFrame(a_clipped_points_gdf):
    assert isinstance(a_clipped_points_gdf, GeoDataFrame)


def test_clip_points_returns_expected_points(a_clipped_points_gdf):
    intersect_bools = a_clipped_points_gdf["intersects"].array
    assert len(intersect_bools) == 3
    assert all(intersect_bools)


@pytest.fixture(scope="module")
def a_clipped_lines_gdf(a_line_string_gdf_for_clip, a_polygon_gdf_for_clip):
    return prospect.utils.clip_lines_polys(
        lines_polys=a_line_string_gdf_for_clip, by=a_polygon_gdf_for_clip
    )


def test_clip_lines_returns_GeoDataFrame(a_clipped_lines_gdf):
    assert isinstance(a_clipped_lines_gdf, GeoDataFrame)


def test_clip_lines_polys_returns_correct_lines(a_clipped_lines_gdf):
    expected_shapes = [
        MultiLineString([((0, 0), (0.5, 0.5)), ((0.5, 0.5), (1, 1))]),
        LineString([(0, 1), (1, 2)]),
        MultiLineString([((0, 0.5), (0.5, 0.5)), ((1.5, 0.5), (2, 0.5))]),
    ]
    assert all(a_clipped_lines_gdf.geometry == expected_shapes)


@pytest.fixture(scope="module")
def a_clipped_poly_gdf(a_polygon_gdf_for_clip, a_shifted_polygon_gdf_for_clip):
    return prospect.utils.clip_lines_polys(
        lines_polys=a_polygon_gdf_for_clip, by=a_shifted_polygon_gdf_for_clip
    )


def test_clip_polys_returns_GeoDataFrame(a_clipped_poly_gdf):
    assert isinstance(a_clipped_poly_gdf, GeoDataFrame)


def test_clip_lines_polys_returns_correct_polys(a_clipped_poly_gdf):
    expected_shape = MultiPolygon(
        [
            (
                (
                    (0.5, 2),
                    (2, 2),
                    (2, 0.5),
                    (1.5, 1),
                    (1.25, 0.75),
                    (1, 1),
                    (0.5, 0.5),
                    (0.5, 2),
                ),
                [],
            ),
            (((2, 0.5), (2, 0), (1.5, 0), (2, 0.5)), []),
            (((1.5, 0), (1, 0), (1.25, 0.25), (1.5, 0)), []),
            (((1, 0), (0.5, 0), (0.5, 0.5), (1, 0)), []),
        ]
    )

    assert a_clipped_poly_gdf.geometry.iloc[0] == expected_shape
