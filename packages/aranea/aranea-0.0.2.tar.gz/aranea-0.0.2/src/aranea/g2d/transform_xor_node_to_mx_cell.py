""" 
Module for transforming XorNode objects from the JSON graph model into MxCellShape objects
for the drawio XML format. The transformation handles xor nodes with their styling.
"""

from uuid import UUID

from aranea.models.json_graph_model import XorNode
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellShape, MxCellStyle, MxGeometryShape


def transform_xor_node_to_mx_cell(
    uuid: UUID, node: XorNode, style_config: StyleConfig
) -> list[MxCellShape]:
    """
    Transform a XorNode object into an MxCellShape object for the drawio XML format.
    """
    mx_cell_style: MxCellStyle = style_config.get_mx_cell_style(node_type=node.type)

    mx_geometry: MxGeometryShape = MxGeometryShape(
        attr_x=node.x,
        attr_y=node.y,
        attr_height=node.height,
        attr_width=node.width,
    )

    mx_cell_shape: MxCellShape = MxCellShape(
        attr_id=uuid,
        attr_style=mx_cell_style.to_semicolon_string(),
        attr_value=node.innerText,
        geometry=mx_geometry,
    )

    return [mx_cell_shape]
