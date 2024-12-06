""" 
Module for transforming nodes from the JSON graph model into MxCell objects
for the drawio XML format.
This module serves as the main entry point for node transformations, delegating to specialized
transform functions based on the node type (Component, Text, Waypoint, XOR). The transformations
handle node-specific attributes and styling according to the provided style configuration.
"""

from typing import Annotated, Dict
from uuid import UUID

from pydantic.types import UuidVersion

from aranea.g2d.transform_component_node_to_mx_cell import \
    transform_component_node_to_mx_cell
from aranea.g2d.transform_text_node_to_mx_cell import \
    transform_text_node_to_mx_cell
from aranea.g2d.transform_waypoint_node_to_mx_cell import \
    transform_waypoint_node_to_mx_cell
from aranea.g2d.transform_xor_node_to_mx_cell import \
    transform_xor_node_to_mx_cell
from aranea.models.json_graph_model import (ComponentNode, NodeUnionType,
                                            TextNode, WaypointNode, XorNode)
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellShape


def transform_nodes_to_mx_cells(
    nodes: Dict[Annotated[UUID, UuidVersion(4)], NodeUnionType], style_config: StyleConfig
) -> list[MxCellShape]:
    """
    Transform a dictionary of nodes into a list of MxCell objects for the drawio XML format.

    :param nodes: Dictionary of nodes to be transformed
    :type nodes: Dict[Annotated[UUID, UuidVersion(4)], NodeUnionType]
    :param style_config: StyleConfig to be used for styling the mxCells
    :type style_config: StyleConfig

    :return: List of MxCell objects
    :rtype: list[MxCell]
    """

    mx_cells: list[MxCellShape] = []

    for uuid, node in nodes.items():
        if isinstance(node, WaypointNode):
            mx_cells += transform_waypoint_node_to_mx_cell(uuid, node, style_config)
        elif isinstance(node, TextNode):
            mx_cells += transform_text_node_to_mx_cell(uuid, node, style_config)
        elif isinstance(node, XorNode):
            mx_cells += transform_xor_node_to_mx_cell(uuid, node, style_config)
        elif isinstance(node, ComponentNode):
            mx_cells += transform_component_node_to_mx_cell(uuid, node, style_config)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    return mx_cells
