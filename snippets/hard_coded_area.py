from shapely.geometry import box
import geopandas as gpd

xmin = 0
ymin = 0 
xmax = 1
ymax = 1
rect = box(xmin, ymin, xmax, ymax)
area1 = gpd.GeoDataFrame({'area_name': ['area1'],
                          'visibility': [0.90],
                          'geometry': rect}, 
                          geometry='geometry')
