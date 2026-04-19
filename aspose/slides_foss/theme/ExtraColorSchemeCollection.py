from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IExtraColorSchemeCollection import IExtraColorSchemeCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import NS

if TYPE_CHECKING:
    from .ExtraColorScheme import ExtraColorScheme
    from .._internal.pptx.theme_part import ThemePart


class ExtraColorSchemeCollection(BaseCollection, IExtraColorSchemeCollection):
    """Represents a collection of additional color schemes."""

    def _init_internal(self, extra_clr_scheme_lst, theme_part: ThemePart, presentation) -> None:
        self._extra_clr_scheme_lst = extra_clr_scheme_lst
        self._theme_part = theme_part
        self._presentation_ref = presentation
        self._items: list = []
        self._parse()

    def _parse(self) -> None:
        if self._extra_clr_scheme_lst is None:
            return
        from .ExtraColorScheme import ExtraColorScheme as ECS
        for child in self._extra_clr_scheme_lst:
            ecs = ECS()
            ecs._init_internal(child, self._theme_part, self._presentation_ref)
            self._items.append(ecs)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> ExtraColorScheme:
        return self._items[index]

    @property
    def as_i_collection(self) -> list:
        return list(self)

    @property
    def as_i_enumerable(self) -> Any:
        return self
