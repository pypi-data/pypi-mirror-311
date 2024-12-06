"""This module contains functions to parse and write TOML files."""

from pathlib import Path
from typing import Any

import tomli
import tomli_w


def __parse_toml(toml_path: Path | str) -> dict[str, Any]:
    with open(toml_path, "rb") as f:
        toml: dict[str, Any] = tomli.load(f)
    return toml


def __write_toml(toml_path: Path, toml: dict[str, Any]) -> None:
    with open(toml_path, "wb") as f:
        tomli_w.dump(toml, f)


def aranea_config_available(toml_path: Path) -> bool:
    """Checks if a aranea section is available in the config file.

    :param toml_path: Path to the TOML file
    :type toml_path: str
    :return: True if aranea section is available
    :rtype: bool
    """
    with open(toml_path, "rb") as f:
        toml: dict[str, Any] = tomli.load(f)
    return "tool" in toml and "aranea" in toml["tool"]


def get_aranea_config(toml_path: Path) -> Any:
    """Gets the aranea config.

    :param toml_path: Path to the TOML file
    :type toml_path: str
    :return: The configuration dict.
    :rtype: dict
    """
    with open(toml_path, "rb") as f:
        toml: dict[str, Any] = tomli.load(f)
    return toml["tool"]["aranea"]
