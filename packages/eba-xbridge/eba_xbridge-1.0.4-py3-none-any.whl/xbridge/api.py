"""API module."""

from pathlib import Path

from xbridge.converter import Converter
from xbridge.xml_instance import Instance


def convert_instance(instance_path: str, output_path: str | Path = None):
    """
    Convert one single instance of XBRL-XML file to a CSV file

    :param instance_path: Path to the XBRL-XML instance

    :param output_path: Path to the output CSV file

    :return: Converted CSV file.

    """

    converter = Converter(instance_path)
    return converter.convert(output_path)


def load_instance(instance_path: str | Path) -> Instance:
    """
    Load an XBRL XML instance file

    :param instance_path: Path to the instance XBRL file

    :return: An instance object may be return
    """

    return Instance(instance_path)
