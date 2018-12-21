from np.random import random
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd

# LAYER 1
n = 3
xrange = (0, 1)
yrange = (0, 1)

xs = (random(n) * (xrange[1] - xrange[0])) + xrange[0]
ys = (random(n) * (yrange[1] - yrange[0])) + yrange[0]
gds = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])

ceramics = gpd.GeoDataFrame({'layer_name': ['ceramics'] * n,
                             'fid': [f'ceramics_{i}' for i in range(n)],
                             'time_penalty': [0.1] * n,
                             'ideal_obs_rate': [0.95] * n,
                             'geometry': gds},
                            geometry='geometry')


# LAYER 2
n = 2
xrange = (0, 1)
yrange = (0, 1)

xs = (random(n) * (xrange[1] - xrange[0])) + xrange[0]
ys = (random(n) * (yrange[1] - yrange[0])) + yrange[0]
gds = gpd.GeoSeries([Point(xy) for xy in zip(xs, ys)])

lithics = gpd.GeoDataFrame({'layer_name': ['lithics'] * n,
                           'fid': [f'lithics_{i}' for i in range(n)],
                           'time_penalty': [0.15] * n,
                           'ideal_obs_rate': [0.80] * n,
                           'geometry': gds},
                           geometry='geometry'
                          )

# COMBINE LAYERS
assemblage = pd.concat([ceramics, lithics], ignore_index=True)
