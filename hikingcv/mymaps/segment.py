import xml.etree.cElementTree as ET
from hikingcv.types.coordinates import LatLngPoint
from hikingcv.mymaps.placemark import Point, LineString
from typing import Union, List


class SegmentDocument(object):
    def __init__(
        self,
        name: str,
        start: LatLngPoint,
        end: LatLngPoint,
        coordinates: List[LatLngPoint],
        start_style="#icon-61",
        end_style="#icon-123",
        segment_style="#line-F9A825-5000",
    ):
        self.name = name
        self.start = start
        self.end = end
        self.coordinates = coordinates
        self.start_style = start_style
        self.end_style = end_style
        self.segment_style = segment_style

    def generate_document(self) -> List[ET.Element]:
        return [
            self.generate_placemark(
                "Start of " + self.name,
                self.start,
                style_url=self.start_style,
            ),
            self.generate_placemark(
                "End of " + self.name,
                self.end,
                style_url=self.end_style,
            ),
            self.generate_placemark(
                self.name,
                self.coordinates,
                style_url=self.segment_style,
            ),
        ]

    def generate_placemark(
        self,
        name: str,
        coordinates: Union[LatLngPoint, List[LatLngPoint]],
        style_url=None,
    ) -> ET.Element:
        if isinstance(coordinates, list):
            placemark = LineString(
                name, "<![CDATA[...]]>", coordinates, style_url=style_url
            )
        else:
            placemark = Point(name, "<![CDATA[...]]>", coordinates, style_url=style_url)

        return placemark.generate_document()
