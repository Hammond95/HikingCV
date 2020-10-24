import re
import click
import functools
import operator
import pandas as pd
import fnmatch
from os import path, walk
from pathlib import Path

from hikingcv.gpx import parser

from hikingcv.mymaps.folder import FolderDocument
from hikingcv.mymaps.segment import SegmentDocument
from hikingcv.mymaps.map import MapDocument
from hikingcv.mymaps.kml import KmlMap
from hikingcv.mymaps.style import IconStyleDocument, LineStyleDocument
from hikingcv.mymaps.stylemap import StyleMapDocument

from hikingcv.cli.utils import pathleaf, cleanup

def parse_csv_path(csvpath):
    filepath, options_string = csvpath.split("?")
    print(filepath, options_string)

    # TODO: Manage paths escape sequences
    filepath = path.abspath(re.sub(r" ", "\ ", filepath))

    if not path.isfile(filepath):
        raise FileNotFoundError("'{}' is not a valid file!".format(filepath))
    
    options = { 
        op.split("=")[0]:op.split("=")[1] 
        for op in options_string.split("&") 
    }

    return filepath, options


def read_csv(filepath, options):
    df = pd.read_csv(
        filepath,
        sep=(options.get("sep") or ","),
        header=(
            options.get("header") or 0
        ),
    )

    print(df.head())

    out = pd.DataFrame()

    out["label"] = df[options.get("label")].fillna("Unlabeled")
    out["lat"] = df[options.get("lat")]
    out["lng"] = df[options.get("lng")]

    # Filtering just valid lat lng rows
    condition = out["lat"].notnull() & out["lng"].notnull()

    out = out[condition]

    return out


def get_icon_styles():
    start_ico_style_norm = IconStyleDocument(
        "icon-123-normal",
        "https://www.gstatic.com/mapspro/images/stock/61-green-dot.png",
    )
    start_ico_style_high = IconStyleDocument(
        "icon-123-highlight",
        "https://www.gstatic.com/mapspro/images/stock/61-green-dot.png",
        label_scale=1.1
    )
    end_ico_style_norm = IconStyleDocument(
        "icon-61-normal",
        "https://www.gstatic.com/mapspro/images/stock/123-red-dot.png",
    )
    end_ico_style_high = IconStyleDocument(
        "icon-61-highlight",
        "https://www.gstatic.com/mapspro/images/stock/123-red-dot.png",
        label_scale=1.1
    )

    start_ico_map = StyleMapDocument(
        "icon-123",
        start_ico_style_norm,
        start_ico_style_high
    )

    end_ico_map = StyleMapDocument(
        "icon-61",
        end_ico_style_norm,
        end_ico_style_high
    )

    return [ start_ico_map, end_ico_map ]

def get_lines_styles():

    line_style_norm = LineStyleDocument(
        "line-0288D1-5000-normal",
        color="ffd18802",
    )

    line_style_high = LineStyleDocument(
        "line-0288D1-5000-highlight",
        color="ffd18802",
        width=7.5
    )

    line_style_map = StyleMapDocument(
        "line-0288D1-5000",
        line_style_norm,
        line_style_high,
    )

    return [line_style_map]


def process_files(folders_list):
    xml_folders = []

    for folder in folders_list:
        foldername = pathleaf(folder)
        click.echo("Reading files in folder '{}'.".format(folder))
        xml_folder_doc = FolderDocument(cleanup(foldername))
        files = []
        for (dirpath, dirnames, filenames) in walk(path.abspath(folder)):
            files.extend(
                path.join(path.abspath(folder), f)
                for f in
                fnmatch.filter(filenames, "*.gpx")
            )
            break
        
        xml_placemarks = []
        for gpx in files:
            filename = pathleaf(gpx)
            segment_name = cleanup(filename.replace(".gpx", ""))
            trk_start, trk_end, coords = parser.parse(gpx)

            click.echo("    Generating Segment Document for {}.".format(filename))
            segment_document = SegmentDocument(
                segment_name,
                trk_start,
                trk_end,
                coords,
                segment_style="#line-0288D1-5000"
            )

            xml_placemarks.extend(segment_document.generate_document())
        
        click.echo("Adding placemarks to layer '{}'.".format(pathleaf(folder)))
        xml_folder_doc.add_placemarks(xml_placemarks)
        xml_folders.append(xml_folder_doc)

    return xml_folders


def create_kml_map(xml_styles, xml_folders):
    click.echo("Creating a Map Document...")
    xml_map = MapDocument("My Hiking Trails (Automated)")

    xml_map.add_styles(
        functools.reduce(
            operator.iconcat,
            [ s.generate_document() for s in xml_styles ],
            []
        )
    )

    xml_map.add_folders(
        [ x.generate_document() for x in xml_folders ]
    )
    
    return KmlMap(xml_map.generate_document())

