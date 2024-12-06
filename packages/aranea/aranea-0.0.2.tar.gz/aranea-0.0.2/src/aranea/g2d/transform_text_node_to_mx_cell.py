""" 
Module for transforming TextNode objects from the JSON graph model into MxCellShape objects
for the drawio XML format. The transformation handles text nodes with their styling.
"""

from uuid import UUID

from aranea.models.json_graph_model import TextNode
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellShape, MxCellStyle, MxGeometryShape

TEXT_NODE_BOUNDING_BOX_HEIGHT = 40
TEXT_NODE_BOUNDING_BOX_WIDTH = 40


def transform_text_node_to_mx_cell(
    uuid: UUID, node: TextNode, style_config: StyleConfig
) -> list[MxCellShape]:
    """
    Transform a TextNode object into an MxCellShape object for the drawio XML format.

    :param uuid: UUID of the text node
    :type uuid: UUID
    :param node: TextNode to be transformed
    :type node: TextNode
    :param style_config: StyleConfig to be used for styling the mxCellShape
    :type style_config: StyleConfig

    :return: List of MxCellShape objects
    :rtype: list[MxCellShape]
    """
    mx_cell_style: MxCellStyle = style_config.get_mx_cell_style(node_type=node.type)

    mx_geometry: MxGeometryShape = MxGeometryShape(
        attr_x=node.x,
        attr_y=node.y,
        attr_height=TEXT_NODE_BOUNDING_BOX_HEIGHT,
        attr_width=TEXT_NODE_BOUNDING_BOX_WIDTH,
    )

    mx_cell_shape: MxCellShape = MxCellShape(
        attr_id=uuid,
        attr_style=mx_cell_style.to_semicolon_string(),
        attr_value=node.innerText,
        geometry=mx_geometry,
    )

    return [mx_cell_shape]
