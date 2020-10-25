import abc
import xml.etree.cElementTree as ET
from typing import Union, List

from hikingcv.types.coordinates import LatLngPoint


class Placemark(metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        description: str,
        coordinates: Union[LatLngPoint, List[LatLngPoint]],
        style_url=None,
    ):
        self.name = name
        self.description = description
        self.coordinates = self._process_coords(coordinates)
        self.type = None
        self.style_url = style_url or ""

    @abc.abstractmethod
    def _process_coords(self, coordinates) -> str:
        pass

    @abc.abstractmethod
    def generate_document(self) -> ET.Element:
        pass


class Point(Placemark):
    def __init__(
        self,
        name: str,
        description: str,
        coordinates: Union[LatLngPoint, List[LatLngPoint]],
        style_url=None,
    ):
        super().__init__(name, description, coordinates, style_url=style_url)
        self.type = "Point"

    def _process_coords(self, coordinates) -> str:
        return "{},{},{}".format(
            coordinates.lng, coordinates.lat, (coordinates.elev or 0.0)
        )

    def generate_document(self) -> ET.Element:
        placemark = ET.Element("Placemark")
        ET.SubElement(placemark, "name").text = self.name
        ET.SubElement(placemark, "description").text = self.description
        ET.SubElement(placemark, "styleUrl").text = self.style_url
        placemarker_shape = ET.SubElement(placemark, self.type)
        ET.SubElement(placemarker_shape, "coordinates").text = self.coordinates

        return placemark


class LineString(Placemark):
    def __init__(
        self,
        name: str,
        description: str,
        coordinates: List[LatLngPoint],
        style_url=None,
    ):
        super().__init__(name, description, coordinates, style_url=style_url)
        self.type = "LineString"

    def _process_coords(self, coordinates) -> str:
        return "\n".join(
            [
                "{},{},{}".format(coord.lng, coord.lat, (coord.elev or 0.0))
                for coord in coordinates
            ]
        )

    def generate_document(self) -> ET.Element:
        placemark = ET.Element("Placemark")
        ET.SubElement(placemark, "name").text = self.name
        ET.SubElement(placemark, "description").text = self.description
        ET.SubElement(placemark, "styleUrl").text = self.style_url
        placemarker_shape = ET.SubElement(placemark, self.type)
        ET.SubElement(placemarker_shape, "coordinates").text = self.coordinates
        ET.SubElement(placemarker_shape, "tessellate").text = "1"

        return placemark
