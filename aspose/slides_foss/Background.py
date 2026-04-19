from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .IBackground import IBackground
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .BackgroundType import BackgroundType
    from .IBackgroundEffectiveData import IBackgroundEffectiveData
    from .IColorFormat import IColorFormat
    from .IEffectFormat import IEffectFormat
    from .IFillFormat import IFillFormat
    from .ISlideComponent import ISlideComponent
    from .IFillParamSource import IFillParamSource
    from ._internal.pptx.slide_part import SlidePart


class Background(PVIObject, IBackground):
    """Represents background of a slide."""

    def _init_internal(self, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization.

        Args:
            slide_part: The SlidePart (or LayoutSlidePart / MasterSlidePart).
            parent_slide: The parent slide object.
        """
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._fill_format_cache = None
        self._effect_format_cache = None
        self._style_color_cache = None

    # ------------------------------------------------------------------
    # XML helpers
    # ------------------------------------------------------------------

    def _get_csld(self) -> ET._Element:
        """Return the <p:cSld> element."""
        return self._slide_part._root.find(Elements.C_SLD)

    def _get_bg(self) -> ET._Element | None:
        """Return the <p:bg> element or None."""
        csld = self._get_csld()
        if csld is not None:
            return csld.find(Elements.P_BG)
        return None

    def _get_or_create_bg(self) -> ET._Element:
        """Get or create <p:bg> as first child of <p:cSld>."""
        csld = self._get_csld()
        bg = csld.find(Elements.P_BG)
        if bg is None:
            bg = ET.Element(Elements.P_BG)
            # <p:bg> must be first child of <p:cSld> (before <p:spTree>)
            csld.insert(0, bg)
        return bg

    def _get_bgpr(self) -> ET._Element | None:
        """Return the <p:bgPr> element or None."""
        bg = self._get_bg()
        if bg is not None:
            return bg.find(Elements.P_BG_PR)
        return None

    def _get_or_create_bgpr(self) -> ET._Element:
        """Get or create <p:bgPr> inside <p:bg>, removing any <p:bgRef>."""
        bg = self._get_or_create_bg()
        bgpr = bg.find(Elements.P_BG_PR)
        if bgpr is None:
            # Remove bgRef if present
            bgref = bg.find(Elements.P_BG_REF)
            if bgref is not None:
                bg.remove(bgref)
            bgpr = ET.SubElement(bg, Elements.P_BG_PR)
        return bgpr

    def _get_bgref(self) -> ET._Element | None:
        """Return the <p:bgRef> element or None."""
        bg = self._get_bg()
        if bg is not None:
            return bg.find(Elements.P_BG_REF)
        return None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def type(self) -> BackgroundType:
        """Returns a type of background fill. Read/write."""
        from .BackgroundType import BackgroundType
        bg = self._get_bg()
        if bg is None:
            return BackgroundType.NOT_DEFINED
        if bg.find(Elements.P_BG_PR) is not None:
            return BackgroundType.OWN_BACKGROUND
        if bg.find(Elements.P_BG_REF) is not None:
            return BackgroundType.THEMED
        return BackgroundType.NOT_DEFINED

    @type.setter
    def type(self, value: BackgroundType):
        from .BackgroundType import BackgroundType
        if value == BackgroundType.OWN_BACKGROUND:
            self._get_or_create_bgpr()
            # Invalidate caches since the element changed
            self._fill_format_cache = None
            self._effect_format_cache = None
        elif value == BackgroundType.THEMED:
            bg = self._get_or_create_bg()
            # Remove bgPr if present
            bgpr = bg.find(Elements.P_BG_PR)
            if bgpr is not None:
                bg.remove(bgpr)
            # Create bgRef if not present
            if bg.find(Elements.P_BG_REF) is None:
                bgref = ET.SubElement(bg, Elements.P_BG_REF, idx="0")
                ET.SubElement(bgref, Elements.A_SCHEME_CLR, val="accent1")
            self._fill_format_cache = None
            self._effect_format_cache = None
            self._style_color_cache = None
        elif value == BackgroundType.NOT_DEFINED:
            bg = self._get_bg()
            if bg is not None:
                csld = self._get_csld()
                csld.remove(bg)
            self._fill_format_cache = None
            self._effect_format_cache = None
            self._style_color_cache = None
        self._slide_part.save()

    @property
    def fill_format(self) -> IFillFormat:
        """Returns a FillFormat for BackgroundType.OwnBackground fill. Read-only."""
        if self._fill_format_cache is None:
            from .FillFormat import FillFormat
            bgpr = self._get_or_create_bgpr()
            ff = FillFormat()
            ff._init_internal(bgpr, self._slide_part, self._parent_slide)
            self._fill_format_cache = ff
        return self._fill_format_cache

    @property
    def effect_format(self) -> IEffectFormat:
        """Returns a EffectFormat for BackgroundType.OwnBackground fill. Read-only."""
        if self._effect_format_cache is None:
            from .EffectFormat import EffectFormat
            bgpr = self._get_or_create_bgpr()
            ef = EffectFormat()
            ef._init_internal(bgpr, self._slide_part, self._parent_slide)
            self._effect_format_cache = ef
        return self._effect_format_cache

    @property
    def style_color(self) -> IColorFormat:
        """Return a ColorFormat for a BackgroundType.Themed fill. Read-only."""
        if self._style_color_cache is None:
            from .ColorFormat import ColorFormat
            bgref = self._get_bgref()
            if bgref is not None:
                cf = ColorFormat()
                cf._init_internal(bgref, self._slide_part, self._parent_slide)
                self._style_color_cache = cf
            else:
                # Return a ColorFormat pointing at a dummy element
                bg = self._get_or_create_bg()
                bgref = bg.find(Elements.P_BG_REF)
                if bgref is None:
                    bgref = ET.SubElement(bg, Elements.P_BG_REF, idx="0")
                cf = ColorFormat()
                cf._init_internal(bgref, self._slide_part, self._parent_slide)
                self._style_color_cache = cf
        return self._style_color_cache

    @property
    def style_index(self) -> int:
        """Returns an index of BackgroundType.Themed fill in background theme collection.

        In OOXML, bgRef/@idx 1-999 references fillStyleLst while 1001+
        references bgFillStyleLst.  The public API exposes 1-based indices
        into the background fill styles, so idx 1001 maps to style_index 1,
        idx 1002 to style_index 2, etc.
        """
        bgref = self._get_bgref()
        if bgref is not None:
            idx = int(bgref.get('idx', '0'))
            if idx >= 1001:
                return idx - 1000
            return idx
        return 0

    @style_index.setter
    def style_index(self, value: int):
        bg = self._get_or_create_bg()
        # Remove bgPr if present — style_index implies themed background
        bgpr = bg.find(Elements.P_BG_PR)
        if bgpr is not None:
            bg.remove(bgpr)
        bgref = bg.find(Elements.P_BG_REF)
        if bgref is None:
            bgref = ET.SubElement(bg, Elements.P_BG_REF)
            ET.SubElement(bgref, f"{NS.A}schemeClr", val="bg1")
        # Map 1-based background style index to OOXML idx (1001+)
        bgref.set('idx', str(value + 1000))
        self._fill_format_cache = None
        self._effect_format_cache = None
        self._style_color_cache = None
        self._slide_part.save()

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_fill_param_source(self) -> IFillParamSource:
        return self

    def get_effective(self) -> IBackgroundEffectiveData:
        """Returns effective background data, resolving inheritance from layout/master."""
        from .BackgroundType import BackgroundType
        from ._internal.background_effective import BackgroundEffectiveData

        # Check this slide's own background first
        if self.type == BackgroundType.OWN_BACKGROUND:
            return BackgroundEffectiveData(self._get_bgpr(), self._slide_part, self._parent_slide)

        # For themed backgrounds, try to resolve from bgRef
        if self.type == BackgroundType.THEMED:
            bgref = self._get_bgref()
            return BackgroundEffectiveData(bgref, self._slide_part, self._parent_slide)

        # If NOT_DEFINED, walk up the inheritance chain: layout → master
        parent_slide = self._parent_slide
        # Try layout slide
        if hasattr(parent_slide, 'layout_slide') and parent_slide.layout_slide is not None:
            layout = parent_slide.layout_slide
            if hasattr(layout, '_background_cache') and layout._background_cache is not None:
                layout_bg = layout._background_cache
            else:
                layout_bg = layout.background
            if layout_bg.type != BackgroundType.NOT_DEFINED:
                return layout_bg.get_effective()

        # Try master slide
        master = None
        if hasattr(parent_slide, 'layout_slide') and parent_slide.layout_slide is not None:
            master = parent_slide.layout_slide.master_slide
        elif hasattr(parent_slide, 'master_slide'):
            master = getattr(parent_slide, 'master_slide', None)

        if master is not None:
            master_bg = master.background
            if master_bg.type != BackgroundType.NOT_DEFINED:
                return master_bg.get_effective()

        # Fallback: return effective data from this slide (will show NOT_DEFINED fill)
        return BackgroundEffectiveData(None, self._slide_part, self._parent_slide)
