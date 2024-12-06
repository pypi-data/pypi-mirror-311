"""Module for executing aranea."""

import logging
import os
import platform
import subprocess  # nosec B404 - See description below
import sys
from pathlib import Path
from xml.etree.ElementTree import ElementTree  # nosec B405 - no xml parsing

import click

from aranea.g2d.transform_graph_collection_to_mx_file import \
    transform_graph_collection_to_mx_file
from aranea.models.json_graph_model import Graph, GraphCollection
from aranea.models.xml_model import MxFile
from aranea.p2g.pdf2graph import PDFReader
from cli.configuration import EPILOG, Config, get_annotation_metadata

_logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "architecture_pdf_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--json-model/--no-json-model",
    "json_model",
    is_flag=True,
    show_default=True,
    default=True,
    required=False,
    type=bool,
    help="If set, the detected architecture is passed as a json file (a GraphCollection) to \
the output folder.",
)
@click.option(
    "--drawio-file/--no-drawio-file",
    "drawio_file",
    is_flag=True,
    show_default=True,
    default=True,
    required=False,
    type=bool,
    help="If set, from the detected architecture a DrawIO file is created and saved to the output\
 folder.",
)
@click.option(
    "-f",
    "--export-format",
    "export_format",
    type=click.Choice(["pdf", "png", "jpg", "svg", "vsdx", "xml"], case_sensitive=True),
    help="If set, the detected architecture is exported to the specified format. The export will\
 be disabled if the drawio_path is not set or the '--no-drawio-file' flag is set.",
)
@click.option(
    "-n",
    "--output-file-name",
    "output_file_name",
    default="aranea_result",
    show_default=True,
    type=str,
    help="You can specify a custom name for the output files.",
)
@click.option(
    "--ecu-min-height",
    "ecu_min_height",
    type=int,
    help=get_annotation_metadata(PDFReader.parse_page, "ecu_min_height")
    + "  [default: "
    + str(PDFReader.parse_page.__kwdefaults__["ecu_min_height"])
    + "]",
)
@click.option(
    "--ecu-max-height",
    "ecu_max_height",
    type=int,
    help=get_annotation_metadata(PDFReader.parse_page, "ecu_max_height")
    + "  [default: "
    + str(PDFReader.parse_page.__kwdefaults__["ecu_max_height"])
    + "]",
)
@click.option(
    "--xor-min-height",
    "xor_min_height",
    type=int,
    help=get_annotation_metadata(PDFReader.parse_page, "xor_min_height")
    + "  [default: "
    + str(PDFReader.parse_page.__kwdefaults__["xor_min_height"])
    + "]",
)
@click.pass_context
def run(
    ctx: click.Context,
    architecture_pdf_path: Path,
    json_model: bool,
    output_file_name: str,
    ecu_min_height: int | None,
    ecu_max_height: int | None,
    xor_min_height: int | None,
    drawio_file: bool,
    export_format: str | None,
) -> None:
    """Run aranea to detect an architecture on a given PDF file.

    If you are using ``--export-format`` under Linux and EUID is 0 (root), drawio will be
    run with ``--no-sandbox``.
    If the environment variable ``CI`` is also set to ``true`` it will be run with ``xvfb-run``.
    This requires that ``xvfb`` is installed on the system.
    """

    config: Config = ctx.obj

    if not architecture_pdf_path.suffix == ".pdf":
        _logger.error("The provided file %s is not a PDF file!", architecture_pdf_path)
        sys.exit(1)

    g2d_parser: PDFReader = PDFReader(str(architecture_pdf_path))
    if ecu_min_height is None:
        ecu_min_height = config.ecu_min_height
    if ecu_max_height is None:
        ecu_max_height = config.ecu_max_height
    if xor_min_height is None:
        xor_min_height = config.xor_min_height

    graph: Graph = g2d_parser.parse_page(
        ecu_min_height=ecu_min_height, ecu_max_height=ecu_max_height, xor_min_height=xor_min_height
    )
    graph_collection: GraphCollection = GraphCollection(graphs=[graph])

    if json_model:
        graph_collection_json: str = graph_collection.model_dump_json()
        file_name: str = output_file_name + ".json"
        path: str = os.path.join(config.output_dir, file_name)
        with open(path, "w", encoding="UTF-8") as f:
            f.write(graph_collection_json)

        _logger.debug("The json model was exported to %s", path)

    if drawio_file:
        mx_file: MxFile = transform_graph_collection_to_mx_file(graph_collection)
        xml_element = mx_file.to_xml_tree()
        xml_tree: ElementTree = ElementTree(xml_element)
        path = os.path.join(config.output_dir, output_file_name + ".drawio")
        xml_tree.write(path)
        _logger.debug("The drawio file was exported to %s", path)

        if export_format is not None:
            if config.drawio_path is None:
                _logger.error("The drawio_path is not set. Aborting the export.")
                sys.exit(1)
            elif not config.drawio_path.is_file():
                _logger.error(
                    "The drawio_path %s does not exist. Aborting the export.", config.drawio_path
                )
                sys.exit(1)
            else:
                command: list[str] = [
                    str(config.drawio_path),
                    "-x",
                    "-f",
                    export_format,
                    "-o",
                    str(config.output_dir / (output_file_name + "." + export_format)),
                    path,
                ]
                # Add --no-sandbox for Linux when running as root
                if platform.system() == "Linux" and os.geteuid() == 0:
                    command.insert(1, "--no-sandbox")
                    _logger.warning("Running drawio with --no-sandbox.")
                    if os.getenv("CI") == "true":
                        _logger.debug("Running drawio with xvfb-run.")
                        command.insert(0, "xvfb-run")

                try:
                    _logger.debug("Calling: %s", " ".join(command))
                    result = subprocess.run(
                        command, check=True, text=True, capture_output=True
                    )  # nosec B603 - We are aware of possible security implications
                    # The user is responsible for the drawio_path,
                    # we can't ensure that the path to the exeutable is secure
                    _logger.debug("The drawio file was exported to %s", result.stdout)
                except subprocess.CalledProcessError as e:
                    _logger.error(
                        "An error occurred while executing the drawio export: %s", e.stderr
                    )
                    sys.exit(1)
