# https://geoffboeing.com/2016/10/r-tree-spatial-index-python/
# https://www.earthdatascience.org/courses/earth-analytics-python/spatial-data-vector-shapefiles/clip-vector-data-in-python-geopandas-shapely/

import geopandas as gpd

def clip_lines_with_polygon(lines, clipper):
    poly = clipper.geometry.unary_union
    spatial_index = lines.sindex
    bbox = poly.bounds
    sidx = list(spatial_index.intersection(bbox))
    shp_sub = lines.iloc[sidx]
    clipped = shp_sub.copy()
    clipped['geometry'] = shp_sub.intersection(poly)
    final_clipped = clipped[clipped.geometry.notnull()]

    return final_clipped

# final_clipped.plot(ax=clipper.plot(), color='yellow')
