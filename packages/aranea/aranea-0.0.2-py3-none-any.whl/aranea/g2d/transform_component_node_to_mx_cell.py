""" 
Module for transforming ComponentNode objects from the JSON graph model into MxCellShape objects
for the drawio XML format. The transformation handles component nodes with their classifications,
technical capabilities, and associated text elements.
"""

from uuid import UUID, uuid4

from aranea.g2d.transform_technical_capabilities_to_mx_cells import \
    transform_technical_capabilities_to_mx_cells
from aranea.g2d.transform_text_node_to_mx_cell import (
    TEXT_NODE_BOUNDING_BOX_HEIGHT, transform_text_node_to_mx_cell)
from aranea.models.json_graph_model import ComponentNode, TextNode
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellShape, MxGeometryShape


def transform_component_node_to_mx_cell(
    uuid: UUID, component_node: ComponentNode, style_config: StyleConfig
) -> list[MxCellShape]:
    """
    Function for transforming a component node to a list of mxCellShapes.
    A list is returned because the technical capabilities of a ComponentNode map
    to icons in the drawio flavor.

    :param uuid: UUID of the component node
    :type uuid: UUID
    :param component_node: ComponentNode to be transformed
    :type component_node: ComponentNode
    :param style_config: StyleConfig to be used for styling the mxCellShape
    :type style_config: StyleConfig
    :return: List of mxCellShapes
    :rtype: list[MxCellShape]
    """

    mx_cell_shapes: list[MxCellShape] = []

    # create component node mxCellShape
    mx_geometry = MxGeometryShape(
        attr_x=component_node.x,
        attr_y=component_node.y,
        attr_width=component_node.width,
        attr_height=component_node.height,
    )

    mx_cell_style = style_config.get_mx_cell_style(
        node_type=component_node.type, node_classifications=list(component_node.classifications)
    )

    mx_cell_shape = MxCellShape(
        attr_id=uuid, attr_style=mx_cell_style.to_semicolon_string(), geometry=mx_geometry
    )

    if component_node.innerText not in (None, ""):
        mx_cell_shape.attr_value = component_node.innerText

    mx_cell_shapes.append(mx_cell_shape)

    # create icons next to the component
    if component_node.amg_only | len(component_node.technical_capabilities) != 0:
        mx_cell_shapes += transform_technical_capabilities_to_mx_cells(component_node)

    # create outer text next to the component
    if component_node.outerText not in (None, ""):
        text_node = TextNode(
            x=component_node.x,
            y=component_node.y - TEXT_NODE_BOUNDING_BOX_HEIGHT,
            innerText=component_node.outerText,
        )
        mx_cell_text_node = transform_text_node_to_mx_cell(uuid4(), text_node, style_config)
        mx_cell_shapes += mx_cell_text_node

    return mx_cell_shapes
