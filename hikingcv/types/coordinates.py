from typing import Union
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
        # maximum bounds for Google Maps
        # see: https://stackoverflow.com/questions/11849636/maximum-lat-and-long-bounds-for-the-world-google-maps-api-latlngbounds
        assert (lat >= -85.0 and lat <= 85.0)
        assert (lng >= -180 and lng <= 180.0)
    
    def set_elevation(self, elev: float):
        self.elev = elev
    
    def set_timestamp(self, ts: str):
        self.ts = parse(ts)
    
    

