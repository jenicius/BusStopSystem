import json
from paths import Path
from stops import Stop


def point(lng, lat):

    obj = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates":[lng, lat],
        "type": "Point"
      }
    }

    return obj


def linestring_obj(path):
    coordinates = [[lng, lat] for lng, lat in zip(path.get_lng(), path.get_lat())]

    obj = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": coordinates,
        "type": "LineString"
      }
    }

    return obj
    

def geojson(file_path, obj_list):
    features = []
    for obj in obj_list:
        features.append(obj)

    json_data = {
    "type": "FeatureCollection",
    "features": features  
    }
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file)







