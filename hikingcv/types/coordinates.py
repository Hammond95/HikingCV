from typing import Union, List
from dateutil.parser import parse

class LatLngPoint(object):

    def __init__(self, lat: Union[float, str], lng: Union[float, str]):
        self.lat = float(lat)
        self.lng = float(lng)
        self.elev = 0.0
        self.ts = None
        LatLngPoint.validate(lat, lng)

    @classmethod
    def validate(self, lat: float, lng: float):
        f_lat = float(lat)
        f_lng = float(lng)
        # maximum bounds for Google Maps
        # see: https://stackoverflow.com/questions/11849636/maximum-lat-and-long-bounds-for-the-world-google-maps-api-latlngbounds
        assert (f_lat >= -85.0 and f_lat <= 85.0)
        assert (f_lng >= -180 and f_lng <= 180.0)
    
    def set_elevation(self, elev: float):
        self.elev = elev
    
    def set_timestamp(self, ts: str):
        self.ts = parse(ts)
    
    

