import sys
from configparser import ConfigParser
from os.path import exists
from pathlib import Path

import typer
from rich import print

from ..app import main

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

app = typer.Typer(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)

app = typer.Typer()

user_home_directory = Path.home()
path_file_config = f"{user_home_directory}/.kultimate.ini"
print(path_file_config)

config_object = ConfigParser()
default_config = ConfigParser()
default_config["WORKING_DIRECTORY"] = {
    "path": f"{user_home_directory}/kultimate",
}


def check_directory(path: str) -> None:
    """Verifica si existe el directorio, si no, sale del programa"""
    working_directory_exists = exists(path)
    if working_directory_exists:
        main(path)
    else:
        print(f"Directory {path} not exists")
        print(f"Change 'path' on {path_file_config}")
        sys.exit(1)


@app.command()
def init(path: str = ""):
    """Verifica que exista el archivo de configuración"""
    file_config_exists = exists(path_file_config)

    if path:
        # Si el usuario introdujo un valor
        check_directory(path)
    elif file_config_exists:
        config_object.read(path_file_config)
        try:
            directory_info = config_object["WORKING_DIRECTORY"]
            working_path = directory_info["path"]
            check_directory(working_path)
        except IndexError:
            print("Error in config file")
            print(f"Please delete {path_file_config} and run kultimate again.")
            print("Or edit it and correct the path.")
    else:
        # DONE: Crear archivo con la configuración por default
        print("file config not exists")
        print(f"creating file {path_file_config}...")
        try:
            with open(path_file_config, "w") as conf:
                default_config.write(conf)
            print("run kultimate again")
        except PermissionError:
            print(f"Error Permission Writing config file '{path_file_config}'")


def run():
    app()
