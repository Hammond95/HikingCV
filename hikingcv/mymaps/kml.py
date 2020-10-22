import xml.etree.cElementTree as ET
from io import BytesIO

class KmlMap(object):

    def __init__(self, map_doc: ET.Element):
        self.map = map_doc
        self.document = ET.Element(
            "kml", attrib={
                "xmlns": "http://www.opengis.net/kml/2.2"
            }
        )
        self.document.append(self.map)
    
    def dump(self):
        ET.dump(self.document)
    
    def to_file(self, path, encoding="utf-8"):
        et = ET.ElementTree(self.document)
        et.write(
            path,
            encoding=encoding,
            xml_declaration=True,
        )