from distutils.command.config import config
import enum
import click
import re
from typing import Optional
from pathlib import Path
import shutil
import os

@click.command('clean')
@click.pass_obj

def cli(ctx):
    """clean"""
    click.echo("palm executing clean")
    command = f"echo 'clean running!'"
    clean(ctx)

def clean(ctx):

    src_path = Path.home() / 'Desktop'
    configuration = {
        'images': {
            'destination_path': '', 
            'allowed_values': ['.jpg', '.png']
            },
        'spreadsheets': {
            'destination_path': '',
            'allowed_values': ['.csv', '.numbers']
        }
    }
    

    # get Path to destinations
    for i, (key, val) in enumerate(configuration.items()):
        files_to_move = []
        destination_path = Path(src_path / key)
        configuration[key]['destination_path'] = destination_path


        for each_file in Path(src_path).glob('*.*'): # grabs all files
            if each_file.suffix in configuration[key]['allowed_values']:
                files_to_move.append(each_file)
            # each_file.rename(trg_path.joinpath(each_file.name)) # moves to parent folder.

        click.echo(destination_path)
        click.echo(files_to_move)