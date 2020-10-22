import xml.etree.cElementTree as ET
from typing import Union, List

class MapDocument(object):

    def __init__(self, name, description="My Hiking Map"):
        self.name = name
        self.description = description
        self.styles = []
        self.folders = []
    
    def add_styles(self, elements: Union[ET.Element, List[ET.Element]]):
        if isinstance(elements, list):
            self.styles = elements
        else:
            self.styles = [elements]
    
    def add_folders(self, elements: Union[ET.Element, List[ET.Element]]):
        if isinstance(elements, list):
            self.folders = elements
        else:
            self.folders = [elements]
    
    def generate_document(self, ) -> ET.Element:
        document = ET.Element("Document")
        ET.SubElement(document, "name").text = self.name
        ET.SubElement(document, "description").text = self.description
        document.extend(self.styles)
        document.extend(self.folders)

        return document