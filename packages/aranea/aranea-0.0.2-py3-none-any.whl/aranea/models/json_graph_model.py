"""
This module provides the pydantic model for working with graph data.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Dict, List, Set, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UuidVersion
from shapely import Polygon

# pylint: disable=line-too-long, missing-class-docstring


class NodeType(Enum):
    COMPONENT = "COMPONENT"
    XOR = "XOR"
    TEXT = "TEXT"
    WAYPOINT = "WAYPOINT"


class Node(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: NodeType
    x: float = Field(
        description="Origin is in upper left corner of the document, x increases to the right.",
    )
    y: float = Field(
        description="Origin is in upper left corner of the document, y increases downwards.",
    )


class TechnicalCapability(Enum):
    NETWORK_SWITCH = "NETWORK_SWITCH"
    BACKEND = "BACKEND"
    CELLULAR = "CELLULAR"
    WIFI = "WIFI"
    BLUETOOTH = "BLUETOOTH"
    USB = "USB"
    SATELLITE = "SATELLITE"
    CAR_CHARGER = "CAR_CHARGER"
    DIGITAL_BROADCAST = "DIGITAL_BROADCAST"
    ANALOG_BROADCAST = "ANALOG_BROADCAST"
    NFC = "NFC"


class EcuClassification(Enum):
    ECU = "ECU"
    NEW_ECU = "NEW_ECU"
    ECU_ONLY_IN_BR = "ECU_ONLY_IN_BR"
    DOMAIN_GATEWAY = "DOMAIN_GATEWAY"
    NON_DOMAIN_GATEWAY = "NON_DOMAIN_GATEWAY"
    LIN_CONNECTED_ECU = "LIN_CONNECTED_ECU"
    ENTRY_POINT = "ENTRY_POINT"
    CRITICAL_ELEMENT = "CRITICAL_ELEMENT"
    EXTERNAL_INTERFACE = "EXTERNAL_INTERFACE"


class ComponentNode(Node):
    type: NodeType = NodeType.COMPONENT
    height: float
    width: float
    innerText: str | None = None
    outerText: str | None = None
    amg_only: bool = False
    technical_capabilities: Set[TechnicalCapability] = set()
    classifications: Set[EcuClassification] = {EcuClassification.ECU}

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.x,
                self.y,
                self.height,
                self.width,
                self.innerText,
                self.outerText,
                self.amg_only,
                tuple(self.technical_capabilities),
                tuple(self.classifications),
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)

    def polygon(self, *, buffer: float = 0.0) -> Polygon:
        """
        Returns the polygon representation of the component's rectangle

        :param buffer: Increase the rectangle's dimensions by `buffer` in all directions
        :type buffer: float
        :return: The polygon representation of the rectangle
        :rtype: Polygon
        """
        _x = self.x
        _y = self.y
        _width = self.width
        _height = self.height

        return Polygon(
            (
                (_x - buffer, _y - buffer),
                (_x - buffer, _y + _height + buffer),
                (_x + _width + buffer, _y + _height + buffer),
                (_x + _width + buffer, _y - buffer),
                (_x - buffer, _y - buffer),
            )
        )


class XorNode(Node):
    type: NodeType = NodeType.XOR
    height: float
    width: float
    innerText: str | None = "XOR"

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.x,
                self.y,
                self.height,
                self.width,
                self.innerText,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class TextNode(Node):
    type: NodeType = NodeType.TEXT
    innerText: str | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.x,
                self.y,
                self.innerText,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class WaypointNode(Node):
    type: NodeType = NodeType.WAYPOINT

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.x,
                self.y,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class TextOrientation(Enum):
    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"


class ProtocolType(Enum):
    CAN = "CAN"
    CAN_250 = "CAN_250"
    CAN_500 = "CAN_500"
    CAN_800 = "CAN_800"
    CAN_FD = "CAN_FD"
    FLEX_RAY = "FLEX_RAY"
    ETHERNET = "ETHERNET"
    MOST_ELECTRIC = "MOST_ELECTRIC"
    LIN = "LIN"
    UNKNOWN = "UNKNOWN"
    OTHER = "OTHER"


class Network(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protocolType: ProtocolType
    masterId: Annotated[UUID, UuidVersion(4)] | None = Field(
        default=None,
        description="The UUID of the bus master if applicable.",
    )
    amg_only: bool = False
    edges: List[Edge]

    def __hash__(self) -> int:
        return hash(
            (
                self.protocolType,
                self.amg_only,
            )
        )


class Edge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sourceId: Annotated[UUID, UuidVersion(4)]
    targetId: Annotated[UUID, UuidVersion(4)]
    sourceAttachmentPointX: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, x increases to the right.",
    )
    sourceAttachmentPointY: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, y increases downwards.",
    )
    targetAttachmentPointX: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, x increases to the right.",
    )
    targetAttachmentPointY: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, y increases downwards.",
    )

    text: str | None = None
    textOrientation: TextOrientation | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.sourceAttachmentPointX,
                self.sourceAttachmentPointY,
                self.targetAttachmentPointX,
                self.targetAttachmentPointY,
                self.text,
                self.textOrientation,
            )
        )


NodeUnionType = Union[WaypointNode, TextNode, XorNode, ComponentNode]


class Graph(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    nodes: Dict[Annotated[UUID, UuidVersion(4)], NodeUnionType]
    networks: List[Network]

    @classmethod
    def get_network_tuple(
        cls, network: Network, graph: Graph
    ) -> tuple[Network, Node | None, tuple[Any, ...]]:
        """
        Get a tuple of (network, network_master, tuple[tuple[edge, source, target]])
        """
        nw_edges: Set[tuple[Edge, Node, Node]] = set()
        for edge in network.edges:
            edge_source = graph.nodes.get(edge.sourceId)
            if edge_source is None:
                raise ReferenceError(f"Could not find source node {edge.sourceId}")
            edge_target = graph.nodes.get(edge.targetId)
            if edge_target is None:
                raise ReferenceError(f"Could not find target node {edge.targetId}")
            nw_edges.add((edge, edge_source, edge_target))

        nw_master = graph.nodes.get(network.masterId) if network.masterId else None
        return (network, nw_master, tuple(nw_edges))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if not self.label == other.label:
            return False

        node_occurrences: Dict[Node, int] = {}

        # count all node_occurrences in self.nodes
        for node in self.nodes.values():
            if node in node_occurrences:
                node_occurrences[node] += 1
            else:
                node_occurrences[node] = 1

        # count all node_occurrences other.nodes
        for other_node in other.nodes.values():
            if other_node in node_occurrences:
                node_occurrences[other_node] -= 1
            else:
                return False

        if any(item != 0 for item in node_occurrences.values()):
            return False

        # count tuples of (network, network_master, list[tuple[edge, source, target]])
        network_occurences: Dict[
            tuple[Network, Node | None, tuple[tuple[Edge, Node, Node]]],
            int,
        ] = {}

        for network in self.networks:
            nw_tuple = self.get_network_tuple(network, self)
            if nw_tuple in network_occurences:
                network_occurences[nw_tuple] += 1
            else:
                network_occurences[nw_tuple] = 1

        for network in other.networks:
            nw_tuple = self.get_network_tuple(network, other)
            if nw_tuple in network_occurences:
                network_occurences[nw_tuple] -= 1
            else:
                return False

        if any(item != 0 for item in network_occurences.values()):
            return False

        return True


class GraphCollection(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        title="Graph Schema",
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "id": "https://gitlab.uni-ulm.de/se/mbti/automated-architecture-analysis/src/aranea/schema/graph-schema-v1.0.json",
        },
    )

    graphs: List[Graph]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.graphs == other.graphs
