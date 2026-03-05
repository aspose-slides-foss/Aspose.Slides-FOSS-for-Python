from __future__ import annotations
from typing import TYPE_CHECKING
from .BasePortionFormat import BasePortionFormat
from .IPortionFormat import IPortionFormat

if TYPE_CHECKING:
    from .IBasePortionFormat import IBasePortionFormat
    from .IHyperlinkContainer import IHyperlinkContainer

class PortionFormat(BasePortionFormat, IPortionFormat):
    """This class contains the text portion formatting properties. Unlike , all properties of this class are writeable."""
    def __init__(self):
        super().__init__()













