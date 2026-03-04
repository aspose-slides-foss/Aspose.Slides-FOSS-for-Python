from __future__ import annotations
from typing import TYPE_CHECKING
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .ICellFormat import ICellFormat

if TYPE_CHECKING:
    from .ICellFormatEffectiveData import ICellFormatEffectiveData
    from .IFillFormat import IFillFormat
    from .ILineFormat import ILineFormat

class CellFormat(PVIObject, ISlideComponent, IPresentationComponent, ICellFormat):
    """Represents format of a table cell."""

    def _init_internal(self, tc_pr_element, slide_part, parent_slide):
        self._tc_pr_element = tc_pr_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    @property
    def fill_format(self) -> IFillFormat:
        """Returns a cell fill properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .FillFormat import FillFormat
        ff = FillFormat()
        ff._init_internal(self._tc_pr_element, self._slide_part, self._parent_slide)
        return ff

    def _get_border(self, ln_tag: str) -> ILineFormat:
        """Get a border LineFormat for the given border element tag."""
        from .LineFormat import LineFormat
        lf = LineFormat()
        lf._init_internal(self._tc_pr_element, self._slide_part, self._parent_slide, ln_tag=ln_tag)
        return lf

    @property
    def border_left(self) -> ILineFormat:
        """Returns a left border line properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        return self._get_border(Elements.A_LN_L)

    @property
    def border_top(self) -> ILineFormat:
        """Returns a top border line properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        return self._get_border(Elements.A_LN_T)

    @property
    def border_right(self) -> ILineFormat:
        """Returns a right border line properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        return self._get_border(Elements.A_LN_R)

    @property
    def border_bottom(self) -> ILineFormat:
        """Returns a bottom border line properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        return self._get_border(Elements.A_LN_B)

    @property
    def border_diagonal_down(self) -> ILineFormat:
        """Returns a top-left to bottom-right diagonal line properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        return self._get_border(Elements.A_LN_TL_TO_BR)

    @property
    def border_diagonal_up(self) -> ILineFormat:
        """Returns a bottom-left to top-right diagonal line properties object. Read-only ."""
        if not hasattr(self, '_tc_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from ._internal.pptx.constants import Elements
        return self._get_border(Elements.A_LN_BL_TO_TR)



