"""
Mermaid specific extensions for ChartStag
"""
import os
from zipfile import ZipFile


def get_mermaid_version() -> str:
    """
    Returns the mermaid version being used

    :return: The version number as string
    """
    return "9.3.0"


def get_mermaid_script() -> bytes:
    """
    Returns the mermaid code as single file JavaScript

    :return: Returns the mermaid code
    """
    path = os.path.dirname(__file__) + "/data/mermaid_min.zip"
    archive = ZipFile(path, "r")
    return archive.read("mermaid.min.js")
