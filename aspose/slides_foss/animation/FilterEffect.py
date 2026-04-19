from __future__ import annotations
from typing import TYPE_CHECKING
from .Behavior import Behavior
from .IBehavior import IBehavior
from .IFilterEffect import IFilterEffect

if TYPE_CHECKING:
    from .FilterEffectRevealType import FilterEffectRevealType
    from .FilterEffectType import FilterEffectType
    from .FilterEffectSubtype import FilterEffectSubtype


class FilterEffect(Behavior, IFilterEffect):
    """Represent filter effect behavior of effect."""

    def __init__(self):
        self._reveal_val = None
        self._type_val = None
        self._subtype_val = None

    @property
    def reveal(self) -> FilterEffectRevealType:
        from .FilterEffectRevealType import FilterEffectRevealType
        return self._reveal_val or FilterEffectRevealType.NOT_DEFINED

    @reveal.setter
    def reveal(self, value: FilterEffectRevealType):
        self._reveal_val = value

    @property
    def type(self) -> FilterEffectType:
        from .FilterEffectType import FilterEffectType
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('transition')
            if val == 'in':
                self._reveal_val = None  # Not filter type
            filt = self._elem.get('filter', '')
            # Map filter string to FilterEffectType
            _map = {
                'barn': FilterEffectType.BARN, 'blinds': FilterEffectType.BLINDS,
                'box': FilterEffectType.BOX, 'checkerboard': FilterEffectType.CHECKERBOARD,
                'circle': FilterEffectType.CIRCLE, 'diamond': FilterEffectType.DIAMOND,
                'dissolve': FilterEffectType.DISSOLVE, 'fade': FilterEffectType.FADE,
                'plus': FilterEffectType.PLUS, 'slide': FilterEffectType.SLIDE,
                'strips': FilterEffectType.STRIPS, 'wedge': FilterEffectType.WEDGE,
                'wheel': FilterEffectType.WHEEL, 'wipe': FilterEffectType.WIPE,
            }
            base = filt.split('(')[0].strip() if filt else ''
            return _map.get(base, FilterEffectType.NONE)
        return self._type_val or FilterEffectType.NONE

    @type.setter
    def type(self, value: FilterEffectType):
        self._type_val = value

    @property
    def subtype(self) -> FilterEffectSubtype:
        from .FilterEffectSubtype import FilterEffectSubtype
        return self._subtype_val or FilterEffectSubtype.NONE

    @subtype.setter
    def subtype(self, value: FilterEffectSubtype):
        self._subtype_val = value

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
