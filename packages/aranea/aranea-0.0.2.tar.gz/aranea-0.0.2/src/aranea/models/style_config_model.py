"""
This module provides a pydantic model for working with style configurations.
"""

from enum import Enum
from typing import Dict, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.color import Color

from aranea.models.custom_xml_shapes.split_border_rectangle import \
    get_split_border_rectangle_shape
from aranea.models.json_graph_model import (EcuClassification, NodeType,
                                            ProtocolType)
from aranea.models.style_config_model_utils import merge_models
from aranea.models.xml_model import (MxCellStyle, MxCellStyleAlign,
                                     MxCellStyleDefaultShape,
                                     MxCellStyleFillStyle,
                                     MxCellStylePerimeter, MxCellStyleShape,
                                     MxCellStyleTextDirection,
                                     MxCellStyleVerticalAlign)


class FillStyle(Enum):
    """
    Enum for defining the fill style.
    """

    SOLID = "SOLID"
    HATCH = "HATCH"
    CROSS_HATCH = "CROSS_HATCH"


class Shape(Enum):
    """
    Enum for defining the shape.
    """

    RECTANGLE = "RECTANGLE"
    ELLIPSE = "ELLIPSE"
    TEXT = "TEXT"
    WAYPOINT = "WAYPOINT"
    DIAG_ROUND_RECTANGLE = "DIAG_ROUND_RECTANGLE"


class TextDirection(Enum):
    """
    Enum for defining the text direction.
    """

    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"


class Align(Enum):
    """
    Enum for defining the text alignment.
    """

    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class VerticalAlign(Enum):
    """
    Enum for defining the vertical text alignment.
    """

    MIDDLE = "MIDDLE"
    TOP = "TOP"
    BOTTOM = "BOTTOM"


class Perimeter(Enum):
    """
    Enum for defining the perimeter.
    """

    CENTER = "CENTER"


ColorDescriptor = Color | Literal["NONE"] | None


class StyleAttributes(BaseModel):
    """
    Model for defining style attributes.
    """

    model_config = ConfigDict(extra="forbid")

    shape: Shape | None = Field(
        default=None,
    )
    rounded: bool | None = Field(
        default=None, description="Mainly used in combination with Shape.RECTANGLE"
    )
    fill_color: ColorDescriptor = Field(
        default=None,
    )
    fill_style: FillStyle | None = Field(
        default=None,
    )
    stroke_color: ColorDescriptor = Field(
        default=None,
    )
    stroke_width: int | None = Field(
        default=None,
    )
    text_direction: TextDirection | None = Field(
        default=None,
    )
    resizable: bool | None = Field(
        default=None,
    )
    rotatable: bool | None = Field(
        default=None,
    )
    autosize: bool | None = Field(
        default=None,
    )
    align: Align | None = Field(
        default=None,
    )
    vertical_align: VerticalAlign | None = Field(
        default=None,
    )
    size: int | None = Field(
        default=None,
    )
    perimeter: Perimeter | None = Field(
        default=None, description="Mainly used in combination with Shape.WAYPOINT"
    )


def map_color_descriptor(style_attributes_color_descriptor: ColorDescriptor) -> str | None:
    """
    Function for mapping a color descriptor to its corresponding XML attribute value.

    :param style_attributes_color_descriptor: ColorDescriptor to be mapped
    :type style_attributes_color_descriptor: ColorDescriptor
    :return: Optional hex color string
    :rtype: str | None
    """
    if style_attributes_color_descriptor:
        if isinstance(style_attributes_color_descriptor, Color):
            return style_attributes_color_descriptor.as_hex(format="long")
        if style_attributes_color_descriptor == "NONE":
            return "none"
    return None


