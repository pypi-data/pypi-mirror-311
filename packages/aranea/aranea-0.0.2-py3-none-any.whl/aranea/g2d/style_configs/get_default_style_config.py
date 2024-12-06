"""
Module for providing a default style config.
"""

from aranea.models.json_graph_model import (EcuClassification, NodeType,
                                            ProtocolType)
from aranea.models.style_config_model import (Align, FillStyle, Perimeter,
                                              Shape, StyleAttributes,
                                              StyleConfig, VerticalAlign)


def get_default_style_config() -> StyleConfig:
    """
    Function that returns a default style config.
    :return: StyleConfig
    """
    return StyleConfig(
        node_type_style_attributes={
            NodeType.COMPONENT: StyleAttributes(
                shape=Shape.RECTANGLE,
                rounded=True,
                fill_color="#FFFFFF",
                fill_style=FillStyle.SOLID,
                stroke_color="#000000",
                stroke_width=1,
            ),
            NodeType.XOR: StyleAttributes(
                shape=Shape.ELLIPSE,
                fill_color="#CCCCCC",
                fill_style=FillStyle.SOLID,
                stroke_color="#000000",
                stroke_width=1,
            ),
            NodeType.TEXT: StyleAttributes(
                shape=Shape.TEXT,
                resizable=False,
                fill_color="NONE",
                stroke_color="NONE",
                autosize=True,
                align=Align.CENTER,
                vertical_align=VerticalAlign.MIDDLE,
            ),
            NodeType.WAYPOINT: StyleAttributes(
                shape=Shape.WAYPOINT,
                fill_color="NONE",
                fill_style=FillStyle.SOLID,
                resizable=False,
                rotatable=False,
                size=6,
                perimeter=Perimeter.CENTER,
            ),
        },
        node_classification_style_attributes={
            EcuClassification.ECU: StyleAttributes(
                rounded=True,
            ),
            EcuClassification.NEW_ECU: StyleAttributes(
                rounded=True,
                fill_color="#708E3F",
                fill_style=FillStyle.HATCH,
            ),
            EcuClassification.ECU_ONLY_IN_BR: StyleAttributes(
                rounded=True,
                fill_color="#B8504B",
                fill_style=FillStyle.CROSS_HATCH,
            ),
            EcuClassification.DOMAIN_GATEWAY: StyleAttributes(
                shape=Shape.DIAG_ROUND_RECTANGLE,
                fill_color="#AAD6E2",
            ),
            EcuClassification.NON_DOMAIN_GATEWAY: StyleAttributes(
                shape=Shape.DIAG_ROUND_RECTANGLE,
                fill_color="#D4CCDF",
            ),
            EcuClassification.LIN_CONNECTED_ECU: StyleAttributes(
                rounded=True,
                fill_color="#EFD3D1",
            ),
            EcuClassification.ENTRY_POINT: StyleAttributes(
                rounded=True,
                stroke_color="#FDB409",
                stroke_width=4,
            ),
            EcuClassification.CRITICAL_ELEMENT: StyleAttributes(
                rounded=True,
                stroke_color="#FC0008",
                stroke_width=4,
            ),
        },
        network_protocol_type_style_attributes={
            ProtocolType.CAN: StyleAttributes(
                stroke_width=4,
            ),
            ProtocolType.CAN_250: StyleAttributes(
                stroke_color="#1A4654",
                stroke_width=4,
            ),
            ProtocolType.CAN_500: StyleAttributes(
                stroke_color="#28728A",
                stroke_width=4,
            ),
            ProtocolType.CAN_800: StyleAttributes(
                stroke_color="#82C2D3",
                stroke_width=4,
            ),
            ProtocolType.CAN_FD: StyleAttributes(
                stroke_color="#B00005",
                stroke_width=4,
            ),
            ProtocolType.FLEX_RAY: StyleAttributes(
                stroke_color="#FEBDFF",
                stroke_width=4,
            ),
            ProtocolType.ETHERNET: StyleAttributes(
                stroke_color="#C1B4D0",
                stroke_width=4,
            ),
            ProtocolType.MOST_ELECTRIC: StyleAttributes(
                stroke_color="#F18B45",
                stroke_width=4,
            ),
            ProtocolType.LIN: StyleAttributes(
                stroke_color="#81CA3F",
                stroke_width=4,
            ),
        },
    )
