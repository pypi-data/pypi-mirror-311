"""
Module that provides functions for getting boundaries of graphs.
"""

from typing import Tuple

from aranea.models.xml_model import MxCellShape

Boundaries = Tuple[Tuple[float, float], Tuple[float, float]]


def get_graph_boundaries(mx_cells: list[MxCellShape]) -> Boundaries:
    """
    Function to get boundaries of graphs.
    Only uses MxCellShapes, not Edges.

    :param mx_cells: The cells contained in the graph.
    :type mx_cells: list[MxCellShape]
    :return: The boundaries of graphs.
    :rtype: Boundaries
    """
    if not mx_cells:
        return (0, 0), (0, 0)

    min_x = min(cell.geometry.attr_x for cell in mx_cells)
    max_x = max(cell.geometry.attr_x + cell.geometry.attr_width for cell in mx_cells)
    min_y = min(cell.geometry.attr_y for cell in mx_cells)
    max_y = max(cell.geometry.attr_y + cell.geometry.attr_height for cell in mx_cells)

    return (min_x, min_y), (max_x, max_y)
