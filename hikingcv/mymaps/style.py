import xml.etree.cElementTree as ET


class StyleDocument(object):
    def __init__(self, style_id, style_type):
        self.id = style_id
        self.type = style_type

    def generate_document(self):
        pass


class IconStyleDocument(StyleDocument):
    def __init__(
        self, style_id, icon_href, color="#000000", icon_scale=1.1, label_scale=0
    ):
        StyleDocument.__init__(self, style_id, "Icon")
        self.icon_href = icon_href
        self.color = color.replace("#", "ff")
        self.icon_scale = str(icon_scale)
        self.label_scale = str(label_scale)

    def generate_document(self) -> ET.Element:
        style = ET.Element("Style", attrib={"id": self.id})
        icon_style = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon_style, "color").text = self.color
        ET.SubElement(icon_style, "scale").text = self.icon_scale
        icon = ET.SubElement(icon_style, "Icon")
        ET.SubElement(icon, "href").text = self.icon_href
        # ET.SubElement(
        #    icon_style,
        #    "hotSpot",
        #    attrib={
        #        "x": "16",
        #        "xunits": "pixels",
        #        "y": "32",
        #        "yunits": "insetPixels"
        #    }
        # )
        label_style = ET.SubElement(style, "LabelStyle")
        ET.SubElement(label_style, "scale").text = self.label_scale

        return style


class LineStyleDocument(StyleDocument):
    def __init__(self, style_id, color, width=5):
        StyleDocument.__init__(self, style_id, "Icon")
        self.color = color
        self.width = str(width)

    def generate_document(self) -> ET.Element:
        style = ET.Element("Style", attrib={"id": self.id})
        line_style = ET.SubElement(style, "LineStyle")
        ET.SubElement(line_style, "color").text = self.color
        ET.SubElement(line_style, "width").text = self.width

        return style
