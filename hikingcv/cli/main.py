import click
import hikingcv
import sys
from os import path, walk

from hikingcv.cli.commands import (
    parse_csv_path, 
    read_csv, 
    process_files, 
    create_kml_map, 
    get_icon_styles, 
    get_lines_styles,
)
from hikingcv.cli.messages import MAP__PATH_SYNTAX

here = path.abspath(path.dirname(__file__))


def do_help(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


@click.group()
@click.version_option(
    version=hikingcv.__version__,
    message="%(version)s",
)
@click.pass_context
def cli(ctx):
    pass

@cli.command(
    name="map", 
    help="Generates a kml file with your hiking trails from gpx files, that can be imported in MyMaps."
)
@click.option(
    "--folders", "-f",
    required=True,
    help="A list of folders containing the gpx files, each folder will be a layer in MyMaps. (max 10 folders)"
)
@click.option(
    "--root", "-R",
    required=False,
    is_flag=True,
    help="If this option is provided, just consider first element of folders and uses the specified folder as a root acting recursively."
)
@click.option(
    "--coords-csv", "-C",
    required=False,
    help="A csv path to import coordinates points in a layer. " + MAP__PATH_SYNTAX
)
@click.option(
    "--dump",
    required=False,
    is_flag=True,
    help="Prints Map KML to stdout."
)
@click.option(
    "--output", "-o",
    required=False,
    default=None,
    help="Writes the KML document to the specified path."
)
def map(folders, root, coords_csv, dump, output):
    folders_list = folders.split(" ")

    if root:
        for (dirpath, dirnames, filenames) in walk(path.abspath(folders)):
            folders_list = [ 
                path.join(path.abspath(folders), f) 
                for f in dirnames[1:]
            ]
            break

    for folder in folders_list:
        if not path.isdir(path.abspath(folder)):
            raise ValueError("'{}' is not a valid directory!".format(folder))

    layers = []
    layers.extend(folders_list)

    if coords_csv:
        csv_filepath, options = parse_csv_path(coords_csv)
        layers.append(csv_filepath)
        df = read_csv(csv_filepath, options)
    
    if len(layers) > 10:
        raise ValueError("The maximum number of layers allowed by MyMaps is 10, provided {} paths.".format(len(layers)))

    xml_styles = []
    xml_styles.extend(get_icon_styles())
    xml_styles.extend(get_lines_styles())

    xml_folders = process_files(folders_list)

    kml = create_kml_map(xml_styles, xml_folders)

    if dump and not(output):
        kml.dump()
    
    if output:
        kml.to_file(path.abspath(output))



