import pytest
import prospect
import itertools
from numpy import ndarray
from geopandas import GeoDataFrame
from scipy.stats._distn_infrastructure import rv_frozen


# `Layer` FIXTURES


@pytest.fixture(scope='module')
def a_default_Layer():
    """Create `Layer` with defaults"""
    simple_Area = prospect.Area.from_area_value(
        name='test_area4layer', value=1.0)
    return prospect.Layer(area=simple_Area)


n_vals = [10, 100, 1000, 10000]


@pytest.fixture(params=n_vals, scope='module')
def a_layer_from_pseudorandom_points(request, an_area_from_shapefile):
    return prospect.Layer.from_pseudorandom_points(n=request.param, area=an_area_from_shapefile, name='test_pseudorandom_points_layer')


# poisson_parent_rates = [1, 10, 100]
poisson_parent_rates = [0.001]
# poisson_child_rates = [1, 10]
poisson_child_rates = [1]


@pytest.fixture(params=poisson_parent_rates, scope='module')
def a_layer_from_poisson_points(request, an_area_from_shapefile):
    return prospect.Layer.from_poisson_points(rate=request.param, area=an_area_from_shapefile, name='test_poisson_points_layer')


# gauss_vars = [0, 0.1, 1, 10, 1000]
gauss_vars = [0, 0.001]

thomas_parent_child_gauss = list(itertools.product(
    poisson_parent_rates, poisson_child_rates, gauss_vars))


@pytest.fixture(params=thomas_parent_child_gauss, scope='module')
def a_layer_from_thomas_points(request, an_area_from_shapefile):
    return prospect.Layer.from_thomas_points(parent_rate=request.param[0], child_rate=request.param[1], gauss_var=request.param[2], area=an_area_from_shapefile, name='test_thomas_points_layer')


@pytest.fixture(params=thomas_parent_child_gauss, scope='module')
def a_layer_from_matern_points(request, an_area_from_shapefile):
    return prospect.Layer.from_matern_points(parent_rate=request.param[0], child_rate=request.param[1], radius=request.param[2], area=an_area_from_shapefile, name='test_matern_points_layer')


@pytest.fixture(scope='module')
def a_simple_Area():
    return prospect.Area.from_area_value(
        name='test_area4layer', value=1.0)


# TEST FOR DEFAULT CONSTRUCTION


def test_default_params_returns_Layer(a_default_Layer):
    assert isinstance(a_default_Layer, prospect.Layer)


def test_default_df_is_GeoDataFrame(a_default_Layer):
    assert isinstance(a_default_Layer.df, GeoDataFrame)


def test_default_df_is_length_at_least_1(a_default_Layer):
    assert a_default_Layer.df.shape[0] >= 1


def test_default_default_columns_exist(a_default_Layer):
    for col in ['layer_name', 'fid', 'time_penalty', 'ideal_obs_rate', 'geometry']:
        assert col in a_default_Layer.df.columns


# TESTS FOR `from_shapefile()` METHOD


def test_from_shapefile_path_returns_Layer(a_layer_shapefile_path, an_area_from_shapefile):
    '''Test that `from_shapefile()` factory function returns a `Layer` object'''
    area = an_area_from_shapefile
    layer = prospect.Layer.from_shapefile(
        path=a_layer_shapefile_path, area=area, name='test_layer', feature_type=None)
    assert isinstance(layer, prospect.Layer)


def test_from_shapefile_returns_Layer(a_layer_from_shapefile):
    assert isinstance(a_layer_from_shapefile, prospect.Layer)


def test_from_shapefile_df_is_GeoDataFrame(a_layer_from_shapefile):
    assert isinstance(a_layer_from_shapefile.df, GeoDataFrame)


def test_from_shapefile_df_is_length_at_least_1(a_layer_from_shapefile):
    assert a_layer_from_shapefile.df.shape[0] >= 1


def test_from_shapefile_default_columns_exist(a_layer_from_shapefile):
    for col in ['layer_name', 'fid', 'time_penalty', 'ideal_obs_rate', 'geometry']:
        assert col in a_layer_from_shapefile.df.columns


# TESTS FOR `from_pseudorandom_points()` METHOD


