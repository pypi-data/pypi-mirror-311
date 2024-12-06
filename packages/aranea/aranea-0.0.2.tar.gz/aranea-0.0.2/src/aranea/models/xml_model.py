"""
This module defines the model used for creating an XML file in drawio flavor.
"""

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List, Optional, Self
from uuid import UUID, uuid4

from pydantic import model_validator
from pydantic_xml import BaseXmlModel, attr, computed_attr

from aranea.models.utils import is_valid_style_string

# Since "as" is a reserved keyword in Python I decided to prefix
# attributes with "attr_" in order to prevent issues with the interpreter


class MxGeometry(BaseXmlModel, tag="mxGeometry"):
    """
    Base model class for defining a <mxGeometry />
    """

    attr_as: str = attr(name="as", default="geometry")


class MxGeometryShape(MxGeometry):
    """
    Model class for defining a <mxGeometry /> for a shape
    """

    attr_x: float = attr(name="x")
    attr_y: float = attr(name="y")
    attr_height: float = attr(name="height")
    attr_width: float = attr(name="width")


class MxGeometryEdge(MxGeometry):
    """
    Model class for defining a <mxGeometry /> for an edge
    """

    attr_relative: int = attr(name="relative", default=1)


class MxCell(BaseXmlModel, tag="mxCell", skip_empty=True):
    """
    Base model class for defining a <mxCell />
    """

    attr_id: UUID = attr(name="id", default_factory=uuid4)
    attr_value: Optional[str] = attr(name="value", default=None)
    attr_parent: Optional[UUID] = attr(name="parent", default=None)
    attr_style: Optional[str] = attr(name="style", default=None)

    @model_validator(mode="after")
    def validate_style_string(self) -> Self:
        """
        Custom validator function for checking style strings used in <mxCell />.
        :return: The checked instance
        :rtype: Self
        """
        if self.attr_style is not None and not is_valid_style_string(self.attr_style):
            raise ValueError("Malformed style string")
        return self


class MxCellStyleDefaultShape(Enum):
    """
    Enum for defining the shape property in a cells style attribute.
    """

    RECTANGLE = "rectangle"
    ELLIPSE = "ellipse"
    WAYPOINT = "waypoint"
    TEXT = "text"
    DIAG_ROUND_RECTANGLE = "mxgraph.basic.diag_round_rect"
    IMAGE = "image"


class MxCellStylePerimeter(Enum):
    """
    Enum for defining the perimeter property in a cells style attribute.
    """

    CENTER_PERIMETER = "centerPerimeter"


class MxCellStyleFillStyle(Enum):
    """
    Enum for defining the fill property in a cells style attribute.
    """

    HATCH = "hatch"
    SOLID = "solid"
    CROSS_HATCH = "cross-hatch"


class MxCellStyleTextDirection(Enum):
    """
    Enum for defining the text direction property in a cells style attribute.
    """

    VERTICAL_LR = "vertical-lr"
    LTR = "ltr"


class MxCellStyleAlign(Enum):
    """
    Enum for defining the text align property in a cells style attribute.
    """

    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


class MxCellStyleVerticalAlign(Enum):
    """
    Enum for defining the vertical text align property
    in a cells style attribute.
    """

    MIDDLE = "middle"
    TOP = "top"
    BOTTOM = "bottom"


@dataclass(kw_only=True)
class Point:
    """
    Class for representing a point
    """

    x: float = field()
    y: float = field()


MxCellStyleShape = MxCellStyleDefaultShape | str  # string is needed for custom shapes


