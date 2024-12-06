"""
This module provides utility functions for the graph schema.
"""

import json
import os.path
from typing import Any, cast

from lark import Lark, UnexpectedInput


def get_graph_schema() -> dict[str, Any]:
    """
    Function for loading the graph schema as a dict.

    @return: dict
    """
    path = os.path.join(os.path.dirname(__file__), "graph-schema-v1.0.json")

    with open(path, encoding="utf8") as schema_file:
        return cast(dict[str, Any], json.load(schema_file))


STYLE_STRING_GRAMMAR = """
?start: kvs
?kvs: kv (";" kv)*
?kv: key "=" value
?key: WORD
?value: NUMBER
        | COLOR
        | WORD
        | "[" value ("," value)? "]"
        | "stencil" "(" ENCODING ")"
        | "data" ":" ENCODING

ENCODING: /[^)]+/
NUMBER: /[-]?\\d+(\\.\\d+)?/
COLOR: /#[0-9a-fA-F]{6}/
WORD: /\\w+(-\\w+)?/
"""

style_string_parser = Lark(STYLE_STRING_GRAMMAR, parser="lalr")


def is_valid_style_string(input_string: str) -> bool:
    """
    Function for is a style string is properly formatted.

    :param input_string:
    :type input_string: str
    :return: bool
    """

    try:
        style_string_parser.parse(input_string, "start")
        return True
    except UnexpectedInput:
        return False
