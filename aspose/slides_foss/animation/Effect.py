from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .IEffect import IEffect
from .._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .AfterAnimationType import AfterAnimationType
    from .AnimateTextType import AnimateTextType
    from .EffectPresetClassType import EffectPresetClassType
    from .EffectSubtype import EffectSubtype
    from .EffectType import EffectType
    from ..IAudio import IAudio
    from .IBehaviorCollection import IBehaviorCollection
    from ..IColorFormat import IColorFormat
    from .ISequence import ISequence
    from ..IShape import IShape
    from .ITextAnimation import ITextAnimation
    from .ITiming import ITiming


class Effect(IEffect):
    """Represents animation effect."""

    def _init_internal(self, effect_par: ET._Element, sequence, slide_part, parent_slide):
        """Initialize from the innermost effect <p:par> element.

        The structure is: <p:par> / <p:cTn presetID=... presetClass=... presetSubtype=...>
        """
        self._effect_par = effect_par
        self._sequence = sequence
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._timing_cache = None
        self._behaviors_cache = None
        self._text_animation_cache = None

        # The effect's <p:cTn> with preset attributes
        self._ctn = effect_par.find(Elements.P_C_TN)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_target_shape_id(self) -> Optional[int]:
        """Extract the spid from <p:spTgt> in the effect's behaviors."""
        if self._ctn is None:
            return None
        for sp_tgt in self._ctn.iter(Elements.P_SP_TGT):
            spid = sp_tgt.get('spid')
            if spid is not None:
                try:
                    return int(spid)
                except ValueError:
                    pass
        return None

    def _find_shape_by_id(self, shape_id: int):
        """Find shape in parent slide by shape_id (cNvPr id)."""
        if self._parent_slide is None:
            return None
        try:
            shapes = self._parent_slide.shapes
            for i in range(len(shapes)):
                shape = shapes[i]
                if hasattr(shape, 'unique_id') and shape.unique_id == shape_id:
                    return shape
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def sequence(self) -> ISequence:
        return self._sequence

    @property
    def text_animation(self) -> ITextAnimation:
        if self._text_animation_cache is None:
            from .TextAnimation import TextAnimation
            ta = TextAnimation()
            shape_id = self._get_target_shape_id()
            shape_id_str = str(shape_id) if shape_id is not None else None
            # Extract grpId from the effect cTn
            grp_id = self._ctn.get('grpId') if self._ctn is not None else None
            bld_p_found = None
            if shape_id is not None and self._slide_part is not None:
                timing_elem = self._slide_part.timing_element
                if timing_elem is not None:
                    bld_lst = timing_elem.find(Elements.P_BLD_LST)
                    if bld_lst is not None:
                        for bld_p in bld_lst.findall(Elements.P_BLD_P):
                            if bld_p.get('spid') == shape_id_str:
                                bld_p_found = bld_p
                                break
            ta._init_internal(bld_p_found, self._slide_part, shape_id_str, grp_id, self)
            self._text_animation_cache = ta
        return self._text_animation_cache

    @property
    def preset_class_type(self) -> EffectPresetClassType:
        from .EffectPresetClassType import EffectPresetClassType
        from .._internal.pptx.animation_mappings import PRESET_CLASS_MAP
        if self._ctn is not None:
            val = self._ctn.get('presetClass', '')
            return PRESET_CLASS_MAP.get(val, EffectPresetClassType.ENTRANCE)
        return EffectPresetClassType.ENTRANCE

    @preset_class_type.setter
    def preset_class_type(self, value: EffectPresetClassType):
        from .._internal.pptx.animation_mappings import PRESET_CLASS_MAP_REV
        if self._ctn is not None:
            xml_val = PRESET_CLASS_MAP_REV.get(value)
            if xml_val:
                self._ctn.set('presetClass', xml_val)

    @property
    def type(self) -> EffectType:
        from .EffectType import EffectType
        from .._internal.pptx.animation_mappings import PRESET_TO_EFFECT_TYPE
        if self._ctn is not None:
            pid = self._ctn.get('presetID')
            pcls = self._ctn.get('presetClass', '')
            if pid is not None:
                try:
                    return PRESET_TO_EFFECT_TYPE.get((int(pid), pcls), EffectType.CUSTOM)
                except ValueError:
                    pass
        return EffectType.CUSTOM

    @type.setter
    def type(self, value: EffectType):
        from .._internal.pptx.animation_mappings import EFFECT_TYPE_TO_PRESET
        if self._ctn is not None:
            entry = EFFECT_TYPE_TO_PRESET.get(value)
            if entry is not None:
                self._ctn.set('presetID', str(entry[0]))
                self._ctn.set('presetClass', entry[1])

    @property
    def subtype(self) -> EffectSubtype:
        from .EffectSubtype import EffectSubtype
        from .._internal.pptx.animation_mappings import PRESET_SUBTYPE_TO_EFFECT_SUBTYPE
        if self._ctn is not None:
            val = self._ctn.get('presetSubtype')
            if val is not None:
                try:
                    return PRESET_SUBTYPE_TO_EFFECT_SUBTYPE.get(int(val), EffectSubtype.NONE)
                except ValueError:
                    pass
        return EffectSubtype.NONE

    @subtype.setter
    def subtype(self, value: EffectSubtype):
        from .._internal.pptx.animation_mappings import EFFECT_SUBTYPE_TO_PRESET_SUBTYPE
        if self._ctn is not None:
            pst = EFFECT_SUBTYPE_TO_PRESET_SUBTYPE.get(value, 0)
            self._ctn.set('presetSubtype', str(pst))

    @property
    def behaviors(self) -> IBehaviorCollection:
        if self._behaviors_cache is None:
            from .BehaviorCollection import BehaviorCollection
            bc = BehaviorCollection()
            if self._ctn is not None:
                child_tn = self._ctn.find(Elements.P_CHILD_TN_LST)
                bc._init_internal(child_tn, self._slide_part)
            else:
                bc._init_internal(None)
            self._behaviors_cache = bc
        return self._behaviors_cache

    @behaviors.setter
    def behaviors(self, value: IBehaviorCollection):
        self._behaviors_cache = value

    @property
    def timing(self) -> ITiming:
        if self._timing_cache is None:
            from .Timing import Timing
            if self._ctn is not None:
                t = Timing()
                t._init_internal(self._ctn)
                self._timing_cache = t
        return self._timing_cache

    @timing.setter
    def timing(self, value: ITiming):
        self._timing_cache = value

    @property
    def target_shape(self) -> IShape:
        shape_id = self._get_target_shape_id()
        if shape_id is not None:
            return self._find_shape_by_id(shape_id)
        return None

    @property
    def sound(self) -> IAudio:
        return None

    @sound.setter
    def sound(self, value: IAudio):
        # Sound embedding requires audio relationship management
        pass

    @property
    def stop_previous_sound(self) -> bool:
        if self._ctn is not None:
            return self._ctn.get('stCondLst_stopPrevSound') == '1'
        return False

    @stop_previous_sound.setter
    def stop_previous_sound(self, value: bool):
        pass

    @property
    def after_animation_type(self) -> AfterAnimationType:
        from .AfterAnimationType import AfterAnimationType
        return AfterAnimationType.DO_NOT_DIM

    @after_animation_type.setter
    def after_animation_type(self, value: AfterAnimationType):
        pass

    @property
    def after_animation_color(self) -> IColorFormat:
        return None

    @after_animation_color.setter
    def after_animation_color(self, value: IColorFormat):
        pass

    @property
    def animate_text_type(self) -> AnimateTextType:
        from .AnimateTextType import AnimateTextType
        if self._ctn is not None:
            iterate = self._ctn.find(f'{NS.P}iterate')
            if iterate is not None:
                it_type = iterate.get('type', '')
                _map = {'wd': AnimateTextType.BY_WORD, 'lt': AnimateTextType.BY_LETTER}
                return _map.get(it_type, AnimateTextType.ALL_AT_ONCE)
        return AnimateTextType.ALL_AT_ONCE

    @animate_text_type.setter
    def animate_text_type(self, value: AnimateTextType):
        from .AnimateTextType import AnimateTextType
        if self._ctn is None:
            return
        iterate = self._ctn.find(f'{NS.P}iterate')
        if value == AnimateTextType.ALL_AT_ONCE:
            if iterate is not None:
                self._ctn.remove(iterate)
            return
        if iterate is None:
            # Insert <p:iterate> after <p:stCondLst> and before <p:childTnLst>
            iterate = ET.SubElement(self._ctn, f'{NS.P}iterate')
            # Move it before childTnLst
            child_tn = self._ctn.find(Elements.P_CHILD_TN_LST)
            if child_tn is not None:
                self._ctn.remove(iterate)
                idx = list(self._ctn).index(child_tn)
                self._ctn.insert(idx, iterate)
        _map = {AnimateTextType.BY_WORD: 'wd', AnimateTextType.BY_LETTER: 'lt'}
        iterate.set('type', _map.get(value, 'wd'))
        # Ensure tmPct child exists
        if iterate.find(f'{NS.P}tmPct') is None:
            ET.SubElement(iterate, f'{NS.P}tmPct', val='0')
        # Also ensure bldP exists for text animation
        self._ensure_bld_p_for_text()

    def _ensure_bld_p_for_text(self):
        """Ensure <p:bldP> exists for text animation on this effect's target shape."""
        if self._slide_part is None or self._ctn is None:
            return
        shape_id = self._get_target_shape_id()
        grp_id = self._ctn.get('grpId')
        if shape_id is None:
            return
        timing = self._slide_part.timing_element
        if timing is None:
            return
        bld_lst = timing.find(Elements.P_BLD_LST)
        if bld_lst is None:
            bld_lst = ET.SubElement(timing, Elements.P_BLD_LST)
        # Check if entry already exists
        for bp in bld_lst.findall(Elements.P_BLD_P):
            if bp.get('spid') == str(shape_id) and bp.get('grpId') == grp_id:
                return
        attrs = {'spid': str(shape_id), 'animBg': '1'}
        if grp_id:
            attrs['grpId'] = grp_id
        ET.SubElement(bld_lst, Elements.P_BLD_P, **attrs)

    @property
    def delay_between_text_parts(self) -> float:
        if self._ctn is not None:
            iterate = self._ctn.find(f'{NS.P}iterate')
            if iterate is not None:
                tm_pct = iterate.find(f'{NS.P}tmPct')
                if tm_pct is not None:
                    val = tm_pct.get('val', '0')
                    try:
                        return int(val) / 1000.0
                    except ValueError:
                        pass
        return 0.0

    @delay_between_text_parts.setter
    def delay_between_text_parts(self, value: float):
        if self._ctn is None:
            return
        iterate = self._ctn.find(f'{NS.P}iterate')
        if iterate is None:
            # Need to set animate_text_type first
            return
        tm_pct = iterate.find(f'{NS.P}tmPct')
        if tm_pct is None:
            tm_pct = ET.SubElement(iterate, f'{NS.P}tmPct')
        tm_pct.set('val', str(int(value * 1000)))
