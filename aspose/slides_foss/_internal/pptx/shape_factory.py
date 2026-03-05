"""
Shape factory for creating the correct shape type from XML elements.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .constants import NS

if TYPE_CHECKING:
    from ...IShape import IShape
    from .slide_part import SlidePart


def create_shape(xml_element: ET._Element, slide_part: 'SlidePart', parent_slide) -> Optional['IShape']:
    """
    Create the appropriate shape object based on the XML element type.

    Args:
        xml_element: The XML element representing the shape
        slide_part: The SlidePart containing the slide XML
        parent_slide: The parent Slide object

    Returns:
        An instance of the appropriate shape subclass, or None if unknown
    """
    tag = xml_element.tag

    # Import here to avoid circular dependencies
    from ...AutoShape import AutoShape
    from ...PictureFrame import PictureFrame
    from ...GroupShape import GroupShape
    from ...Connector import Connector
    from ...Table import Table
    try:
        from ...charts.Chart import Chart
    except ImportError:
        Chart = None
    try:
        from ...smartart.SmartArt import SmartArt
    except ImportError:
        SmartArt = None

    shape = None

    # Determine shape type based on XML tag
    if tag == f"{NS.P}sp":
        # Shape (AutoShape)
        shape = AutoShape()
    elif tag == f"{NS.P}pic":
        # Picture frame
        shape = PictureFrame()
    elif tag == f"{NS.P}grpSp":
        # Group shape
        shape = GroupShape()
    elif tag == f"{NS.P}cxnSp":
        # Connector
        shape = Connector()
    elif tag == f"{NS.P}graphicFrame":
        # GraphicFrame can be Table, Chart, SmartArt, etc.
        # Need to inspect the graphicData to determine the actual type
        shape = _create_graphical_object(xml_element, slide_part, parent_slide)
        if shape is not None:
            return shape

    # Initialize the shape with internal data if created
    if shape is not None and hasattr(shape, '_init_internal'):
        shape._init_internal(xml_element, slide_part, parent_slide)

    return shape


def _create_graphical_object(xml_element: ET._Element, slide_part: 'SlidePart', parent_slide) -> Optional['IShape']:
    """
    Create the appropriate graphical object (Table, Chart, SmartArt) from a graphicFrame element.

    Args:
        xml_element: The graphicFrame XML element
        slide_part: The SlidePart containing the slide XML
        parent_slide: The parent Slide object

    Returns:
        An instance of Table, Chart, SmartArt, or None
    """
    from ...Table import Table
    try:
        from ...charts.Chart import Chart
    except ImportError:
        Chart = None
    try:
        from ...smartart.SmartArt import SmartArt
    except ImportError:
        SmartArt = None

    # Find the graphicData element
    graphic_data = xml_element.find(f".//{NS.A}graphicData")
    if graphic_data is None:
        return None

    # Check the URI to determine the type
    uri = graphic_data.get('uri', '')

    shape = None
    if 'table' in uri.lower():
        shape = Table()
    elif 'chart' in uri.lower():
        if Chart is not None:
            shape = Chart()
    elif 'smartart' in uri.lower() or 'diagram' in uri.lower():
        if SmartArt is not None:
            shape = SmartArt()

    # Initialize the shape with internal data if created
    if shape is not None and hasattr(shape, '_init_internal'):
        shape._init_internal(xml_element, slide_part, parent_slide)

    return shape
