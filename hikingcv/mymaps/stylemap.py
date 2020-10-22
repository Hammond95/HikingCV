import xml.etree.cElementTree as ET
from hikingcv.mymaps.style import StyleDocument

from typing import Union, List

class StyleMapDocument(object):

    def __init__(self, style_map_id, normal: StyleDocument, highlight: StyleDocument):
        self.id = style_map_id
        self.normal = normal
        self.highlight = highlight
    
    def generate_document(self) -> List[ET.Element]:
        style_map = ET.Element(
            "StyleMap", 
            attrib={"id": self.id}
        )
        normal_pair = ET.SubElement(style_map, "Pair")
        ET.SubElement(normal_pair, "key").text = "normal"
        ET.SubElement(normal_pair, "styleUrl").text = "#" + self.normal.id

        highlight_pair = ET.SubElement(style_map, "Pair")
        ET.SubElement(highlight_pair, "key").text = "highlight"
        ET.SubElement(highlight_pair, "styleUrl").text = "#" + self.highlight.id

        style_map.extend([normal_pair, highlight_pair])

        return [
            self.normal.generate_document(),
            self.highlight.generate_document(),
            style_map
        ]



