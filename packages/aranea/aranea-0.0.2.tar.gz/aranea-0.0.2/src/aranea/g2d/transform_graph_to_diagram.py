"""
This module provides a model transformation (Graph-Model->XML-Model) for graphs.
"""

from aranea.g2d.transform_networks_to_mx_cells import \
    transform_networks_to_mx_cells
from aranea.g2d.transform_nodes_to_mx_cells import transform_nodes_to_mx_cells
from aranea.g2d.utils.get_graph_boundaries import (Boundaries,
                                                   get_graph_boundaries)
from aranea.g2d.utils.get_graph_label import get_graph_label
from aranea.models.json_graph_model import Graph
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import (Diagram, MxCell, MxCellEdge, MxCellShape,
                                     MxGraphModel, Root)
from aranea.models.xml_model_utils import get_xml_layer


def transform_graph_to_diagram(graph: Graph, style_config: StyleConfig) -> Diagram:
    """
    Function to transform graphs to Diagrams.

    :param graph: The graph to transform.
    :type graph: Graph
    :param style_config: The StyleConfig to use for the transformation.
    :type style_config: StyleConfig
    :return: The corresponding Diagram.
    :rtype: Diagram
    """
    networks_mx_cells: list[MxCellEdge] = transform_networks_to_mx_cells(
        graph.networks, style_config
    )
    nodes_mx_cells: list[MxCellShape] = transform_nodes_to_mx_cells(graph.nodes, style_config)

    graph_boundaries: Boundaries = get_graph_boundaries(nodes_mx_cells)
    label_mx_cell: MxCellShape = get_graph_label(graph.label, graph_boundaries)

    layer_wrapped_cells: list[MxCell] = get_xml_layer(
        networks_mx_cells + nodes_mx_cells + [label_mx_cell]
    )

    root_element: Root = Root(
        cells=layer_wrapped_cells,
    )

    mx_graph_model: MxGraphModel = MxGraphModel(
        root=root_element,
    )

    diagram: Diagram = Diagram(
        attr_name=graph.label,
        graph_model=mx_graph_model,
    )

    return diagram
