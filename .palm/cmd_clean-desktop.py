from distutils.command.config import config
import enum
import click
import yaml
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
    file_directory_config = Path(__file__).parent / 'file_directory_config.yaml'
    unmatched_files = []

    with file_directory_config.open() as fp:
        configuration = yaml.safe_load(fp)

    # get Path to destinations
    for i, (key, val) in enumerate(configuration.items()):
        destination_path = Path(src_path / key)
        configuration[key]['destination_path'] = destination_path

        # create the directories if they don't exist
        destination_path.mkdir(parents=True, exist_ok=True)

        # grabs all files
        for each_file in Path(src_path).glob('*.*'):
            if not each_file.name.startswith('.'):
                if each_file.suffix in configuration[key]['allowed_values']:
                    # moves to parent folder.
                    each_file.rename(destination_path.joinpath(each_file.name))
                else:
                    if each_file.suffix not in unmatched_files:
                        unmatched_files.append(each_file.suffix)

    if len(unmatched_files) > 0:
        click.secho(f"{len(unmatched_files)} suffixes did not have a designation:", fg="yellow")
        for file in unmatched_files:
            click.secho(f"{file}", fg="red")