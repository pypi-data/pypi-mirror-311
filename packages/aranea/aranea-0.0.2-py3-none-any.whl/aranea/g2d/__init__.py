"""
Graph to Diagram module (G2D) for converting graph data (JSON) into
an editable diagram (XML with drawio flavor) and vice versa.
"""

from xml.etree.ElementTree import \
    ElementTree  # nosec TODO: xml has to be sanitized

from aranea.models.json_graph_model import GraphCollection


def graph_to_xml(graph: GraphCollection) -> ElementTree:
    """
    Converts a given graph into an XML string with drawio flavor.

    :param graph: A graph represented in a GraphCollection.
    :type graph: GraphCollection
    :return: The converted XML represented in an ElementTree.
    :rtype: ElementTree
    """
    # method calls placeholder
    return ElementTree()


def xml_to_graph(xml: ElementTree) -> GraphCollection:
    """
    Converts an XML ElementTree into a GraphCollection.

    :param xml: A graph represented in a GraphCollection.
    :type xml: ElementTree
    :return: The converted GraphCollection.
    :rtype: GraphCollection
    """
    # method calls placeholder
    return GraphCollection(graphs=[])  # placeholder return value
