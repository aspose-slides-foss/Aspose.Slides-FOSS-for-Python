from __future__ import annotations
from .ITransitionValueBase import ITransitionValueBase

class TransitionValueBase(ITransitionValueBase):
    """Base class for slide transition effects."""

    def __init__(self):
        self._element = None
        self._slide_part = None

    def _init_internal(self, element, slide_part):
        """Initialize with the transition child XML element and slide part."""
        self._element = element
        self._slide_part = slide_part