def map_shape(style_attributes: StyleAttributes, stroke_colors: list[str]) -> MxCellStyleShape:
    """
    Function for mapping style attributes and stroke
    colors to the corresponding XML attribute value.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :param stroke_colors: Stroke colors to be mapped
    :type stroke_colors: list[str]
    :return: Corresponding MxCellStyleShape value
    :rtype: MxCellStyleShape
    """
    stroke_colors_len = len(stroke_colors)

    if stroke_colors_len > 2:
        raise ValueError("Currently only shapes with up to two stroke colors are supported.")

    if stroke_colors_len == 2 and style_attributes.shape == Shape.DIAG_ROUND_RECTANGLE:
        return get_split_border_rectangle_shape(stroke_colors[0], stroke_colors[1])
        # TODO: use correct shape (wait for the custom drawio shape library)

    if stroke_colors_len == 2 and not style_attributes.shape == Shape.DIAG_ROUND_RECTANGLE:
        raise ValueError("The used shape does not support more than one stroke color.")

    match style_attributes.shape:
        case Shape.RECTANGLE:
            return MxCellStyleDefaultShape.RECTANGLE
        case Shape.ELLIPSE:
            return MxCellStyleDefaultShape.ELLIPSE
        case Shape.TEXT:
            return MxCellStyleDefaultShape.TEXT
        case Shape.WAYPOINT:
            return MxCellStyleDefaultShape.WAYPOINT
        case Shape.DIAG_ROUND_RECTANGLE:
            return MxCellStyleDefaultShape.DIAG_ROUND_RECTANGLE


