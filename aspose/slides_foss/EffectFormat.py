from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IEffectFormat import IEffectFormat
from .IEffectParamSource import IEffectParamSource
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT

if TYPE_CHECKING:
    from .effects.IBlur import IBlur
    from .IEffectFormatEffectiveData import IEffectFormatEffectiveData
    from .effects.IFillOverlay import IFillOverlay
    from .effects.IGlow import IGlow
    from .effects.IInnerShadow import IInnerShadow
    from .effects.IOuterShadow import IOuterShadow
    from .effects.IPresetShadow import IPresetShadow
    from .effects.IReflection import IReflection
    from .effects.ISoftEdge import ISoftEdge
    from ._internal.pptx.slide_part import SlidePart

# OOXML effectLst child order
_EFFECT_LST_ORDER = [
    Elements.A_BLUR,
    Elements.A_FILL_OVERLAY,
    Elements.A_GLOW,
    Elements.A_INNER_SHDW,
    Elements.A_OUTER_SHDW,
    Elements.A_PRST_SHDW,
    Elements.A_REFLECTION,
    Elements.A_SOFT_EDGE,
]


class EffectFormat(PVIObject, ISlideComponent, IPresentationComponent, IEffectFormat, IEffectParamSource):
    """Represents effect properties of shape."""

    def _init_internal(self, parent_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization.

        Args:
            parent_element: The XML element that may contain <a:effectLst>
                (e.g., <p:spPr>).
            slide_part: The SlidePart for saving changes.
            parent_slide: The parent slide object.
        """
        self._parent_element = parent_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _get_effect_lst(self) -> ET._Element | None:
        """Get the <a:effectLst> element if it exists."""
        if not hasattr(self, '_parent_element'):
            return None
        return self._parent_element.find(Elements.A_EFFECT_LST)

    def _ensure_effect_lst(self) -> ET._Element:
        """Get or create the <a:effectLst> element at the correct position in spPr.

        OOXML requires spPr children in order: xfrm, geometry, fill, ln, effectLst, ...
        """
        el = self._get_effect_lst()
        if el is not None:
            return el
        el = ET.Element(Elements.A_EFFECT_LST)
        # Insert after <a:ln>, before scene3d/sp3d/extLst
        insert_before = None
        for child in self._parent_element:
            if child.tag in (Elements.A_SCENE_3D, Elements.A_SP_3D, Elements.A_EXT_LST):
                insert_before = child
                break
        if insert_before is not None:
            idx = list(self._parent_element).index(insert_before)
            self._parent_element.insert(idx, el)
        else:
            self._parent_element.append(el)
        return el

    def _get_effect_child(self, tag: str) -> ET._Element | None:
        """Get a specific effect child from effectLst."""
        effect_lst = self._get_effect_lst()
        if effect_lst is None:
            return None
        return effect_lst.find(tag)

    def _ensure_effect_child(self, tag: str) -> ET._Element:
        """Get or create a specific effect child in effectLst at the correct position."""
        effect_lst = self._ensure_effect_lst()
        existing = effect_lst.find(tag)
        if existing is not None:
            return existing
        el = ET.Element(tag)
        try:
            new_rank = _EFFECT_LST_ORDER.index(tag)
        except ValueError:
            effect_lst.append(el)
            return el
        for i, child in enumerate(effect_lst):
            try:
                child_rank = _EFFECT_LST_ORDER.index(child.tag)
            except ValueError:
                continue
            if child_rank > new_rank:
                effect_lst.insert(i, el)
                return el
        effect_lst.append(el)
        return el

    def _remove_effect_child(self, tag: str) -> None:
        """Remove a specific effect child from effectLst."""
        effect_lst = self._get_effect_lst()
        if effect_lst is None:
            return
        child = effect_lst.find(tag)
        if child is not None:
            effect_lst.remove(child)
        # If effectLst is now empty, remove it too
        if len(effect_lst) == 0:
            self._parent_element.remove(effect_lst)

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def is_no_effects(self) -> bool:
        """Returns true if all effects are disabled (as just created, default EffectFormat object). Read-only ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        effect_lst = self._get_effect_lst()
        if effect_lst is None:
            return True
        return len(effect_lst) == 0

    @property
    def blur_effect(self) -> IBlur:
        """Blur effect. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.Blur import Blur
        blur_el = self._get_effect_child(Elements.A_BLUR)
        if blur_el is None:
            return None
        b = Blur()
        b._init_internal(blur_el, self._slide_part, self._parent_slide)
        return b

    @blur_effect.setter
    def blur_effect(self, value: IBlur):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_BLUR)
        else:
            blur_el = self._ensure_effect_child(Elements.A_BLUR)
            blur_el.set('rad', str(int(round(value.radius * EMU_PER_POINT))))
            blur_el.set('grow', '1' if value.grow else '0')
        self._save()

    @property
    def fill_overlay_effect(self) -> IFillOverlay:
        """Fill overlay effect. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.FillOverlay import FillOverlay
        el = self._get_effect_child(Elements.A_FILL_OVERLAY)
        if el is None:
            return None
        fo = FillOverlay()
        fo._init_internal(el, self._slide_part, self._parent_slide)
        return fo

    @fill_overlay_effect.setter
    def fill_overlay_effect(self, value: IFillOverlay):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_FILL_OVERLAY)
        else:
            el = self._ensure_effect_child(Elements.A_FILL_OVERLAY)
            if hasattr(value, '_element'):
                # Copy attributes from value's element
                for k, v in value._element.attrib.items():
                    el.set(k, v)
        self._save()

    @property
    def glow_effect(self) -> IGlow:
        """Glow effect. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.Glow import Glow
        el = self._get_effect_child(Elements.A_GLOW)
        if el is None:
            return None
        g = Glow()
        g._init_internal(el, self._slide_part, self._parent_slide)
        return g

    @glow_effect.setter
    def glow_effect(self, value: IGlow):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_GLOW)
        else:
            el = self._ensure_effect_child(Elements.A_GLOW)
            el.set('rad', str(int(round(value.radius * EMU_PER_POINT))))
        self._save()

    @property
    def inner_shadow_effect(self) -> IInnerShadow:
        """Inner shadow. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.InnerShadow import InnerShadow
        el = self._get_effect_child(Elements.A_INNER_SHDW)
        if el is None:
            return None
        s = InnerShadow()
        s._init_internal(el, self._slide_part, self._parent_slide)
        return s

    @inner_shadow_effect.setter
    def inner_shadow_effect(self, value: IInnerShadow):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_INNER_SHDW)
        else:
            el = self._ensure_effect_child(Elements.A_INNER_SHDW)
            el.set('blurRad', str(int(round(value.blur_radius * EMU_PER_POINT))))
            el.set('dist', str(int(round(value.distance * EMU_PER_POINT))))
            el.set('dir', str(int(round(value.direction * 60000))))
        self._save()

    @property
    def outer_shadow_effect(self) -> IOuterShadow:
        """Outer shadow. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.OuterShadow import OuterShadow
        el = self._get_effect_child(Elements.A_OUTER_SHDW)
        if el is None:
            return None
        s = OuterShadow()
        s._init_internal(el, self._slide_part, self._parent_slide)
        return s

    @outer_shadow_effect.setter
    def outer_shadow_effect(self, value: IOuterShadow):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_OUTER_SHDW)
        else:
            el = self._ensure_effect_child(Elements.A_OUTER_SHDW)
            el.set('blurRad', str(int(round(value.blur_radius * EMU_PER_POINT))))
            el.set('dist', str(int(round(value.distance * EMU_PER_POINT))))
            el.set('dir', str(int(round(value.direction * 60000))))
        self._save()

    @property
    def preset_shadow_effect(self) -> IPresetShadow:
        """Preset shadow. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.PresetShadow import PresetShadow
        el = self._get_effect_child(Elements.A_PRST_SHDW)
        if el is None:
            return None
        s = PresetShadow()
        s._init_internal(el, self._slide_part, self._parent_slide)
        return s

    @preset_shadow_effect.setter
    def preset_shadow_effect(self, value: IPresetShadow):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_PRST_SHDW)
        else:
            el = self._ensure_effect_child(Elements.A_PRST_SHDW)
            if hasattr(value, '_element'):
                for k, v in value._element.attrib.items():
                    el.set(k, v)
        self._save()

    @property
    def reflection_effect(self) -> IReflection:
        """Reflection. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.Reflection import Reflection
        el = self._get_effect_child(Elements.A_REFLECTION)
        if el is None:
            return None
        r = Reflection()
        r._init_internal(el, self._slide_part, self._parent_slide)
        return r

    @reflection_effect.setter
    def reflection_effect(self, value: IReflection):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_REFLECTION)
        else:
            self._ensure_effect_child(Elements.A_REFLECTION)
        self._save()

    @property
    def soft_edge_effect(self) -> ISoftEdge:
        """Soft edge. Read/write ."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .effects.SoftEdge import SoftEdge
        el = self._get_effect_child(Elements.A_SOFT_EDGE)
        if el is None:
            return None
        s = SoftEdge()
        s._init_internal(el, self._slide_part, self._parent_slide)
        return s

    @soft_edge_effect.setter
    def soft_edge_effect(self, value: ISoftEdge):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        if value is None:
            self._remove_effect_child(Elements.A_SOFT_EDGE)
        else:
            el = self._ensure_effect_child(Elements.A_SOFT_EDGE)
            el.set('rad', str(int(round(value.radius * EMU_PER_POINT))))
        self._save()

    @property
    def as_i_effect_param_source(self) -> IEffectParamSource:
        return self

    def set_blur_effect(self, radius, grow) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        blur_el = self._ensure_effect_child(Elements.A_BLUR)
        blur_el.set('rad', str(int(round(radius * EMU_PER_POINT))))
        blur_el.set('grow', '1' if grow else '0')
        self._save()

    def enable_fill_overlay_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_FILL_OVERLAY)
        self._save()

    def enable_glow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_GLOW)
        self._save()

    def enable_inner_shadow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_INNER_SHDW)
        self._save()

    def enable_outer_shadow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_OUTER_SHDW)
        self._save()

    def enable_preset_shadow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_PRST_SHDW)
        self._save()

    def enable_reflection_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_REFLECTION)
        self._save()

    def enable_soft_edge_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._ensure_effect_child(Elements.A_SOFT_EDGE)
        self._save()

    def disable_blur_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_BLUR)
        self._save()

    def disable_fill_overlay_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_FILL_OVERLAY)
        self._save()

    def disable_glow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_GLOW)
        self._save()

    def disable_inner_shadow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_INNER_SHDW)
        self._save()

    def disable_outer_shadow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_OUTER_SHDW)
        self._save()

    def disable_preset_shadow_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_PRST_SHDW)
        self._save()

    def disable_reflection_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_REFLECTION)
        self._save()

    def disable_soft_edge_effect(self) -> None:
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        self._remove_effect_child(Elements.A_SOFT_EDGE)
        self._save()

