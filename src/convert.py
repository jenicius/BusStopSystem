import pyproj
import pyproj.transformer
import math


class Converter:
    def __init__(self, source_crs = pyproj.CRS("EPSG:4326"), target_crs = pyproj.CRS("EPSG:3405")):
        self.transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)
    
    def convert(self, lng, lat):
        x, y = self.transformer.transform(lng, lat)
        return x, y

    def cartesian_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)






