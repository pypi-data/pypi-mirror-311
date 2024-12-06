"""
This module provides a model transformation (Graph-Model->XML-Model) for a single network
"""

from aranea.g2d.transform_edge_to_mx_cell import transform_edge_to_mx_cell
from aranea.models.json_graph_model import Network
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxCellEdge


def transform_network_to_mx_cells(network: Network, style_config: StyleConfig) -> list[MxCellEdge]:
    """
    Transforms a single network to the corresponding
    `MxCellEdge`s.

    :param network: The network to transform.
    :type: Network
    :param style_config: The StyleConfig to use.
    :type: StyleConfig
    :return: The list of MxCellEdges.
    :rtype: list[MxCellEdge]
    """
    mx_cells: list[MxCellEdge] = []

    for edge in network.edges:
        mx_cells.extend(transform_edge_to_mx_cell(edge, network.protocolType, style_config))

    return mx_cells
