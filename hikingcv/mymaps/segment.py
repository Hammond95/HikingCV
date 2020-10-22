import xml.etree.cElementTree as ET
from hikingcv.types.coordinates import LatLngPoint
from typing import Union

class SegmentDocument(object):

    def __init__(
        self,
        name: str, 
        start:LatLngPoint, 
        end:LatLngPoint, 
        coordinates:list[LatLngPoint],
        start_style="#icon-61",
        end_style="#icon-123",
        segment_style="#line-F9A825-5000"
    ):
        self.name = name
        self.start = start
        self.end = end
        self.coordinates = coordinates
        self.start_style = start_style
        self.end_style = end_style
        self.segment_style = segment_style
    
    def generate_segment_document(self):
        return [
            self.generate_placemark(
                "Inizio di " + name,
                self.start,
                style_url=self.start_style,
            ),
            self.generate_placemark(
                "Fine di " + name,
                self.end,
                style_url=self.end_style,
            ),
            self.generate_placemark(
                name,
                self.coordinates,
                style_url=self.segment_style,
            ),
        ]
    
    def generate_placemark(
        self,
        name: str,
        coordinates: Union[LatLngPoint, list[LatLngPoint]],
        style_url=None
    ) -> ET.Element:
        placemark = ET.Element("Placemark")

        ET.SubElement(placemark, "name").text = name

        if isinstance(coordinates, list):
            placemark_type = "LineString"
            placemark_desc = "<![CDATA[...]]>"
            placemark_style = (style_url or "")
            placemark_coords = "\n".join(
                [
                    "{},{},{}".format(coord.lat, coord.lng, (coord.elev or 0.0))
                    for coord in coordinates
                ]
            )
        else:
            placemark_type = "Point"
            placemark_desc = "<![CDATA[...]]>"
            placemark_style = (style_url or "")
            placemark_coords = "{},{},{}".format(
                coordinates.lat,
                coordinates.lng,
                (coordinates.elev or 0.0)
            )
        
        ET.SubElement(placemark, "description").text = placemark_desc
        ET.SubElement(placemark, "styleUrl").text = placemark_style
        placemarker_shape = ET.SubElement(placemark, placemark_type)
        ET.SubElement(placemarker_shape, "coordinates").text = placemark_coords

        return placemark




