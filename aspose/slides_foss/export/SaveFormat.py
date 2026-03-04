from __future__ import annotations
from enum import Enum

class SaveFormat(Enum):
    """Constants which define the format of a saved presentation."""
    PPT = 'Ppt'  # Save presentation in PPT format.
    PDF = 'Pdf'  # Save presentation in PDF format.
    XPS = 'Xps'  # Save presentation in XPS format.
    PPTX = 'Pptx'  # Save presentation in PPTX format.
    PPSX = 'Ppsx'  # Save presentation in PPSX (slideshow) format.
    TIFF = 'Tiff'  # Save presentation as multi-page TIFF image.
    ODP = 'Odp'  # Save presentation in ODP format.
    PPTM = 'Pptm'  # Save presentation in PPTM (macro-enabled presentation) format.
    PPSM = 'Ppsm'  # Save presentation in PPSM (macro-enabled slideshow) format.
    POTX = 'Potx'  # Save presentation in POTX (template) format.
    POTM = 'Potm'  # Save presentation in POTM (macro-enabled template) format.
    HTML = 'Html'  # Save presentation in HTML format.
    SWF = 'Swf'  # Save presentation in SWF format.
    OTP = 'Otp'  # Save presentation in OTP (presentation template) format.
    PPS = 'Pps'  # Save presentation in PPS format.
    POT = 'Pot'  # Save presentation in POT format.
    FODP = 'Fodp'  # Save presentation in FODP format.
    GIF = 'Gif'  # Save presentation in GIF format.
    HTML5 = 'Html5'  # Save presentation in HTML format using new HTML5 templating system.
    MD = 'Md'  # Save presentation in Markdown format
    XML = 'Xml'  # Save presentation in PowerPoint XML Presentation format.
