"""
This module provides a model transformation (Graph-Model->XML-Model) for
icons associated with technical capabilities of a ComponentNode.
"""

from typing import Literal, Self, Tuple

from aranea.models.custom_xml_shapes.icons import IconFactory
from aranea.models.json_graph_model import ComponentNode, TechnicalCapability
from aranea.models.xml_model import (MxCellShape, MxCellStyle,
                                     MxCellStyleDefaultShape, MxGeometryShape)

DEFAULT_ICON_DIMENSION = 20


def get_technical_capability_icon_str(
    technical_capability: TechnicalCapability | Literal["AMG_ONLY"],
) -> str:
    """
    Function for mapping a technical capability
    to the respective icon.

    :param technical_capability: The technical capability
    :type technical_capability: TechnicalCapability
    :return: The respective icon string.
    :rtype: str
    """
    icon_factory: IconFactory = IconFactory()

    match technical_capability:
        case "AMG_ONLY":
            return str(icon_factory.get_amg_icon_image_str())
        case TechnicalCapability.NETWORK_SWITCH:
            return str(icon_factory.get_network_switch_icon_image_str())
        case TechnicalCapability.BACKEND:
            return str(icon_factory.get_backend_icon_image_str())
        case TechnicalCapability.CELLULAR:
            return str(icon_factory.get_cellular_icon_image_str())
        case TechnicalCapability.WIFI:
            return str(icon_factory.get_wifi_icon_image_str())
        case TechnicalCapability.BLUETOOTH:
            return str(icon_factory.get_bluetooth_icon_image_str())
        case TechnicalCapability.USB:
            return str(icon_factory.get_usb_icon_image_str())
        case TechnicalCapability.SATELLITE:
            return str(icon_factory.get_satellite_icon_image_str())
        case TechnicalCapability.CAR_CHARGER:
            return str(icon_factory.get_car_charger_icon_image_str())
        case TechnicalCapability.DIGITAL_BROADCAST:
            return str(icon_factory.get_digital_broadcast_icon_image_str())
        case TechnicalCapability.ANALOG_BROADCAST:
            return str(icon_factory.get_analog_broadcast_icon_image_str())
        case TechnicalCapability.NFC:
            return str(icon_factory.get_nfc_icon_image_str())
        case _:
            raise ValueError(f"Unknown technical capability: {technical_capability}")


class IconPositioner:
    """
    Class for generating icon positions below a ComponentNode.
    """

    def __init__(
        self,
        component_node: ComponentNode,
        step_x: float = DEFAULT_ICON_DIMENSION,
        step_y: float = DEFAULT_ICON_DIMENSION,
    ):
        self.x = component_node.x
        self.y = component_node.y
        self.width = component_node.width
        self.height = component_node.height
        self.step_x = step_x
        self.step_y = step_y
        self.current_x = self.x
        self.current_y = self.y + self.height
        self.is_initial_position = True

    def reset(self) -> Self:
        """
        Function for resetting the position generation.
        """
        self.current_x = self.x
        self.current_y = self.y + self.height
        self.is_initial_position = True

        return self

    def get_next_position(self) -> Tuple[float, float]:
        """
        Function for getting the next icon position.
        Wraps around when icons exceed width of node.

        :return: A tuple of x and y coordinates.
        :rtype: Tuple[float, float]
        """
        if self.is_initial_position:
            self.is_initial_position = False
            return self.current_x, self.current_y

        self.current_x += self.step_x

        if self.current_x + self.step_x > self.width + self.x:
            self.current_x = self.x
            self.current_y += self.step_y

        return self.current_x, self.current_y


def transform_technical_capabilities_to_mx_cells(
    component_node: ComponentNode,
) -> list[MxCellShape]:
    """
    Function for generating MxCells for a ComponentNode's
    technical capabilities.

    :param component_node: The component node.
    :type component_node: ComponentNode
    :return: The MxCells of the technical capability icons.
    :rtype: list[MxCellShape]
    """
    mx_cells: list[MxCellShape] = []
    icon_positioner: IconPositioner = IconPositioner(component_node)

    technical_capabilities: set[TechnicalCapability | Literal["AMG_ONLY"]] = (
        component_node.technical_capabilities
    )

    if component_node.amg_only:
        technical_capabilities |= {"AMG_ONLY"}

    for technical_capability in component_node.technical_capabilities:
        icon_position = icon_positioner.get_next_position()

        mx_cells.append(
            MxCellShape(
                attr_style=MxCellStyle(
                    shape=MxCellStyleDefaultShape.IMAGE,
                    image=get_technical_capability_icon_str(technical_capability),
                ).to_semicolon_string(),
                geometry=MxGeometryShape(
                    attr_x=icon_position[0],
                    attr_y=icon_position[1],
                    attr_height=DEFAULT_ICON_DIMENSION,
                    attr_width=DEFAULT_ICON_DIMENSION,
                ),
            )
        )

    return mx_cells
