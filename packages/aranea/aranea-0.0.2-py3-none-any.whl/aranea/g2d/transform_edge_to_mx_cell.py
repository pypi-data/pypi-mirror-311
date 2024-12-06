"""
This module provides a model transformation (Graph-Model->XML-Model) for a single edge.
"""

from uuid import uuid4

from aranea.models.json_graph_model import Edge, ProtocolType, TextOrientation
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import (MxCellEdge, MxCellStyle,
                                     MxCellStyleTextDirection, MxGeometryEdge)


def get_source_attachment_point_style_string(
    source_attachment_point_x: float,
    source_attachment_point_y: float,
) -> str:
    """
    Function to generate a source attachment point style string.

    :param source_attachment_point_x: The x coordinate of the source attachment point.
    :type: float
    :param source_attachment_point_y: The y coordinate of the source attachment point.
    :type: float
    :return: The source attachment point style string.
    :rtype: str
    """
    return f"exitX={source_attachment_point_x};exitY={source_attachment_point_y}"


def get_target_attachment_point_style_string(
    target_attachment_point_x: float,
    target_attachment_point_y: float,
) -> str:
    """
    Function to generate a target attachment point style string.

    :param target_attachment_point_x: The x coordinate of the target attachment point.
    :type: float
    :param target_attachment_point_y: The y coordinate of the target attachment point.
    :type: float
    :return: The target attachment point style string.
    :rtype: str
    """
    return f"entryX={target_attachment_point_x};entryY={target_attachment_point_y}"


def get_text_orientation_style_string(text_orientation: TextOrientation) -> str:
    """
    Function to generate a text orientation style string.

    :param text_orientation: The provided text orientation.
    :type: TextOrientation
    :return: The text orientation style string.
    :rtype: str
    """
    match text_orientation:
        case TextOrientation.HORIZONTAL:
            return f"textDirection={MxCellStyleTextDirection.LTR.value}"
        case TextOrientation.VERTICAL:
            return f"textDirection={MxCellStyleTextDirection.VERTICAL_LR.value}"
        case _:
            raise ValueError(f"Invalid text orientation: {text_orientation}")


def transform_edge_to_mx_cell(
    edge: Edge, protocol_type: ProtocolType, style_config: StyleConfig
) -> list[MxCellEdge]:
    """
    Function to transform an edge to a MxCellEdge.

    :param edge: The edge to transform.
    :type: Edge
    :param protocol_type: The protocol type of the edge.
    :type: ProtocolType
    :param style_config: The StyleConfig to use for the transformation.
    :return: The list of MxCellEdges.
    :rtype: list[MxCellEdge]
    """
    mx_cell_style: MxCellStyle = style_config.get_mx_cell_style(protocol_type=protocol_type)

    composed_style_string = (
        mx_cell_style.to_semicolon_string()
        + ";"
        + get_source_attachment_point_style_string(
            edge.sourceAttachmentPointX, edge.sourceAttachmentPointY
        )
        + ";"
        + get_target_attachment_point_style_string(
            edge.targetAttachmentPointX, edge.targetAttachmentPointY
        )
    )

    if text_orientation := edge.textOrientation:
        composed_style_string += ";" + get_text_orientation_style_string(text_orientation)

    mx_geometry: MxGeometryEdge = MxGeometryEdge()

    mx_cell_edge: MxCellEdge = MxCellEdge(
        attr_id=uuid4(),
        attr_style=composed_style_string,
        attr_value=edge.text,
        attr_source=edge.sourceId,
        attr_target=edge.targetId,
        geometry=mx_geometry,
    )

    return [mx_cell_edge]
