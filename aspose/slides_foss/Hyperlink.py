from __future__ import annotations
from .IHyperlink import IHyperlink


class Hyperlink(IHyperlink):
    """Represents a hyperlink to an external target."""

    def __init__(self, external_url: str, tooltip: str = None, target_frame: str = None):
        self._external_url = external_url or ''
        self._tooltip = tooltip
        self._target_frame = target_frame

    @property
    def external_url(self) -> str:
        """Returns the target URL of the hyperlink. Read-only ."""
        return self._external_url

    @property
    def tooltip(self) -> str:
        """Returns the text shown when the pointer rests on the link. Read-only ."""
        return self._tooltip

    @property
    def target_frame(self) -> str:
        """Returns the frame the link opens in. Read-only ."""
        return self._target_frame

    def __eq__(self, other) -> bool:
        if isinstance(other, Hyperlink):
            return (self._external_url == other._external_url
                    and self._tooltip == other._tooltip
                    and self._target_frame == other._target_frame)
        if isinstance(other, str):
            return self._external_url == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._external_url, self._tooltip, self._target_frame))

    def __repr__(self) -> str:
        return 'Hyperlink(%r)' % self._external_url

    def __str__(self) -> str:
        return self._external_url