@dataclass(kw_only=True)
class MxCellStyle:  # pylint: disable=too-many-instance-attributes
    """
    Data class for defining the style of an <mxCell />.

    To get more information on available properties have a look at the
    drawio code.

    https://github.com/jgraph/drawio/blob/dev/src/main/webapp/mxgraph/src/util/mxConstants.js
    """

    shape: MxCellStyleShape
    rounded: Optional[bool] = field(default=None)
    fillColor: Optional[str] = field(default=None)  # pylint: disable=C0103
    fillStyle: Optional[MxCellStyleFillStyle] = field(default=None)  # pylint: disable=invalid-name
    strokeColor: Optional[str] = field(default=None)  # pylint: disable=invalid-name
    strokeWidth: Optional[int] = field(default=None)  # pylint: disable=invalid-name
    textDirection: Optional[MxCellStyleTextDirection] = field(
        default=None
    )  # pylint: disable=invalid-name
    resizable: Optional[bool] = field(default=None)
    autosize: Optional[bool] = field(default=None)
    align: Optional[MxCellStyleAlign] = field(default=None)
    verticalAlign: Optional[MxCellStyleVerticalAlign] = field(
        default=None
    )  # pylint: disable=invalid-name
    size: Optional[int] = field(default=None)
    rotatable: Optional[bool] = field(default=None)
    connectable: Optional[bool] = field(default=None)
    perimeter: Optional[MxCellStylePerimeter] = field(default=None)
    points: Optional[list[Point]] = field(default=None)
    image: Optional[str] = field(default=None)

    # `points` is representing the attachment points of an element with coordinates relative
    # to the respective element

    def to_semicolon_string(self) -> str | None:
        """
        Transforms the style attributes to a key=value pair string that are
        separated by semicolons.

        :return: Semicolon separated string of key=value pairs.
        :rtype: str
        """
        items = []
        for key, value in asdict(self).items():
            if value is None:
                continue  # Skip attributes with None values
            if isinstance(value, bool):
                items.append(f"{key}={int(value)}")  # Convert boolean to 0 or 1
            elif key == "points":
                # Format points as [[x1, y1], [x2, y2]]
                points_str = "[" + ",".join(f"[{v["x"]},{v["y"]}]" for v in value) + "]"
                items.append(f"{key}={points_str}")
            elif isinstance(value, Enum):
                items.append(f"{key}={value.value}")
            else:
                items.append(f"{key}={value}")

        if len(items) == 0:
            return None

        return ";".join(items)


class MxCellEdge(MxCell):
    """
    Model class for defining a <mxCell /> for an edge
    """

    attr_edge: int = attr(name="edge", default=1)
    attr_source: UUID = attr(name="source")
    attr_target: UUID = attr(name="target")
    geometry: MxGeometryEdge


class MxCellShape(MxCell):
    """
    Model class for defining a <mxCell /> for a shape
    """

    attr_vertex: int = attr(name="vertex", default=1)
    geometry: MxGeometryShape


RootCells = MxCellEdge | MxCellShape | MxCell


# The MxCell is needed as child of the Root for layer creation.
# A layer is represented as a child of the upmost MxCell and is
# then referenced by its contained elements.


class Root(BaseXmlModel, tag="root"):
    """
    Model class for defining a <root />
    """

    cells: List[RootCells]


class MxGraphModel(BaseXmlModel, tag="mxGraphModel", skip_empty=True):
    """
    Model class for defining a <mxGraphModel />
    """

    attr_page: Optional[int] = attr(name="page", default=1)
    attr_page_width: Optional[float] = attr(name="pageWidth", default=None)
    attr_page_height: Optional[float] = attr(name="pageHeight", default=None)
    attr_page_scale: Optional[float] = attr(name="pageScale", default=1.0)
    attr_arrows: Optional[int] = attr(name="arrows", default=0)
    attr_connect: Optional[int] = attr(name="connect", default=1)
    attr_tooltips: Optional[int] = attr(name="tooltips", default=1)
    attr_guides: Optional[int] = attr(name="guides", default=1)
    attr_grid: Optional[int] = attr(name="grid", default=1)
    attr_grid_size: Optional[int] = attr(name="gridSize", default=10)
    root: Root


class Diagram(BaseXmlModel, tag="diagram"):
    """
    Model class for defining a <diagram />
    """

    attr_id: UUID = attr(name="id", default_factory=uuid4)
    attr_name: str = attr(name="name")
    graph_model: MxGraphModel


class MxFile(BaseXmlModel, tag="mxfile", skip_empty=True):
    """
    Model class for defining a <mxfile />
    """

    diagrams: List[Diagram]

    @computed_attr(name="pages")  # type: ignore
    # https://docs.pydantic.dev/2.0/usage/computed_fields/
    def pages(self) -> int:
        """
        Method used by pydantic_xml to compute the corresponding attribute.
        :return: Amount of current diagram pages
        :rtype: int
        """
        return len(self.diagrams)