def test_from_pseudorandom_points_returns_Layer(a_layer_from_pseudorandom_points):
    assert isinstance(a_layer_from_pseudorandom_points, prospect.Layer)


def test_from_pseudorandom_points_df_is_GeoDataFrame(a_layer_from_pseudorandom_points):
    assert isinstance(a_layer_from_pseudorandom_points.df, GeoDataFrame)


def test_from_pseudorandom_points_df_is_length_at_least_1(a_layer_from_pseudorandom_points):
    assert a_layer_from_pseudorandom_points.df.shape[0] >= 1


def test_from_pseudorandom_points_default_columns_exist(a_layer_from_pseudorandom_points):
    for col in ['layer_name', 'fid', 'time_penalty', 'ideal_obs_rate', 'geometry']:
        assert col in a_layer_from_pseudorandom_points.df.columns


# TESTS FOR `from_poisson_points()` METHOD


def test_from_poisson_points_returns_Layer(a_layer_from_poisson_points):
    assert isinstance(a_layer_from_poisson_points, prospect.Layer)


def test_from_poisson_points_df_is_GeoDataFrame(a_layer_from_poisson_points):
    assert isinstance(a_layer_from_poisson_points.df, GeoDataFrame)


def test_from_poisson_points_df_is_length_at_least_1(a_layer_from_poisson_points):
    assert a_layer_from_poisson_points.df.shape[0] >= 1


def test_from_poisson_points_default_columns_exist(a_layer_from_poisson_points):
    for col in ['layer_name', 'fid', 'time_penalty', 'ideal_obs_rate', 'geometry']:
        assert col in a_layer_from_poisson_points.df.columns


# TESTS FOR `from_thomas_points()` METHOD


def test_from_thomas_points_returns_Layer(a_layer_from_thomas_points):
    assert isinstance(a_layer_from_thomas_points, prospect.Layer)


def test_from_thomas_points_df_is_GeoDataFrame(a_layer_from_thomas_points):
    assert isinstance(a_layer_from_thomas_points.df, GeoDataFrame)


def test_from_thomas_points_default_columns_exist(a_layer_from_thomas_points):
    for col in ['layer_name', 'fid', 'time_penalty', 'ideal_obs_rate', 'geometry']:
        assert col in a_layer_from_thomas_points.df.columns


# TESTS FOR `from_matern_points()` METHOD


def test_from_matern_points_returns_Layer(a_layer_from_matern_points):
    assert isinstance(a_layer_from_matern_points, prospect.Layer)


def test_from_matern_points_df_is_GeoDataFrame(a_layer_from_matern_points):
    assert isinstance(a_layer_from_matern_points.df, GeoDataFrame)


def test_from_matern_points_default_columns_exist(a_layer_from_matern_points):
    for col in ['layer_name', 'fid', 'time_penalty', 'ideal_obs_rate', 'geometry']:
        assert col in a_layer_from_matern_points.df.columns


# TESTS FOR `poisson_points()` METHOD


def test_poisson_points_returns(an_area_from_shapefile):
    poisson_point_vals = prospect.Layer.poisson_points(
        area=an_area_from_shapefile, rate=10.0)
    assert isinstance(poisson_point_vals, ndarray)
    assert poisson_point_vals.shape[1] == 2


# TESTS FOR `uniform_disk()` METHOD


def test_uniform_disk_returns():
    disk = prospect.Layer.uniform_disk(x=0, y=0, r=10)
    assert isinstance(disk, tuple)
    assert len(disk) == 2
    assert isinstance(disk[0], float)
    assert isinstance(disk[1], float)


# TESTS FOR `set_ideal_obs_rate_beta()` METHOD


def test_set_ideal_obs_rate_beta_creates_rv_frozen(a_layer_from_shapefile):
    layer = a_layer_from_shapefile
    layer.set_ideal_obs_rate_beta(alpha=9, beta=1)
    assert isinstance(layer.ideal_obs_rate, rv_frozen)


# TESTS FOR `set_time_penalty_truncnorm()` METHOD


def test_set_time_penalty_truncnorm_creates_rv_frozen(a_layer_from_shapefile):
    layer = a_layer_from_shapefile
    layer.set_time_penalty_truncnorm(mean=300, sd=600, lower=0, upper=10000)
    assert isinstance(layer.time_penalty, rv_frozen)
