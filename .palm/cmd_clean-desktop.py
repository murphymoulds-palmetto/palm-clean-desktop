from distutils.command.config import config
import enum
import click
from typing import Optional
from pathlib import Path

@click.command('clean-desktop')
@click.pass_obj

def cli(ctx):
    """Clean Desktop
    
    1) Create a images and spreadsheets folder\n
    2) run `palm clean-desktop`\n
    3) all jpg, png, csv, and numbers will be moved to those folders
    """
    click.echo("palm executing clean")

    clean_desktop(ctx)

def clean_desktop(ctx):

    src_path = Path.home() / 'Desktop'

    configuration = {
        'images': {
            'destination_path': '', 
            'allowed_values': ['.jpg', '.png', '.jpeg']
            },
        'spreadsheets': {
            'destination_path': '',
            'allowed_values': ['.csv', '.numbers']
        }
    }

    # get Path to destinations
    for i, (key, val) in enumerate(configuration.items()):
        destination_path = Path(src_path / key)
        configuration[key]['destination_path'] = destination_path

        # create the directories if they don't exist
        destination_path.mkdir(parents=True, exist_ok=True)

        # grabs all files
        for each_file in Path(src_path).glob('*.*'): 
            if each_file.suffix in configuration[key]['allowed_values']:
                # moves to parent folder.
                each_file.rename(destination_path.joinpath(each_file.name))
