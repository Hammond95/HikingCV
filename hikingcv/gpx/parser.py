import xml
import xml.etree.ElementTree as ET

from hikingcv.types.coordinates import LatLngPoint
from dateutil.parser import parse


def read_file(filename):
    # Add check on path
    # Add check on filetype
    return ET.parse(filename)

def check_tag(el: ET.Element, name: str):
    topografix = "{http://www.topografix.com/GPX/1/1}"
    return el.tag == (topografix + name)

def parse(filename, trk_name=None):
    tree = read_file(filename)
    root = tree.getroot()

    trk = None
    for child in root:
        if check_tag(child, "trk"):
            trk = child
            break
    
    if not trk:
        raise ValueError("No tag <trk> found in gpx file!")
    
    track_name = trk_name
    segment = None
    for child in trk:
        if (not track_name) and (check_tag(child, "name")):
            track_name = str(child.tag.text)
        
        if check_tag(child, "trkseg"):
            segment = child
            break
    
    if not segment:
        raise ValueError("No tag <trkseg> found in gpx file!")
    
    coordinates = []

    trk_start_point = LatLngPoint(segment[0].attrib['lat'], segment[0].attrib['lon'])
    for child in segment[0]:
        if check_tag(child, "time"):
            trk_start_point.set_timestamp(child.text)
        if check_tag(child, "ele"):
            trk_start_point.set_elevation(child.text)
    coordinates.append(trk_start_point)

    for child in segment[1:-1]:
        coordinates.append(
            LatLngPoint(child.attrib['lat'], child.attrib['lon'])
        )

    trk_end_point = LatLngPoint(segment[-1].attrib['lat'], segment[-1].attrib['lon'])
    for child in segment[-1]:
        if check_tag(child, "time"):
            trk_end_point.set_timestamp(child.text)
        if check_tag(child, "ele"):
            trk_end_point.set_elevation(child.text)
    coordinates.append(trk_end_point)

    

    