def map_rounded(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `rounded` value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.rounded


def map_fill_color(style_attributes: StyleAttributes) -> Optional[str]:
    """
    Function for mapping the StyleAttributes' `fill_color`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[str]
    """
    return map_color_descriptor(style_attributes.fill_color)


def map_fill_style(style_attributes: StyleAttributes) -> Optional[MxCellStyleFillStyle]:
    """
    Function for mapping the StyleAttributes' `fill_style`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleFillStyle]
    """
    match style_attributes.fill_style:
        case FillStyle.SOLID:
            return MxCellStyleFillStyle.SOLID
        case FillStyle.HATCH:
            return MxCellStyleFillStyle.HATCH
        case FillStyle.CROSS_HATCH:
            return MxCellStyleFillStyle.CROSS_HATCH
        case _:
            return None


def map_stroke_color(style_attributes: StyleAttributes) -> Optional[str]:
    """
    Function for mapping the StyleAttributes' `stroke_color`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[str]
    """
    return map_color_descriptor(style_attributes.stroke_color)


def map_stroke_width(style_attributes: StyleAttributes) -> Optional[int]:
    """
    Function for mapping the StyleAttributes' `stroke_width`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[int]
    """
    return style_attributes.stroke_width


def map_text_direction(style_attributes: StyleAttributes) -> Optional[MxCellStyleTextDirection]:
    """
    Function for mapping the StyleAttributes' `text_direction`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleTextDirection]
    """
    match style_attributes.text_direction:
        case TextDirection.HORIZONTAL:
            return MxCellStyleTextDirection.LTR
        case TextDirection.VERTICAL:
            return MxCellStyleTextDirection.VERTICAL_LR
        case _:
            return None


def map_resizable(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `resizable`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.resizable


def map_rotatable(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `rotatable`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.rotatable


def map_autosize(style_attributes: StyleAttributes) -> Optional[bool]:
    """
    Function for mapping the StyleAttributes' `autosize`
    value to the corresponding XML attributes.

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[bool]
    """
    return style_attributes.autosize


def map_align(style_attributes: StyleAttributes) -> Optional[MxCellStyleAlign]:
    """
    Function for mapping the StyleAttributes' `align`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleAlign]
    """
    match style_attributes.align:
        case Align.CENTER:
            return MxCellStyleAlign.CENTER
        case Align.LEFT:
            return MxCellStyleAlign.LEFT
        case Align.RIGHT:
            return MxCellStyleAlign.RIGHT
        case _:
            return None


def map_vertical_align(style_attributes: StyleAttributes) -> Optional[MxCellStyleVerticalAlign]:
    """
    Function for mapping the StyleAttributes' `vertical_align`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStyleVerticalAlign]
    """
    match style_attributes.vertical_align:
        case VerticalAlign.MIDDLE:
            return MxCellStyleVerticalAlign.MIDDLE
        case VerticalAlign.TOP:
            return MxCellStyleVerticalAlign.TOP
        case VerticalAlign.BOTTOM:
            return MxCellStyleVerticalAlign.BOTTOM
        case _:
            return None


def map_size(style_attributes: StyleAttributes) -> Optional[int]:
    """
    Function for mapping the StyleAttributes' `size`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :type style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[int]
    """
    return style_attributes.size


def map_perimeter(style_attributes: StyleAttributes) -> Optional[MxCellStylePerimeter]:
    """
    Function for mapping the StyleAttributes' `perimeter`
    value to the corresponding XML attributes.'

    :param style_attributes: StyleAttributes to be mapped
    :param style_attributes: StyleAttributes
    :return: Corresponding MxCellStyle value
    :rtype: Optional[MxCellStylePerimeter]
    """
    match style_attributes.perimeter:
        case Perimeter.CENTER:
            return MxCellStylePerimeter.CENTER_PERIMETER
        case _:
            return None


class StyleConfig(BaseModel):
    """
    Model for defining a style config.
    """

    model_config = ConfigDict(
        extra="forbid",
        title="Style Config Schema",
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "id": "https://gitlab.uni-ulm.de/se/mbti/automated-architecture-analysis"
            + "/src/aranea/models/style-config-schema-v1.0.json",
        },
    )

    node_type_style_attributes: Dict[NodeType, StyleAttributes] | None = Field(
        default=None,
    )
    node_classification_style_attributes: Dict[EcuClassification, StyleAttributes] | None = Field(
        default=None,
    )
    network_protocol_type_style_attributes: Dict[ProtocolType, StyleAttributes] | None = Field(
        default=None,
    )

    def get_node_type_style_attributes(self, node_type: NodeType) -> StyleAttributes | None:
        """
        Function for getting the style attributes for a node type.

        :param node_type: NodeType to get the style attributes for
        :type node_type: NodeType
        :return Corresponding style attributes
        :rtype: StyleAttributes | None
        """
        if not self.node_type_style_attributes:
            return None

        if (
            node_type not in self.node_type_style_attributes
        ):  # pylint: disable=unsupported-membership-test
            return None

        return self.node_type_style_attributes[node_type]  # pylint: disable=unsubscriptable-object

    def get_network_protocol_style_attributes(
        self, protocol: ProtocolType
    ) -> StyleAttributes | None:
        """
        Function for getting the style attributes for a network protocol.

        :param protocol: ProtocolType to get the style attributes for
        :type protocol: ProtocolType
        :return: Corresponding style attributes
        :rtype: StyleAttributes | None
        """
        if not self.network_protocol_type_style_attributes:
            return None

        return self.network_protocol_type_style_attributes[
            protocol
        ]  # pylint: disable=unsubscriptable-object

    def get_node_classifications_style_attributes(
        self, node_classifications: list[EcuClassification]
    ) -> list[StyleAttributes] | None:
        """
        Function for getting the style attributes for a node classifications.

        :param node_classifications: Node classifications to get the
        style attributes for
        :type node_classifications: list[EcuClassification]
        :return: Corresponding style attributes list
        :rtype: list[StyleAttributes] | None
        """
        if not self.node_classification_style_attributes:
            return None

        classification_styles: list[StyleAttributes] = []

        for classification in node_classifications:
            if (
                classification not in self.node_classification_style_attributes
            ):  # pylint: disable=unsupported-membership-test
                continue

            classification_styles.append(
                self.node_classification_style_attributes[classification]
            )  # pylint: disable=unsubscriptable-object

        return classification_styles if len(classification_styles) > 0 else None

    def get_combined_style_attributes_and_stroke_colors(
        self,
        *,
        node_type: Optional[NodeType] = None,
        node_classifications: Optional[list[EcuClassification]] = None,
        protocol_type: Optional[ProtocolType] = None,
    ) -> Tuple[StyleAttributes, list[str]]:
        """
        Function for combining style attributes based on NodeType,
        EcuClassifications and ProtocolType.

        :param node_type: NodeType to get the style attributes for
        :type node_type: NodeType
        :param node_classifications: EcuClassifications to get
        the style attributes for
        :type node_classifications: list[EcuClassification]
        :param protocol_type: ProtocolType to get the style attributes for
        :type protocol_type: ProtocolType
        :return: Corresponding style attributes and color list
        :rtype: Tuple[StyleAttributes, list[str]]
        """
        stroke_colors: list[str] = []  # keep track if multiple stroke colors should apply
        style_attributes: StyleAttributes = StyleAttributes()

        if node_type:
            if node_type_style_attributes := self.get_node_type_style_attributes(node_type):
                style_attributes = merge_models(
                    style_attributes, node_type_style_attributes, StyleAttributes
                )
                if node_type_stroke_colors := map_color_descriptor(
                    node_type_style_attributes.stroke_color
                ):
                    stroke_colors.append(node_type_stroke_colors)

        if node_classifications:
            if node_classifications_styles_attributes := (
                self.get_node_classifications_style_attributes(node_classifications)
            ):
                for (
                    classification_style_attributes
                ) in node_classifications_styles_attributes:  # pylint: disable=not-an-iterable
                    if classification_stroke_color := map_color_descriptor(
                        classification_style_attributes.stroke_color
                    ):
                        stroke_colors.append(classification_stroke_color)
                    style_attributes = merge_models(
                        style_attributes, classification_style_attributes, StyleAttributes
                    )

        if protocol_type:
            if protocol_type_styles_attributes := self.get_network_protocol_style_attributes(
                protocol_type
            ):
                style_attributes = merge_models(
                    style_attributes, protocol_type_styles_attributes, StyleAttributes
                )
                if protocol_type_stroke_colors := map_color_descriptor(
                    protocol_type_styles_attributes.stroke_color
                ):
                    stroke_colors.append(protocol_type_stroke_colors)

        return style_attributes, stroke_colors

    def get_mx_cell_style(
        self,
        *,
        node_type: Optional[NodeType] = None,
        node_classifications: Optional[list[EcuClassification]] = None,
        protocol_type: Optional[ProtocolType] = None,
    ) -> MxCellStyle:
        """
        Function for getting the `MxCellStyle` based on NodeType,
        EcuClassifications and ProtocolType.

        :param node_type: NodeType to get the style attributes for
        :type node_type: NodeType
        :param node_classifications: EcuClassifications to get
        the style attributes for
        :type node_classifications: list[EcuClassification]
        :param protocol_type: ProtocolType to get the style attributes for
        :type protocol_type: ProtocolType
        :return: Composed cell style
        :rtype: MxCellStyle
        """
        combined_style_attributes, stroke_colors = (
            self.get_combined_style_attributes_and_stroke_colors(
                node_type=node_type,
                node_classifications=node_classifications,
                protocol_type=protocol_type,
            )
        )
        mx_cell_shape = map_shape(combined_style_attributes, stroke_colors)

        return MxCellStyle(
            shape=mx_cell_shape,
            rounded=map_rounded(combined_style_attributes),
            fillColor=map_fill_color(combined_style_attributes),
            fillStyle=map_fill_style(combined_style_attributes),
            strokeColor=map_stroke_color(combined_style_attributes),
            strokeWidth=map_stroke_width(combined_style_attributes),
            textDirection=map_text_direction(combined_style_attributes),
            resizable=map_resizable(combined_style_attributes),
            rotatable=map_rotatable(combined_style_attributes),
            autosize=map_autosize(combined_style_attributes),
            align=map_align(combined_style_attributes),
            verticalAlign=map_vertical_align(combined_style_attributes),
            size=map_size(combined_style_attributes),
            perimeter=map_perimeter(combined_style_attributes),
        )
