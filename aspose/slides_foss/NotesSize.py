from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .INotesSize import INotesSize

if TYPE_CHECKING:
    from ._internal.pptx.presentation_part import PresentationPart

# 1 point = 12700 EMUs
_EMU_PER_POINT = 12700


class NotesSize(INotesSize):
    """Represents a size of notes slide."""

    def __init__(self):
        self._presentation_part: PresentationPart = None

    def _init_internal(self, presentation_part: PresentationPart) -> None:
        """
        Internal initialization.

        Args:
            presentation_part: The PresentationPart providing access to notesSz in XML.
        """
        self._presentation_part = presentation_part

    @property
    def size(self) -> Any:
        """Returns or sets the size in points. Read/write ."""
        from .drawing import SizeF
        cx, cy = self._presentation_part.get_notes_size()
        return SizeF(
            width=cx / _EMU_PER_POINT,
            height=cy / _EMU_PER_POINT
        )

    @size.setter
    def size(self, value: Any):
        cx = int(value.width * _EMU_PER_POINT)
        cy = int(value.height * _EMU_PER_POINT)
        self._presentation_part.set_notes_size(cx, cy)
