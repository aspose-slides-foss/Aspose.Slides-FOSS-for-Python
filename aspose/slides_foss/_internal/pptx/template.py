"""
PPTX template loading.

Loads the Template.pptx file for new presentations.
"""

from __future__ import annotations
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..opc import OpcPackage

# Path to the template file (in the same directory as this module)
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'Template.pptx')


def get_template_path() -> str:
    """
    Get the path to the Template.pptx file.

    Returns:
        Absolute path to Template.pptx.

    Raises:
        FileNotFoundError: If template file doesn't exist.
    """
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(
            f"Template.pptx not found at {TEMPLATE_PATH}. "
            "Please ensure the template file exists."
        )
    return TEMPLATE_PATH


def load_template(package: 'OpcPackage') -> None:
    """
    Load the Template.pptx into the given package.

    Args:
        package: The OPC package to populate with template contents.

    Raises:
        FileNotFoundError: If Template.pptx doesn't exist.
    """
    template_path = get_template_path()

    # Use the same class as the passed package to open the template
    template_package = type(package).open(template_path)

    # Copy all parts from template to the target package
    for part_name in template_package.get_part_names():
        content = template_package.get_part(part_name)
        package.set_part(part_name, content)


# Alias for backward compatibility
create_minimal_pptx = load_template
