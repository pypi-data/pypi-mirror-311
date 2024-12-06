"""
Module for creating image strings for custom icons in drawio.
"""

from pathlib import Path

from mako.template import Template

from aranea.models.custom_xml_shapes.custom_xml_shapes_utils import (
    get_mx_cell_image_str, is_valid_hex_color)


class IconFactory:
    """
    Class for creating image strings for custom icons in drawio.
    """

    def __init__(self):
        # get path to this file so that absolute paths to the templates can be constructed
        path_to_parent = Path(__file__).parent
        # create templates
        path_to_amg_template = path_to_parent / "icons/amg_icon.mako"
        if not path_to_amg_template.exists():
            raise FileNotFoundError(f"The file {path_to_amg_template} does not exist")
        self.__amg_template = Template(
            filename=str(path_to_amg_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_analog_broadcast_template = path_to_parent / "icons/analog_broadcast_icon.mako"
        if not path_to_analog_broadcast_template.exists():
            raise FileNotFoundError(f"The file {path_to_analog_broadcast_template} does not exist")
        self.__analog_broadcast_template = Template(
            filename=str(path_to_analog_broadcast_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_backend_template = path_to_parent / "icons/backend_icon.mako"
        if not path_to_backend_template.exists():
            raise FileNotFoundError(f"The file {path_to_backend_template} does not exist")
        self.__backend_template = Template(
            filename=str(path_to_backend_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_bluetooth_template = path_to_parent / "icons/bluetooth_icon.mako"
        if not path_to_bluetooth_template.exists():
            raise FileNotFoundError(f"The file {path_to_bluetooth_template} does not exist")
        self.__bluetooth_template = Template(
            filename=str(path_to_bluetooth_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_car_charger_template = path_to_parent / "icons/car_charger_icon.mako"
        if not path_to_car_charger_template.exists():
            raise FileNotFoundError(f"The file {path_to_car_charger_template} does not exist")
        self.__car_charger_template = Template(
            filename=str(path_to_car_charger_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_cellular_template = path_to_parent / "icons/cellular_icon.mako"
        if not path_to_cellular_template.exists():
            raise FileNotFoundError(f"The file {path_to_cellular_template} does not exist")
        self.__cellular_template = Template(
            filename=str(path_to_cellular_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_digital_broadcast_template = path_to_parent / "icons/digital_broadcast_icon.mako"
        if not path_to_digital_broadcast_template.exists():
            raise FileNotFoundError(f"The file {path_to_digital_broadcast_template} does not exist")
        self.__digital_broadcast_template = (
            Template(  # nosec use_of_mako_templates - implemented recommended practice
                filename=str(path_to_digital_broadcast_template), default_filters=["escape"]
            )
        )

        path_to_network_switch_template = path_to_parent / "icons/network_switch_icon.mako"
        if not path_to_network_switch_template.exists():
            raise FileNotFoundError(f"The file {path_to_network_switch_template} does not exist")
        self.__network_switch_template = Template(
            filename=str(path_to_network_switch_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_nfc_template = path_to_parent / "icons/nfc_icon.mako"
        if not path_to_nfc_template.exists():
            raise FileNotFoundError(f"The file {path_to_nfc_template} does not exist")
        self.__nfc_template = Template(
            filename=str(path_to_nfc_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_satellite_template = path_to_parent / "icons/satellite_icon.mako"
        if not path_to_satellite_template.exists():
            raise FileNotFoundError(f"The file {path_to_satellite_template} does not exist")
        self.__satellite_template = Template(
            filename=str(path_to_satellite_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_usb_template = path_to_parent / "icons/usb_icon.mako"
        if not path_to_usb_template.exists():
            raise FileNotFoundError(f"The file {path_to_usb_template} does not exist")
        self.__usb_template = Template(
            filename=str(path_to_usb_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

        path_to_wifi_template = path_to_parent / "icons/wifi_icon.mako"
        if not path_to_wifi_template.exists():
            raise FileNotFoundError(f"The file {path_to_wifi_template} does not exist")
        self.__wifi_template = Template(
            filename=str(path_to_wifi_template), default_filters=["escape"]
        )  # nosec use_of_mako_templates - implemented recommended practice

    def get_amg_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of an AMG icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: AMG icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__amg_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_analog_broadcast_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of an Analog Broadcast icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: analog broadcast icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__analog_broadcast_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_backend_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of a Backend icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: backend icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__backend_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_bluetooth_icon_image_str(
        self, color_rune: str = "#f9fafb", color_border: str = "#043c94"
    ) -> str:
        """
        Method for getting the image string for the MxCell style of a Bluetooth icon.

        :param color_rune: Color of the "B"-Rune in the icon in hex format
        :type color: str
        :param color_border: Color of the border in the icon in hex format
        :type color: str

        :return: bluetooth icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color_rune) or not is_valid_hex_color(color_border):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__bluetooth_template.render(
            color_rune=color_rune, color_border=color_border
        )
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_car_charger_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of a Car Charger icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: car charger icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__car_charger_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_cellular_icon_image_str(
        self, color_body: str = "#000000", color_screen: str = "#ffffff"
    ) -> str:
        """
        Method for getting the image string for the MxCell style of a Cellular icon.

        :param color_body: Color of the body of the cellphone icon in hex format
        :type color_body: str
        :param color_screen: Color of the screen of the cellphone icon in hex format
        :type color_screen: str

        :return: cellular icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color_body) or not is_valid_hex_color(color_screen):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__cellular_template.render(
            color_body=color_body, color_screen=color_screen
        )
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_digital_broadcast_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of a Digital Broadcast (DAB) icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: digital broadcast icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__digital_broadcast_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_network_switch_icon_image_str(
        self,
        color_eth: str = "#051205",
        color_eth_border: str = "#9b9b9c",
        color_back: str = "#0433fc",
        color_front: str = "#0448fb",
    ) -> str:
        """
        Method for getting the image string for the MxCell style of a Network Switch icon.

        :param color_eth: Color of the Ethernet ports in the icon in hex format
        :type color_eth: str
        :param color_eth_border: Color of the Ethernet ports border in the icon in hex format
        :type color_eth_border: str
        :param color_back: Color of the back of the icon in hex format
        :type color_back: str
        :param color_front: Color of the front of the icon in hex format
        :type color_front: str

        :return: network switch icon image string for MxCell style
        :rtype: str
        """
        if (
            not is_valid_hex_color(color_eth)
            or not is_valid_hex_color(color_eth_border)
            or not is_valid_hex_color(color_back)
            or not is_valid_hex_color(color_front)
        ):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__network_switch_template.render(
            color_eth=color_eth,
            color_eth_border=color_eth_border,
            color_back=color_back,
            color_front=color_front,
        )
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_nfc_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of an NFC icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: NFC icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__nfc_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_satellite_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of a Satellite icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: satellite icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__satellite_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_usb_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of a USB icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: USB icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__usb_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str

    def get_wifi_icon_image_str(self, color: str = "#000000") -> str:
        """
        Method for getting the image string for the MxCell style of a WiFi icon.

        :param color: Color of the icon in hex format
        :type color: str

        :return: WiFi icon image string for MxCell style
        :rtype: str
        """
        if not is_valid_hex_color(color):
            raise ValueError("Expected a valid hex color argument string")

        svg_str: str = self.__wifi_template.render(color=color)
        encoded_image_str: str = get_mx_cell_image_str(svg_str)

        return encoded_image_str
