"""
Utility functions for creating custom drawio XML shapes.
"""

import base64
import re
import zlib
from urllib.parse import quote

from defusedxml import ElementTree as ET


def is_valid_hex_color(hex_string: str) -> bool:
    """
    Function for validating a hex color string.

    :param hex_string: string to be validated
    :type hex_string: str

    :return: evaluation result
    :rtype: bool
    """
    return bool(re.match("#[0-9a-fA-F]{6}", hex_string))


def deflate(deflated_string: str) -> bytes:
    """
    Function for deflating an input string.

    :param deflated_string: string to be deflated
    :type deflated_string: str

    :return: deflated string
    :rtype: bytes
    """
    compress = zlib.compressobj(
        zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8, strategy=zlib.Z_DEFAULT_STRATEGY
    )

    compressed_data = compress.compress(bytes(deflated_string, "iso-8859-1"))

    compressed_data += compress.flush()

    return compressed_data


def encode_xml_str(xml_str: str) -> str:
    """
    Function for encoding an XML string into a base64 string for drawio.
    Uses url encoding and deflating.

    Reverse engineered from:
    https://github.com/jgraph/drawio-tools/blob/master/tools/convert.html

    :param xml_str: xml string to be encoded
    :type xml_str: str

    :return: base64 encoded xml string
    :rtype: str
    """
    url_encoded = quote(xml_str, safe="~()*!.'")
    deflated = deflate(url_encoded)
    base_64 = base64.b64encode(deflated).decode("utf-8")

    return base_64


def is_valid_svg_namespace(svg_string: str) -> bool:
    """
    Function for checking if a string is a valid SVG string.

    :param svg_string: string to be checked
    :type svg_string: str

    :return: evaluation result
    :rtype: bool
    """
    try:
        root = ET.fromstring(svg_string)
        return bool(root.tag == "{http://www.w3.org/2000/svg}svg")
    except ET.ParseError:
        return False


def get_mx_cell_image_str(svg_str: str) -> str:
    """
    Function for getting the image string for a MxCell style.

    Encodes the SVG string into a base64 string and adds the necessary prefix.
    Reverse engineered by importing an SVG file into drawio and decoding the style string using
    https://jgraph.github.io/drawio-tools/tools/convert.html

    :param svg_str: svg string to be encoded
    :type svg_str: str

    :return: image string for MxCell style
    :rtype: str
    """

    # check that the string represents an SVG
    if not is_valid_svg_namespace(svg_str):
        raise ValueError("The given string is not an SVG string")

    # separate each element by a single whitespace for better testing of the results
    svg_str = " ".join(svg_str.split())

    base_64 = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml,{base_64}"
