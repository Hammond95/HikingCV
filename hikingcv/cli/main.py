import click
import hikingcv
import sys
from os import path

from hikingcv.cli.commands import *

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
def cli(ctx, version,):
    """Command Line Interface for `GHunt`."""
    # TODO: Add Logo print on console
    if version:
        return _version()
    
    ctx.obj = {
        'DATA_PATH_EXISTS': False
    }

    print(ctx)

