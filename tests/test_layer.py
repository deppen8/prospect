from geopandas import GeoDataFrame

import prospect


def test_returns_Layer(a_layer):
    assert isinstance(a_layer, prospect.Layer)


def test_has_desired_attributes(a_layer):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer, a)


def test_name_attribute_str(a_layer):
    assert isinstance(a_layer.name, str)


def test_input_features_attribute_List_Features(a_layer):
    assert isinstance(a_layer.input_features, list)
    assert all(
        isinstance(feature, prospect.Feature) for feature in a_layer.input_features
    )


def test_df_attribute_gdf(a_layer):
    assert isinstance(a_layer.df, GeoDataFrame)


def test_from_shapefile_returns_Layer(a_area_layer_shapefile_path_pair):
    area = prospect.Area.from_shapefile(
        name="test_area_from_shapefile", path=a_area_layer_shapefile_path_pair[0]
    )
    layer = prospect.Layer.from_shapefile(
        path=a_area_layer_shapefile_path_pair[1],
        name="test_layer_from_shapefile",
        area=area,
    )

    assert isinstance(layer, prospect.Layer)


def test_from_shapefile_has_desired_attributes(a_layer_from_shapefile):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer_from_shapefile, a)


def test_from_shapefile_name_attribute_str(a_layer_from_shapefile):
    assert isinstance(a_layer_from_shapefile.name, str)


def test_from_shapefile_input_features_attribute_List_Features(a_layer_from_shapefile):
    assert isinstance(a_layer_from_shapefile.input_features, list)
    assert all(
        isinstance(feature, prospect.Feature)
        for feature in a_layer_from_shapefile.input_features
    )


def test_from_shapefile_df_attribute_gdf(a_layer_from_shapefile):
    assert isinstance(a_layer_from_shapefile.df, GeoDataFrame)


def test_from_pseudorandom_pts_returns_Layer(an_area_from_shapefile):
    layer = prospect.Layer.from_pseudorandom_points(
        n=25, name="layer_from_pseudorandom_pts", area=an_area_from_shapefile
    )

    assert isinstance(layer, prospect.Layer)


def test_from_pseudorandom_pts_has_desired_attributes(a_layer_from_pseudorandom_points):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer_from_pseudorandom_points, a)


def test_from_pseudorandom_pts_name_attribute_str(a_layer_from_pseudorandom_points):
    assert isinstance(a_layer_from_pseudorandom_points.name, str)


def test_from_pseudorandom_pts_input_features_attribute_List_Features(
    a_layer_from_pseudorandom_points,
):
    assert isinstance(a_layer_from_pseudorandom_points.input_features, list)
    assert all(
        isinstance(feature, prospect.Feature)
        for feature in a_layer_from_pseudorandom_points.input_features
    )


def test_from_pseudorandom_pts_creates_expected_25_points(
    a_layer_from_pseudorandom_points,
):
    assert len(a_layer_from_pseudorandom_points.input_features) == 25
    assert a_layer_from_pseudorandom_points.df.shape[0] == 25


def test_from_pseudorandom_pts_df_attribute_gdf(a_layer_from_pseudorandom_points):
    assert isinstance(a_layer_from_pseudorandom_points.df, GeoDataFrame)


def test_from_poisson_pts_returns_Layer(an_area_from_shapefile):
    layer = prospect.Layer.from_poisson_points(
        rate=0.001, name="layer_from_poisson_pts", area=an_area_from_shapefile
    )

    assert isinstance(layer, prospect.Layer)


def test_from_poisson_pts_has_desired_attributes(a_layer_from_poisson_points):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer_from_poisson_points, a)


def test_from_poisson_pts_name_attribute_str(a_layer_from_poisson_points):
    assert isinstance(a_layer_from_poisson_points.name, str)


def test_from_poisson_pts_input_features_attribute_List_Features(
    a_layer_from_poisson_points,
):
    assert isinstance(a_layer_from_poisson_points.input_features, list)
    assert all(
        isinstance(feature, prospect.Feature)
        for feature in a_layer_from_poisson_points.input_features
    )


def test_from_poisson_pts_df_attribute_gdf(a_layer_from_poisson_points):
    assert isinstance(a_layer_from_poisson_points.df, GeoDataFrame)


def test_from_thomas_pts_returns_Layer(an_area_from_shapefile):
    layer = prospect.Layer.from_thomas_points(
        parent_rate=0.001,
        child_rate=1,
        gauss_var=5,
        name="layer_from_thomas_pts",
        area=an_area_from_shapefile,
    )

    assert isinstance(layer, prospect.Layer)


def test_from_thomas_pts_has_desired_attributes(a_layer_from_thomas_points):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer_from_thomas_points, a)


def test_from_thomas_pts_name_attribute_str(a_layer_from_thomas_points):
    assert isinstance(a_layer_from_thomas_points.name, str)


def test_from_thomas_pts_input_features_attribute_List_Features(
    a_layer_from_thomas_points,
):
    assert isinstance(a_layer_from_thomas_points.input_features, list)
    assert all(
        isinstance(feature, prospect.Feature)
        for feature in a_layer_from_thomas_points.input_features
    )


def test_from_thomas_pts_df_attribute_gdf(a_layer_from_thomas_points):
    assert isinstance(a_layer_from_thomas_points.df, GeoDataFrame)


def test_from_matern_pts_returns_Layer(an_area_from_shapefile):
    layer = prospect.Layer.from_matern_points(
        parent_rate=0.001,
        child_rate=1,
        radius=5,
        name="layer_from_matern_pts",
        area=an_area_from_shapefile,
    )

    assert isinstance(layer, prospect.Layer)


def test_from_matern_pts_has_desired_attributes(a_layer_from_matern_points):
    for a in ["name", "input_features", "df"]:
        assert hasattr(a_layer_from_matern_points, a)


def test_from_matern_pts_name_attribute_str(a_layer_from_matern_points):
    assert isinstance(a_layer_from_matern_points.name, str)


def test_from_matern_pts_input_features_attribute_List_Features(
    a_layer_from_matern_points,
):
    assert isinstance(a_layer_from_matern_points.input_features, list)
    assert all(
        isinstance(feature, prospect.Feature)
        for feature in a_layer_from_matern_points.input_features
    )


def test_from_matern_pts_df_attribute_gdf(a_layer_from_matern_points):
    assert isinstance(a_layer_from_matern_points.df, GeoDataFrame)
