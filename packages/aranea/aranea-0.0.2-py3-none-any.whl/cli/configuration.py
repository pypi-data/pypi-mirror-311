"""Module for the configuration command of the CLI."""

import logging
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

import click

from aranea.p2g.pdf2graph import PDFReader
from cli.toml_tools import (__parse_toml, __write_toml,
                            aranea_config_available, get_aranea_config)

_logger: logging.Logger = logging.getLogger(__name__)

EPILOG: str = "Docs: https://674c8e49-0742-43e3-bf6f-def680a9d585.ul.bw-cloud-instance.org"


def get_annotation_metadata(func: Callable[..., Any], key: str, metadata_index: int = 0) -> str:
    """Get the metadata of an annotation of a function."""
    annotation = func.__annotations__.get(key)
    if annotation is not None and hasattr(annotation, "__metadata__"):
        return str(annotation.__metadata__[metadata_index])
    return ""


class Config:
    """Configuration class containing configuration settings for other commands."""

    default_config: dict[str, Any] = {
        "tool": {
            "aranea": {
                "output_dir": "./",
                "drawio_path": "/path/to/draw.io",
                "log_level": "INFO",
                "p2g": PDFReader.parse_page.__kwdefaults__,
            },
        },
    }

    config: dict[str, Any]
    output_dir: Path
    drawio_path: Path | None
    log_level: str
    ecu_min_height: int
    ecu_max_height: int
    xor_min_height: int

    def __init__(
        self,
        config_file_path: Path,
        output_dir: Path | None = None,
        log_level: str | None = None,
        drawio_path: Path | None = None,
    ):
        if config_file_path.exists() and aranea_config_available(config_file_path):
            _logger.info("Using the config from %s", config_file_path)
            self.config = get_aranea_config(config_file_path)
        else:
            _logger.info("No config found for %s", config_file_path)
            self.config = {}

        # output_dir
        if output_dir is not None:
            self.output_dir = output_dir
        elif "output_dir" in self.config:
            self.output_dir = Path(self.config["output_dir"]).resolve()
        else:
            self.output_dir = Path(self.default_config["tool"]["aranea"]["output_dir"]).resolve()
        if not self.output_dir.exists():
            _logger.error("The output directory %s does not exist!", self.output_dir)
            sys.exit(1)

        # log_level
        if log_level is not None:
            self.log_level = log_level
        elif "log_level" in self.config:
            self.log_level = self.config["log_level"]
        else:
            self.log_level = self.default_config["tool"]["aranea"]["log_level"]

        # drawio_path
        if drawio_path is not None:
            self.drawio_path = drawio_path
        elif "drawio_path" in self.config:
            self.drawio_path = Path(self.config["drawio_path"]).resolve()
        elif shutil.which("drawio") is not None:
            # escaped mypy, all ready checked if path is None
            self.drawio_path = Path(shutil.which("drawio"))  # type: ignore[arg-type]
        else:
            self.drawio_path = None

        # ecu_min_height
        if "p2g" in self.config and "ecu_min_height" in self.config["p2g"]:
            self.ecu_min_height = int(self.config["p2g"]["ecu_min_height"])
        else:
            self.ecu_min_height = self.default_config["tool"]["aranea"]["p2g"]["ecu_min_height"]

        # ecu_max_height
        if "p2g" in self.config and "ecu_max_height" in self.config["p2g"]:
            self.ecu_max_height = int(self.config["p2g"]["ecu_max_height"])
        else:
            self.ecu_max_height = self.default_config["tool"]["aranea"]["p2g"]["ecu_max_height"]

        # xor_min_height
        if "p2g" in self.config and "xor_min_height" in self.config["p2g"]:
            self.xor_min_height = int(self.config["p2g"]["xor_min_height"])
        else:
            self.xor_min_height = self.default_config["tool"]["aranea"]["p2g"]["xor_min_height"]


@click.command(epilog=EPILOG)
@click.argument(
    "new_config_file_path",
    nargs=1,
    required=True,
    type=click.Path(
        dir_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--overwrite/--no-overwrite",
    "overwrite",
    is_flag=True,
    show_default=True,
    default=False,
    required=False,
    type=bool,
    help="If set, the configuration section in the provided file will be overwritten if it already \
exists.",
)
@click.pass_context
def create_config(ctx: click.Context, new_config_file_path: Path, overwrite: bool) -> None:
    """Creates an initial configuration section for aranea in the CONFIG_FILE_PATH with all default
    values.

    Aranea checks for the existence of the CONFIG_FILE_PATH file and creates a new one if it does
    not exist. The config file needs to be a ``.toml`` file.
    """
    config: Config = ctx.obj

    if new_config_file_path.suffix != ".toml":
        _logger.error("The configuration file must be a .toml file!")
        sys.exit(1)

    if new_config_file_path.is_file():
        _logger.info("Found an existing configuration file: %s", new_config_file_path)
        existing_config: dict[str, Any] = __parse_toml(new_config_file_path)

        if "tool" in existing_config and "aranea" in existing_config["tool"]:
            _logger.info("Found an existing aranea configuration section.")

            if not overwrite:
                _logger.warning("Will not overwrite the existing configuration!")
            else:
                existing_config["tool"]["aranea"] = config.default_config["tool"]["aranea"]
                _logger.info("Old aranea configuration was deleted!")
                __write_toml(new_config_file_path, existing_config)
                _logger.info("New default aranea configuration was written!")
        else:
            _logger.info("No existing aranea configuration found.")
            existing_config["tool"]["aranea"] = config.default_config["tool"]["aranea"]
            __write_toml(new_config_file_path, existing_config)
            _logger.info("New default aranea configuration added.")

    else:
        Path(new_config_file_path).touch()
        _logger.info("Created a new configuration file: %s", new_config_file_path)
        __write_toml(new_config_file_path, config.default_config)
