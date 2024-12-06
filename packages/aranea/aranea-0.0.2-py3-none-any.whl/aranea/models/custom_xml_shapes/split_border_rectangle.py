"""
Module for generating the drawio custom shape: Split Boarder Rectangle
"""

from aranea.models.custom_xml_shapes.custom_xml_shapes_utils import (
    encode_xml_str, is_valid_hex_color)


def get_split_border_rectangle_xml(color_1: str, color_2: str) -> str:
    """
    Function for creating an XML string of a split border rectangle.

    Documentation on how to create custom shapes:
    https://www.drawio.com/doc/faq/shape-complex-create-edit

    :param color_1: First color of the border (upper half)
    :type color_1: str
    :param color_2: Second color of the border (lower half)
    :type color_2: str

    :return: str
    """
    if not is_valid_hex_color(color_1) or not is_valid_hex_color(color_2):
        raise ValueError("Expected a valid hex color argument string")

    return f"""
    <shape name="Split Border Rectangle" h="100" w="160" aspect="variable" strokewidth="inherit">
        <connections>
            <constraint x="0" y="0" perimeter="0" name="NW" />
            <constraint x="0.25" y="0" perimeter="0" name="N1" />
            <constraint x="0.5" y="0" perimeter="0" name="N" />
            <constraint x="0.75" y="0" perimeter="0" name="N2" />
            <constraint x="1" y="0" perimeter="0" name="NE" />
            <constraint x="0" y="0.25" perimeter="0" name="W1" />
            <constraint x="0" y="0.5" perimeter="0" name="W" />
            <constraint x="0" y="0.75" perimeter="0" name="W2" />
            <constraint x="1" y="0.25" perimeter="0" name="E1" />
            <constraint x="1" y="0.5" perimeter="0" name="E" />
            <constraint x="1" y="0.75" perimeter="0" name="E2" />
            <constraint x="0" y="1" perimeter="0" name="SW" />
            <constraint x="0.25" y="1" perimeter="0" name="S1" />
            <constraint x="0.5" y="1" perimeter="0" name="S" />
            <constraint x="0.75" y="1" perimeter="0" name="S2" />
            <constraint x="1" y="1" perimeter="0" name="SE" />
        </connections>
        <background>
            <rect x="0" y="0" w="160" h="100" />
        </background>
        <foreground>
            <fillstroke />
            <strokecolor color="{color_1}" />
            <path>
                <move x="0" y="50" />
                <line x="0" y="0" />
                <line x="160" y="0" />
                <line x="160" y="50" />
            </path>
            <stroke />
            <strokecolor color="{color_2}" />
            <path>
                <move x="0" y="50" />
                <line x="0" y="100" />
                <line x="160" y="100" />
                <line x="160" y="50" />
            </path>
            <stroke />
        </foreground>
    </shape>
    """


def get_split_border_rectangle_shape(color_1: str, color_2: str) -> str:
    """
    Factory function for generating an encoded custom shape stencil.

    :param color_1: str (hex color)
    :param color_2: str (hex color)
    :return: str
    """
    xml_str: str = get_split_border_rectangle_xml(color_1, color_2)
    encoded_xml_str: str = encode_xml_str(xml_str)
    shape: str = "stencil(" + encoded_xml_str + ")"
    return shape
