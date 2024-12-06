"""
Module that provides a function for creating graph labels
"""

from aranea.g2d.utils.get_graph_boundaries import Boundaries
from aranea.models.style_config_model import Shape
from aranea.models.xml_model import (MxCellShape, MxCellStyle,
                                     MxCellStyleAlign,
                                     MxCellStyleVerticalAlign, MxGeometryShape)

DEFAULT_BOTTOM_MARGIN = 40
DEFAULT_DIMENSION = 40


def get_graph_label(label: str, graph_boundaries: Boundaries) -> MxCellShape:
    """
    Function for creating a graph label mx cell.

    :param graph_boundaries: Boundaries of the graph
    :type graph_boundaries: Boundaries
    :return: Graph label mx cell
    :rtype: MxCellShape
    """
    return MxCellShape(
        attr_value=label,
        geometry=MxGeometryShape(
            attr_x=(graph_boundaries[0][0] + graph_boundaries[1][0]) / 2 - DEFAULT_DIMENSION / 2,
            attr_y=graph_boundaries[1][1] + DEFAULT_BOTTOM_MARGIN,
            attr_height=DEFAULT_DIMENSION,
            attr_width=DEFAULT_DIMENSION,
        ),
        attr_style=MxCellStyle(
            shape=Shape.TEXT,
            align=MxCellStyleAlign.CENTER,
            verticalAlign=MxCellStyleVerticalAlign.MIDDLE,
        ).to_semicolon_string(),
    )
