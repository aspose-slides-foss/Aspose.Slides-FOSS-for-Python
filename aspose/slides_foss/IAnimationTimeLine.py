from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .animation.ISequence import ISequence
    from .animation.ISequenceCollection import ISequenceCollection
    from .animation.ITextAnimationCollection import ITextAnimationCollection

class IAnimationTimeLine(ABC):
    """Represents timeline of animation."""
    @property
    @abstractmethod
    def interactive_sequences(self) -> ISequenceCollection:
        """Returns collection of interactive sequences. This sequences may contain only effects by "click on shape" with specifies target shape. Read-only ."""
        ...

    @property
    @abstractmethod
    def main_sequence(self) -> ISequence:
        """Returns main sequence which may contain only main effects collection. Read-only ."""
        ...

    @property
    @abstractmethod
    def text_animation_collection(self) -> ITextAnimationCollection:
        """Returns collection of text animations. Read-only ."""
        ...

