"""
This module provides functionality to read and process PDF files to extract
Electronic Control Units (ECUs) using the pymupdf library.
"""

import re
from collections.abc import Generator
from math import isclose, sqrt
from os.path import isfile
from typing import Annotated, Any, List, Tuple
from uuid import uuid4

import pymupdf
from pymupdf.pymupdf import Page, Rect
from pymupdf.utils import get_text_blocks
from shapely import LineString, Polygon

from aranea.models.json_graph_model import (ComponentNode, EcuClassification,
                                            Graph, NodeType, XorNode)


class PDFReader:
    """
    A class to parse information of an Automotive Architecture (mainly its
    ECUs, networks) from the specified page of the provided PDF file.
    """

    def __init__(self, pdfpath: str, pagenumber: int = 0) -> None:
        self.path = pdfpath
        if not isfile(pdfpath):
            raise IOError("Input is no file")
        with open(pdfpath, "rb") as inpf:
            if inpf.read(5) != b"%PDF-":
                raise IOError("Input is not a PDF file")
            doc = pymupdf.open(inpf, filetype="pdf")
        self.metadata = doc.metadata or {}
        self.page: Page = doc.load_page(pagenumber)

    def __remove_nested_ecus(
        self, ecus: List[ComponentNode] | Generator[ComponentNode]
    ) -> Generator[ComponentNode]:
        for ecu in ecus:
            for other_ecu in ecus:
                if ecu == other_ecu:
                    continue
                if other_ecu.polygon().contains(ecu.polygon()):
                    break
            else:
                yield ecu

    def __remove_diagram_key_ecus(
        self, nodes: List[ComponentNode] | Generator[ComponentNode]
    ) -> Generator[ComponentNode]:
        """
        Removes all ComponentNodes where no line is nearby
        """
        lines = [
            item
            for path in self.page.get_drawings(extended=False)
            for item in path.get("items")
            if item[0] == "l"
        ]

        # TODO: only checking nodes that are not part of any network would
        # reduce the amount of intersection checks and speed this up (only
        # possible once networks got extracted)
        for node in nodes:
            if node.type != NodeType.COMPONENT:
                continue
            margin = 10
            if any(
                [node.polygon(buffer=margin).intersects(LineString(line[1:])) for line in lines]
            ):
                yield node

    def __is_horizontal(self, x0: float, y0: float, x1: float, y1: float) -> bool:
        return abs(x1 - x0) > abs(y1 - y0)

    def __get_inner_ecu_text(
        self,
        ecu: ComponentNode,
        word_blocks: List[Tuple[float, float, float, float, str, int, int]],
    ) -> str | None:
        rect = (
            ecu.x + 1,
            ecu.y + 1,
            ecu.x + ecu.width - 1,
            ecu.y + ecu.height - 1,
        )

        inner_texts = [
            w
            for w in word_blocks
            if self.__is_horizontal(*w[:4]) and pymupdf.Rect(w[:4]).intersects(rect)
        ]

        def __cleanup(text_blocks: List[Tuple[float, float, float, float, str, int, int]]) -> str:
            seen_block_strings = set()
            block_strings = []
            for block in text_blocks:
                seen = set()
                lines = []
                for line in block[4].split("\n"):
                    line = line.strip()
                    if line not in seen:
                        seen.add(line)
                        lines.append(line.strip())
                block_string = " ".join(lines).strip()
                if block_string not in seen_block_strings:
                    seen_block_strings.add(block_string)
                    block_strings.append(block_string)
            return "\n".join(block_strings)

        if inner_texts is not None and len(inner_texts) > 0:
            return __cleanup(inner_texts)
        return None

    def __get_outer_ecu_text(
        self,
        ecu: ComponentNode,
        word_blocks: List[Tuple[float, float, float, float, str, int, int]],
    ) -> Tuple[str, bool] | Tuple[None, bool]:
        rect = (ecu.x, ecu.y - 4, ecu.x + ecu.width, ecu.y - 1)

        def __vert_distance2ecu(y1: float) -> float:
            d: float = y1 - ecu.y
            return -d if d < 0 else d

        outer_texts = [
            w
            for w in word_blocks
            if self.__is_horizontal(*w[:4]) and pymupdf.Rect(w[:4]).intersects(rect)
        ]

        def __cleanup(outer_text: str) -> Tuple[str, bool]:
            seen = set()
            lines = []
            for line in outer_text.split("\n"):
                if line not in seen:
                    seen.add(line.strip())
                    lines.append(line.strip())
            outer_text = " ".join(lines)

            amg_only = re.search(r"amg[\s_-]*only", outer_text, flags=re.IGNORECASE) is not None
            outer_text = re.sub(r"\(?amg[\s]*only\)?", "", outer_text, flags=re.IGNORECASE)
            outer_text = outer_text.replace("*", "").strip()

            return outer_text, amg_only

        if outer_texts is not None and len(outer_texts) > 0:
            outer_text = min(outer_texts, key=lambda t: __vert_distance2ecu(t[3]))
            return __cleanup(outer_text[4])
        return None, False

    def __get_ecu_labels(
        self, ecus: List[ComponentNode] | Generator[ComponentNode]
    ) -> Generator[ComponentNode]:
        """
        Extracts the ECU labels from the page for the all ECUs of `ecus`

        :param ecus: The ecus to process.
        :type ecus: List[ComponentNode] | Generator[ComponentNode]
        :return: A generator for ComponentNode with the extracted labels
        :rtype: Generator[ComponentNode]
        """

        # word_blocks = self.page.get_text("blocks")
        word_blocks = get_text_blocks(
            self.page,
            flags=pymupdf.TEXT_INHIBIT_SPACES,
        )
        for ecu in ecus:
            ecu.innerText = self.__get_inner_ecu_text(ecu, word_blocks)
            ecu.outerText, ecu.amg_only = self.__get_outer_ecu_text(ecu, word_blocks)

            yield ecu

    def get_ecus(
        self,
        *,
        min_height: float = 15,
        max_height: float = 21,
    ) -> List[ComponentNode]:
        """
        Extracts the ``ComponentNode`` of all Electronic
        Control Units (ECUs) from the page drawings based on their height.

        :param min_height: Minimum height of the rectangle to be considered as an ECU. Default: 15
        :type min_height: float
        :param max_height: Maximum height of the rectangle to be considered as an ECU. Default: 21
        :type max_height: float
        :return: A generator of unique ECUs.
        :rtype: List[ComponentNode]
        """
        ecu_rects: dict[Polygon, ComponentNode] = {}
        for path in self.page.get_drawings(extended=False):
            if not "items" in path:
                continue

            for item in path["items"]:
                if item[0] == "re":
                    rect = item[1]

                    if rect.height >= min_height and rect.height <= max_height:
                        ecu_rect = ComponentNode(
                            x=rect.x0,
                            y=rect.y0,
                            width=rect.x1 - rect.x0,
                            height=rect.y1 - rect.y0,
                        )
                        ecu_rects[ecu_rect.polygon()] = ecu_rect

        return list(
            self.__remove_diagram_key_ecus(
                self.__get_ecu_labels(self.__remove_nested_ecus(list(ecu_rects.values())))
            )
        )

    def __calculate_distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """
        Calculates the Euclidean distance between two points.

        :param p1: The first point, as a tuple of (x, y) coordinates.
        :type p1: Tuple[float, float]
        :param p2: The second point, as a tuple of (x, y) coordinates.
        :type p2: Tuple[float, float]
        :return: The distance between the two points.
        :rtype: float
        """
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def __is_diamond(self, points: List[Tuple[float, float]], tolerance: float = 5) -> bool:
        """
        Checks if the given points form a diamond shape by verifying that all side lengths are
        nearly equal.

        :param points: A list of four points (tuples of x, y coordinates) representing the vertices
                       of the shape.
        :type points: List[Tuple[float, float]]
        :param tolerance: The tolerance for comparing side lengths, default is 0.1.
        :type tolerance: float
        :return: True if the points form a diamond (all sides are nearly equal within the
                 tolerance), False otherwise.
        :rtype: bool
        """
        if len(points) != 4:
            return False

        # calculate side lengths
        d1 = self.__calculate_distance(points[0], points[1])
        d2 = self.__calculate_distance(points[1], points[2])
        d3 = self.__calculate_distance(points[2], points[3])
        d4 = self.__calculate_distance(points[3], points[0])

        # checks if all sides are nearly the same length
        return (
            isclose(d1, d2, abs_tol=tolerance)
            and isclose(d2, d3, abs_tol=tolerance)
            and isclose(d3, d4, abs_tol=tolerance)
        )

    def __is_overlapping(
        self,
        bbox1: Tuple[float, float, float, float],
        bbox2: Tuple[float, float, float, float],
        threshold: float = 0.3,
    ) -> bool:
        """
        Checks if two bounding boxes overlap by more than the specified threshold.

        The overlap is calculated as a percentage of the area of the smaller bounding box.

        :param bbox1: Bounding box of the first text (x0, y0, x1, y1).
        :param bbox2: Bounding box of the second text (x0, y0, x1, y1).
        :param threshold: The overlap threshold (default is 0.3 for 30%).
        :return: True if the overlap is greater than the threshold; otherwise, False.
        """
        # Calculate the area of intersection
        x_overlap = max(0, min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0]))
        y_overlap = max(0, min(bbox1[3], bbox2[3]) - max(bbox1[1], bbox2[1]))
        intersection_area = x_overlap * y_overlap

        # Calculate the area of the smaller box
        bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        bbox2_area = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
        smaller_area = min(bbox1_area, bbox2_area)

        # Determine if overlap is greater than the threshold
        return (intersection_area / smaller_area) > threshold

    def __get_text_in_diamond(self, rect: Rect, texts: List[dict[str, Any]]) -> str:
        """
        Extracts and concatenates text within a given diamond area.

        This function iterates over text blocks and collects texts that fall within
        the specified rectangle (rect). It sorts the texts from top to bottom,
        left to right, and removes any overlapping texts that have more than 30%
        overlap with an already included text (keeping the last-encountered text).

        :param rect: The bounding rectangle of the diamond.
        :param texts: All text blocks on the page.
        :return: A concatenated string of text within the diamond.
        """
        diamond_texts = []

        for block in texts:
            if block["type"] == 0:  # Only text blocks
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        text_bbox = span["bbox"]

                        # Check if the text is within the diamond's bounds
                        if (
                            rect.x0 < text_bbox[0]
                            and rect.x1 > text_bbox[2]
                            and rect.y0 < text_bbox[1]
                            and rect.y1 > text_bbox[3]
                        ):
                            diamond_texts.append({"text": text, "bbox": text_bbox})

        # Sort texts by y (top to bottom), then by x (left to right)
        diamond_texts = sorted(diamond_texts, key=lambda t: (t["bbox"][1], t["bbox"][0]))

        # Filter overlapping texts by keeping only the "topmost" in the stack (last in list order)
        filtered_texts: List[dict[str, Any]] = []
        for current_text in reversed(diamond_texts):  # Process from the last element to the first
            if not any(
                self.__is_overlapping(current_text["bbox"], other_text["bbox"])
                for other_text in filtered_texts
            ):
                filtered_texts.append(current_text)

        # Reverse filtered_texts to maintain original order in output
        filtered_texts.reverse()

        # Concatenate texts
        concatenated_text = " ".join(t["text"] for t in filtered_texts)
        return concatenated_text

    def __get_points_and_rect(
        self, drawing: dict[str, Any]
    ) -> Tuple[List[Tuple[float, float]], Any]:
        """
        Extracts points and rectangle information from a drawing element based on its type.

        :param drawing: The drawing element to process, containing shape or line data.
        :type drawing: dict
        :return: A tuple with a list of points and a rectangle (rect) if available, otherwise
        False.
        :rtype: Tuple[List[Tuple[float, float]], Rect] | bool
        """
        points: List[Tuple[float, float]] = []
        rect = None
        if "items" in drawing and drawing["type"] == "s":

            for item in drawing["items"]:
                if item[0] == "qu":
                    quad = item[1]
                    points = [(point.x, point.y) for point in quad]
                    rect = drawing["rect"]

        elif "items" in drawing and drawing["type"] == "fs":
            points = [(item[1].x, item[1].y) for item in drawing["items"] if item[0] == "l"]
            rect = drawing["rect"]

        return points, rect

    def get_xor_nodes(self, *, min_height: float = 10) -> List[XorNode]:
        """
        Extracts diamond shapes in the pdf

        This method iterates through the drawings on the page, identifies diamond shapes.
        It then creates Diamond and returns a list of XorNodes.

        :param min_height: The minimum height of XOR diamond shapes.
        :type min_height: float
        :return: A list of XorNodes
        :rtype: List[XorNode]
        """

        seen_diamonds = set()  # Set for monitoring diamonds that have already been found
        diamonds = []

        drawings = self.page.get_drawings()
        texts = self.page.get_text("dict")["blocks"]

        for drawing in drawings:
            points, rect = self.__get_points_and_rect(drawing)

            if len(points) > 0:
                if rect.height >= min_height:

                    # Check if the line points form a diamond
                    if self.__is_diamond(points):
                        diamond_text = self.__get_text_in_diamond(rect, texts)
                        # Convert points to tuple
                        points_tuple = tuple(sorted(points))  # sort tuples to find duplicates
                        if points_tuple not in seen_diamonds:
                            diamond = XorNode(
                                x=rect.x0,
                                y=rect.y0,
                                width=rect.height,
                                height=rect.width,
                                innerText=diamond_text.strip(),
                            )

                            seen_diamonds.add(points_tuple)  # add tuple for duplicate check
                            diamonds.append(diamond)

        return diamonds

    def get_obd_connectors(
        self,
        *,
        min_height: float = 8,
        max_height: float = 9,
        min_width: float = 27,
        max_width: float = 28,
        color: str | None = "#99ccff",
    ) -> List[ComponentNode]:
        """
        Extracts all OBD connectors from the page. There will probably be only
        one OBD connector most of the time.

        :param min_height: Minimum height of OBD connectors
        :type min_height: float
        :param max_height: Maximum height of OBD connectors
        :type max_height: float
        :param min_width: Minimum width of OBD connectors
        :type min_width: float
        :param max_width: Maximum width of OBD connectors
        :type max_width: float
        :param color: Color of the underlying rectangle of the OBD connector
        :type color: str | None
        :return: A list of OBD connectors ComponentNode
        :rtype: List[ComponentNode]
        """

        def __color2str(color: Tuple[float, float, float]) -> str:
            if color is None:
                return "#000000"
            return "#" + "".join([f"{int(x * 255):02x}" for x in color])

        word_blocks = get_text_blocks(
            self.page,
            flags=pymupdf.TEXT_INHIBIT_SPACES,
        )

        obds = []
        for path in self.page.get_drawings(extended=False):
            if not "items" in path or not "fill" in path:
                continue

            if path.get("fill_opacity") != 1.0:
                continue

            if (
                isinstance(path.get("fill"), tuple)
                and color is not None
                and __color2str(path.get("fill")) != color.lower()
            ):
                continue

            for item in path["items"]:
                if item[0] == "re":
                    rect = item[1]

                    if (
                        rect.height >= min_height
                        and rect.height <= max_height
                        and rect.width >= min_width
                        and rect.width <= max_width
                    ):
                        obd = ComponentNode(
                            x=rect.x0,
                            y=rect.y0,
                            width=rect.x1 - rect.x0,
                            height=rect.y1 - rect.y0,
                            classifications={EcuClassification.EXTERNAL_INTERFACE},
                        )
                        obds.append(obd)

                        rect = (obd.x, obd.y - 8, obd.x + obd.width, obd.y - 1)
                        outer_texts = [
                            w
                            for w in word_blocks
                            if self.__is_horizontal(*w[:4]) and pymupdf.Rect(w[:4]).intersects(rect)
                        ]
                        obd.outerText = "".join([t[4] for t in outer_texts]).replace("\n", "")
        return obds

    def get_title(self, *, width_factor: float = 0.9) -> Tuple[str, float]:
        """
        Gets the diagram's title and title size.

        It tries to find the long horizontal line above the title and then
        return the text span with the largest size.

        :param width_factor: Minimal length of the title line in relation to the diagram width
        :type width_factor: float
        :return: The title and its text size
        :rtype: Tuple[str, float]
        """

        # get all horizontal lines of a certain length
        lines = [
            item
            for path in self.page.get_drawings(extended=False)
            for item in path.get("items")
            if item[0] == "l"
            and abs(item[2].y - item[1].y) < 1
            and abs(item[2].x - item[1].x) >= self.page.mediabox.width * width_factor
        ]

        y: float
        if len(lines) > 0:
            title_line = max(lines, key=lambda l: (l[1].y, abs(l[2].x - l[1].x)))
            y = title_line[1].y
        else:
            y = self.page.mediabox.height - 36

        # get all texts below the title line as dictionaries
        texts = self.page.get_text(
            "dict",
            clip=[
                (0, y),
                (self.page.mediabox.width, self.page.mediabox.height),
            ],
        )
        spans = [
            lines.get("spans") for b in texts.get("blocks") for lines in (b.get("lines") or [])
        ]
        spans = [s for span in spans for s in span]
        title_text: str | None = None
        title_size: float = 0
        if len(spans) > 0:
            # Get the upper most text span with the largest size
            title = max(spans, key=lambda s: (s.get("size"), -s.get("origin")[1]))
            title_text = title.get("text")
            title_size = title.get("size")

        title_text = (title_text or self.metadata.get("title") or "").strip()
        return title_text, title_size

    def parse_page(
        self,
        *,
        ecu_min_height: Annotated[float, "Minimum height of ECU rectangles"] = 15,
        ecu_max_height: Annotated[float, "Maximum height of ECU rectangles"] = 21,
        xor_min_height: Annotated[float, "Minimum height of XOR diamond shapes"] = 10,
        obd_min_height: Annotated[float, "Minimum height of OBD connectors"] = 8,
        obd_max_height: Annotated[float, "Maximum height of OBD connectors"] = 9,
        obd_min_width: Annotated[float, "Minimum width of OBD connectors"] = 27,
        obd_max_width: Annotated[float, "Maximum width of OBD connectors"] = 28,
        obd_color: Annotated[
            str, "Color of the underlying rectangle of the OBD connector"
        ] = "#99ccff",
    ) -> Graph:
        """
        Tries to parse all necessary information from the PDF file.

        :param ecu_min_height: Minimum height of the rectangle to be considered as an ECU.
        :type ecu_min_height: float
        :param ecu_max_height: Maximum height of the rectangle to be considered as an ECU.
        :type ecu_max_height: float
        :param xor_min_height: The minimum height of XOR diamond shapes.
        :type xor_min_height: float
        :param obd_min_height: Minimum height of OBD connectors
        :type obd_min_height: float
        :param obd_max_height: Maximum height of OBD connectors
        :type obd_max_height: float
        :param obd_min_width: Minimum width of OBD connectors
        :type obd_min_width: float
        :param obd_max_width: Maximum width of OBD connectors
        :type obd_max_width: float
        :param obd_color: Color of the underlying rectangle of the OBD connector
        :return: A Graph representing all extracted information
        :rtype: Graph
        """

        ecus = self.get_ecus(min_height=ecu_min_height, max_height=ecu_max_height)
        xors = self.get_xor_nodes(min_height=xor_min_height)
        obds = self.get_obd_connectors(
            min_height=obd_min_height,
            max_height=obd_max_height,
            min_width=obd_min_width,
            max_width=obd_max_width,
            color=obd_color,
        )
        nodes = {uuid4(): node for node in ecus + xors + obds}

        title, _ = self.get_title()
        return Graph(label=title, nodes=dict(nodes), networks=[])
