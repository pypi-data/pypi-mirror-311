"""
This module provides a model transformation (Graph-Model->XML-Model) for graph collections.
"""

from aranea.g2d.style_configs.get_default_style_config import \
    get_default_style_config
from aranea.g2d.transform_graph_to_diagram import transform_graph_to_diagram
from aranea.models.json_graph_model import GraphCollection
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import Diagram, MxFile


def transform_graph_collection_to_mx_file(
    graph_collection: GraphCollection, style_config: StyleConfig = get_default_style_config()
) -> MxFile:
    """
    Function to transform graph collection to MxFile.

    :param graph_collection: The graph collection to transform.
    :type graph_collection: GraphCollection
    :param style_config: The StyleConfig to use for the transformation.
    :type style_config: StyleConfig
    :return: The corresponding MxFile.
    :rtype: MxFile
    """
    transformed_diagrams: list[Diagram] = []

    for graph in graph_collection.graphs:
        transformed_diagrams.append(transform_graph_to_diagram(graph, style_config))

    return MxFile(diagrams=transformed_diagrams)
