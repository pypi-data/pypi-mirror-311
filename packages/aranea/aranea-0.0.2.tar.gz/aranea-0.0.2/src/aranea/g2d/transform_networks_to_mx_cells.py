"""
This module provides a model transformation (Graph-Model->XML-Model) for multiple networks.
"""

from aranea.g2d.transform_network_to_mx_cells import \
    transform_network_to_mx_cells
from aranea.models.json_graph_model import Network
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellEdge


def transform_networks_to_mx_cells(
    networks: list[Network], style_config: StyleConfig
) -> list[MxCellEdge]:
    """
    Function to transform multiple networks into a list of MxCellEdges.

    :param networks: The list of networks to transform.
    :type networks: list[Network]
    :param style_config: The style configuration to use for the transformation.
    :type style_config: StyleConfig
    :return: The list of MxCellEdges.
    :rtype: list[MxCellEdge]
    """
    mx_cells: list[MxCellEdge] = []

    for network in networks:
        mx_cells.extend(transform_network_to_mx_cells(network, style_config))

    return mx_cells
