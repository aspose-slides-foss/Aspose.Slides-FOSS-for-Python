from __future__ import annotations
from abc import ABC, abstractmethod


class IHyperlink(ABC):
    """Represents a hyperlink."""

    @property
    @abstractmethod
    def external_url(self) -> str:
        """Returns the target URL of the hyperlink. Read-only ."""

    @property
    @abstractmethod
    def tooltip(self) -> str:
        """Returns the text shown when the pointer rests on the link. Read-only ."""

    @property
    @abstractmethod
    def target_frame(self) -> str:
        """Returns the frame the link opens in. Read-only ."""
