import xml.etree.cElementTree as ET
from typing import Union, List


class FolderDocument(object):

    def __init__(self, name,):
        # TODO: Add a check on valid names
        self.name = name
        self.placemarks = []
    
    def add_placemarks(self, elements: Union[ET.Element, List[ET.Element]]):
        if isinstance(elements, list):
            self.placemarks.extend(elements)
        else:
            self.placemarks.append(elements)
    
    def generate_document(self, ) -> ET.Element:
        document = ET.Element("Folder")
        ET.SubElement(document, "name").text = self.name
        document.extend(self.placemarks)

        return document