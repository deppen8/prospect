def make_transects(transect_interval, sweep_width, angle_degrees, area_gdf):
    import numpy as np
    import geopandas as gpd
    from shapely.geometry import LineString

    xmin = area_gdf.bounds.minx.min()
    xmax = area_gdf.bounds.maxx.max()
    ymin = area_gdf.bounds.miny.min()
    ymax = area_gdf.bounds.maxy.max()

    h = ymax-ymin

    def standard(temp_angle):
        theta = np.radians(temp_angle)
        horiz_shift = (1/np.cos(theta)) * transect_interval
        top_start = xmin
        
        # calculate bottom starting point
        a = (1/np.tan(theta)) * transect_interval
        b = h - a
        bottom_start_shift = np.tan(theta) * b
        bottom_start = xmin - bottom_start_shift
        
        n_transects = int((xmax - bottom_start) / horiz_shift)
        
        offsets = np.arange(1, n_transects+1) * horiz_shift
        top_vals  = top_start + offsets
        bottom_vals = bottom_start + offsets
        
        return top_vals, bottom_vals, n_transects
    
    def special(horiz_shift, top_start, bottom_start):
        n_transects = int((xmax - bottom_start) / horiz_shift)
    
        offsets = np.arange(1, n_transects+1) * horiz_shift
        top_vals  = top_start + offsets
        bottom_vals = bottom_start + offsets
        
        return top_vals, bottom_vals, n_transects


    if 0 < angle_degrees < 90:
        top_vals, bottom_vals, n_transects = standard(angle_degrees)
        
    elif 90 < angle_degrees < 180:
        supplement = 180 - angle_degrees
        bottom_vals, top_vals, n_transects = standard(supplement)
        
    elif angle_degrees in [0, 180]:
        horiz_shift = transect_interval
        top_start = xmin + sweep_width
        bottom_start = top_start
        top_vals, bottom_vals, n_transects = special(horiz_shift, top_start, bottom_start)
    
    elif angle_degrees == 90:
        horiz_shift = transect_interval
        top_start = ymin + sweep_width
        bottom_start = top_start
        top_vals, bottom_vals, n_transects = special(horiz_shift, top_start, bottom_start)
    
    top_coords = list(zip(top_vals, np.full_like(top_vals, fill_value=ymax)))
    bottom_coords = list(zip(bottom_vals, np.full_like(bottom_vals, fill_value=ymin)))

    lines_gs = gpd.GeoSeries([LineString(coord_pair) for coord_pair in zip(top_coords, bottom_coords)])
    lines_gdf = gpd.GeoDataFrame({'length': np.arange(0, n_transects),
                                  'geometry': lines_gs
                                 }, geometry='geometry')
    
    # clip lines by bounding box
    poly = area1.geometry.unary_union
    spatial_index = lines_gdf.sindex
    bbox = poly.bounds
    sidx = list(spatial_index.intersection(bbox))
    lines_sub = lines_gdf.iloc[sidx]
    clipped = lines_sub.copy()
    clipped['geometry'] = lines_sub.intersection(poly)
    lines_clipped = clipped[clipped.geometry.notnull()]
    
    
    transects_buffer = lines_clipped.buffer(sweep_width)  # buffer transects
    buffer_gdf = gpd.GeoDataFrame({'angle_deg':[angle_degrees] * n_transects,
                                   'length': lines_clipped.length,
                                   'geometry': transects_buffer}, 
                                   geometry='geometry')

    transects = gpd.overlay(buffer_gdf, area_gdf, how='intersection')
    transects['area'] = transects.area
    
    return transects

def compare_transect_angles(transect_interval, sweep_width, area_gdf):
    import pandas as pd
    
    df_list=[]
    for angle in range(0, 180, 5):
        df = make_transects(transect_interval, sweep_width, angle, area_gdf)
        df_list.append(df)
    
    angle_df = pd.concat(df_list)
    angle_df['area']= angle_df.area
    
    return angle_df.groupby('angle_deg')['area'].sum()
