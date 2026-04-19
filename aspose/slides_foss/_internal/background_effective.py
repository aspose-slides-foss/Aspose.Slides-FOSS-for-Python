"""
BackgroundEffectiveData — resolved/effective background properties.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from ..IBackgroundEffectiveData import IBackgroundEffectiveData
from ..IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .pptx.slide_part import SlidePart


class _FillFormatEffective:
    """Lightweight effective fill format that reads directly from a bg element."""

    def __init__(self, parent_element, slide_part, parent_slide):
        from ..FillFormat import FillFormat
        self._ff = FillFormat()
        if parent_element is not None:
            self._ff._init_internal(parent_element, slide_part, parent_slide)
        else:
            # No background — create with a dummy element
            dummy = ET.Element("dummy")
            self._ff._init_internal(dummy, slide_part, parent_slide)

    @property
    def fill_type(self):
        return self._ff.fill_type

    @property
    def solid_fill_color(self):
        """Return the solid fill color (as a Color object for effective data)."""
        from ..FillType import FillType
        if self._ff.fill_type == FillType.SOLID:
            color_format = self._ff.solid_fill_color
            return color_format.color
        return None

    @property
    def gradient_format(self):
        return self._ff.gradient_format

    @property
    def pattern_format(self):
        return self._ff.pattern_format

    @property
    def picture_fill_format(self):
        return self._ff.picture_fill_format

    @property
    def rotate_with_shape(self):
        return False

    @property
    def as_i_fill_param_source(self):
        return self


class _EffectFormatEffective:
    """Lightweight effective effect format."""

    def __init__(self, parent_element, slide_part, parent_slide):
        from ..EffectFormat import EffectFormat
        self._ef = EffectFormat()
        if parent_element is not None:
            self._ef._init_internal(parent_element, slide_part, parent_slide)
        else:
            dummy = ET.Element("dummy")
            self._ef._init_internal(dummy, slide_part, parent_slide)


class BackgroundEffectiveData(IBackgroundEffectiveData):
    """Immutable object which contains effective background properties."""

    def __init__(self, bg_element, slide_part: SlidePart, parent_slide):
        self._bg_element = bg_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    @property
    def fill_format(self):
        return _FillFormatEffective(self._bg_element, self._slide_part, self._parent_slide)

    @property
    def effect_format(self):
        return _EffectFormatEffective(self._bg_element, self._slide_part, self._parent_slide)

    @property
    def as_i_fill_param_source(self) -> IFillParamSource:
        return self
