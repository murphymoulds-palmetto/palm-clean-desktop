import enum
from distutils.command.config import config
from pathlib import Path
from typing import Optional

import click
import yaml


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

    with file_directory_config.open() as fp:
        configuration = yaml.safe_load(fp)

    existing_suffixes = []

    for i, (key, val) in enumerate(configuration.items()):
      existing_suffixes.extend(val['allowed_values'])

    # get Path to destinations
    for i, (key, val) in enumerate(configuration.items()):
        destination_path = Path(src_path / key)
        configuration[key]['destination_path'] = destination_path

        # create the directories if they don't exist
        destination_path.mkdir(parents=True, exist_ok=True)

        # grabs all files
        for each_file in Path(src_path).glob('*.*'):
          if not each_file.name.startswith('.'):
            if each_file.suffix not in existing_suffixes:
              handle_unmatched_suffixes(ctx, each_file.suffix, file_directory_config)
            elif each_file.suffix in val['allowed_values']:
              each_file.rename(destination_path.joinpath(each_file.name))

def handle_unmatched_suffixes(ctx, suffix_to_check, file_directory_config):

    with file_directory_config.open() as fp:
        configuration_raw = yaml.safe_load(fp)

    configured_suffixes = []

    template_config = {
        'allowed_values': []
    }

    for key, val in configuration_raw.items():
        configured_suffixes = configured_suffixes + val['allowed_values']

    if suffix_to_check not in configured_suffixes:

        click.secho(f"{suffix_to_check}", fg="red")
        user_wants_update = click.Choice(choices=['yes', 'no'], case_sensitive=False)

        if user_wants_update:

            click.echo("Here is a current list of folders you have configured")
            click.echo(f"{ configuration_raw.keys() }")
            name_of_folder = click.prompt(f"Type name of folder to put {suffix_to_check} in.")

            if name_of_folder not in list(configuration_raw.keys()):
                configuration_raw[name_of_folder] = template_config

            if suffix_to_check not in configuration_raw[name_of_folder]['allowed_values']:
                configuration_raw[name_of_folder]['allowed_values'].append(suffix_to_check)

        with file_directory_config.open('w') as fp:
            yaml.safe_dump(configuration_raw, fp, indent=4, default_flow_style=False)