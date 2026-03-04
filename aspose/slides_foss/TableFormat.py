from __future__ import annotations
from typing import TYPE_CHECKING
from .ITableFormat import ITableFormat

if TYPE_CHECKING:
    from .IFillFormat import IFillFormat
    from .ITableFormatEffectiveData import ITableFormatEffectiveData

class TableFormat(ITableFormat):
    """Represents format of a table."""

    def _init_internal(self, tbl_pr_element, slide_part, parent_slide):
        self._tbl_pr_element = tbl_pr_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        return self

    @property
    def fill_format(self) -> IFillFormat:
        """Returns a table fill properties object. Read-only ."""
        if not hasattr(self, '_tbl_pr_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .FillFormat import FillFormat
        ff = FillFormat()
        ff._init_internal(self._tbl_pr_element, self._slide_part, self._parent_slide)
        return ff



