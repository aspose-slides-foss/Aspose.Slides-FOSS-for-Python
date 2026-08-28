from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .IHyperlink import IHyperlink

class IHyperlinkContainer(ABC):
    """Represents an object that can carry hyperlinks."""

    @property
    @abstractmethod
    def hyperlink_click(self) -> IHyperlink:
        """Returns or sets the hyperlink followed on a mouse click. Read/write ."""

    @hyperlink_click.setter
    @abstractmethod
    def hyperlink_click(self, value) -> None:
        ...

    @property
    @abstractmethod
    def hyperlink_mouse_over(self) -> IHyperlink:
        """Returns or sets the hyperlink followed on a mouse over. Read/write ."""

    @hyperlink_mouse_over.setter
    @abstractmethod
    def hyperlink_mouse_over(self, value) -> None:
        ...
