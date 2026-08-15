from __future__ import annotations
from typing import TYPE_CHECKING
from .BasePortionFormat import BasePortionFormat
from .IPortionFormat import IPortionFormat
from ._internal.pptx.constants import Elements
from ._internal.pptx.hyperlinks import get_hyperlink, set_hyperlink

if TYPE_CHECKING:
    from .IBasePortionFormat import IBasePortionFormat
    from .IHyperlink import IHyperlink
    from .IHyperlinkContainer import IHyperlinkContainer

class PortionFormat(BasePortionFormat, IPortionFormat):
    """This class contains the text portion formatting properties. Unlike , all properties of this class are writeable."""
    def __init__(self):
        super().__init__()

    @property
    def hyperlink_click(self) -> IHyperlink:
        """Returns or sets the hyperlink followed on a mouse click. Read/write ."""
        return get_hyperlink(self._rpr_element, self._slide_part, Elements.A_HLINK_CLICK)

    @hyperlink_click.setter
    def hyperlink_click(self, value):
        set_hyperlink(self._rpr_element, self._slide_part, Elements.A_HLINK_CLICK, value)
        self._save()

    @property
    def hyperlink_mouse_over(self) -> IHyperlink:
        """Returns or sets the hyperlink followed on a mouse over. Read/write ."""
        return get_hyperlink(self._rpr_element, self._slide_part, Elements.A_HLINK_MOUSE_OVER)

    @hyperlink_mouse_over.setter
    def hyperlink_mouse_over(self, value):
        set_hyperlink(self._rpr_element, self._slide_part, Elements.A_HLINK_MOUSE_OVER, value)
        self._save()
