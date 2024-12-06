"""
This module provides utility functions for working with the xml model.
"""

from typing import List, Optional
from uuid import UUID, uuid4

from aranea.models.xml_model import MxCell, RootCells


def assign_parent_id(cell: RootCells, parent_id: UUID) -> RootCells:
    """
    Function for setting the parent id on cells accepted by the <root /> element.

    :param cell: The cell where the parent id shall be set.
    :type cell: RootCells
    :param parent_id: The UUID of the respective parent element
    :type parent_id: UUID
    :return:
    """
    cell.attr_parent = parent_id
    return cell


def get_xml_layer(
    cells: List[RootCells],
    *,
    layer_uuid: Optional[UUID] = uuid4(),
    root_uuid: Optional[UUID] = uuid4(),
) -> List[RootCells]:
    """
    Function for generating a default layer structure with a single layer
    :param cells: The cells that shall be painted onto the generated layer.
    :return:
    """
    root_cell = MxCell(attr_id=root_uuid)
    layer_cell = MxCell(
        attr_id=layer_uuid,
        attr_value="Layer 1",
        attr_parent=root_cell.attr_id,
    )

    return [
        root_cell,
        layer_cell,
        *list(map(lambda cell: assign_parent_id(cell, layer_cell.attr_id), cells)),
    ]
