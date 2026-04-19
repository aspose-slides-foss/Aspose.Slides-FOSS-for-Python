from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any, Optional
import lxml.etree as ET
from .ISequence import ISequence
from .._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .IEffect import IEffect
    from ..IShape import IShape


class Sequence(ISequence):
    """Represents sequence (collection of effects)."""

    def _init_internal(self, seq_elem: ET._Element, slide_part, parent_slide, is_main: bool = True):
        """Initialize from a <p:seq> element.

        Args:
            seq_elem: The <p:seq> XML element.
            slide_part: The SlidePart that owns this timing tree.
            parent_slide: The Slide/LayoutSlide/MasterSlide object.
            is_main: True if this is the main sequence, False for interactive.
        """
        self._seq_elem = seq_elem
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._is_main = is_main
        self._effects: Optional[list] = None
        self._trigger_shape_val = None

        # The <p:cTn> of the sequence
        self._seq_ctn = seq_elem.find(Elements.P_C_TN)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_seq_child_tn_lst(self) -> ET._Element:
        """Get or create the <p:childTnLst> under the sequence's <p:cTn>."""
        child_tn = self._seq_ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn is None:
            child_tn = ET.SubElement(self._seq_ctn, Elements.P_CHILD_TN_LST)
        return child_tn

    def _load_effects(self):
        """Parse existing effect nodes from XML."""
        if self._effects is not None:
            return

        from .Effect import Effect
        self._effects = []

        child_tn = self._seq_ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn is None:
            return

        # Each click-group is a <p:par> under <p:childTnLst>
        for click_par in child_tn.findall(Elements.P_PAR):
            click_ctn = click_par.find(Elements.P_C_TN)
            if click_ctn is None:
                continue
            click_children = click_ctn.find(Elements.P_CHILD_TN_LST)
            if click_children is None:
                continue

            for wrapper_par in click_children.findall(Elements.P_PAR):
                wrapper_ctn = wrapper_par.find(Elements.P_C_TN)
                if wrapper_ctn is None:
                    continue
                wrapper_children = wrapper_ctn.find(Elements.P_CHILD_TN_LST)
                if wrapper_children is None:
                    continue

                for effect_par in wrapper_children.findall(Elements.P_PAR):
                    eff = Effect()
                    eff._init_internal(effect_par, self, self._slide_part, self._parent_slide)
                    self._effects.append(eff)

    def _resolve_paragraph_target(self, paragraph):
        """Given a Paragraph, return (parent_shape, paragraph_index).

        Navigates from the paragraph's XML element up to the containing shape,
        then finds the matching Shape object and computes the 0-based paragraph index.
        """
        p_elem = paragraph._p_element
        txbody = paragraph._txbody_element
        if txbody is None and p_elem is not None:
            txbody = p_elem.getparent()

        # Compute paragraph index
        para_index = 0
        if txbody is not None and p_elem is not None:
            for i, ap in enumerate(txbody.findall(Elements.A_P)):
                if ap is p_elem:
                    para_index = i
                    break

        # Find the parent shape element (walk up from txBody)
        shape_elem = txbody.getparent() if txbody is not None else None

        # Match to a Shape object on the slide by unique_id
        shape = None
        if shape_elem is not None and self._parent_slide is not None:
            nv = shape_elem.find(f'{NS.P}nvSpPr')
            if nv is not None:
                cnv_pr = nv.find(f'{NS.P}cNvPr')
                if cnv_pr is not None:
                    target_id = cnv_pr.get('id')
                    for s in self._parent_slide.shapes:
                        if str(s.unique_id) == target_id:
                            shape = s
                            break
        if shape is None:
            raise ValueError("Cannot resolve the parent shape of the given paragraph")
        return shape, para_index

    def _build_effect_xml(self, shape, effect_type, subtype, trigger_type, paragraph_index=None) -> ET._Element:
        """Build the triple-nested <p:par> structure for a new effect.

        Returns the outermost click-group <p:par> element.
        """
        from .EffectType import EffectType
        from .EffectTriggerType import EffectTriggerType
        from .._internal.pptx.animation_mappings import (
            EFFECT_TYPE_TO_PRESET, EFFECT_SUBTYPE_TO_PRESET_SUBTYPE,
            TRIGGER_TO_NODE_TYPE, infer_preset_class,
        )

        preset_entry = EFFECT_TYPE_TO_PRESET.get(effect_type, (1, 'entr'))
        preset_id = preset_entry[0]
        preset_class_str = preset_entry[1]
        preset_subtype = EFFECT_SUBTYPE_TO_PRESET_SUBTYPE.get(subtype, 0)
        node_type = TRIGGER_TO_NODE_TYPE.get(trigger_type, 'clickEffect')

        # Get shape ID
        shape_id = str(shape.unique_id) if hasattr(shape, 'unique_id') else '0'

        # Manage grpId counter — global per slide (shared across all sequences)
        if not hasattr(self._slide_part, '_grp_id_counter'):
            self._slide_part._grp_id_counter = 0
        self._slide_part._grp_id_counter += 1
        grp_id = str(self._slide_part._grp_id_counter)

        # Get next cTn IDs
        id_base = self._slide_part.next_ctn_id()

        # Build outer click-group: <p:par>
        click_par = ET.Element(Elements.P_PAR)
        click_ctn = ET.SubElement(click_par, Elements.P_C_TN,
                                   id=str(id_base), fill='hold',
                                   nodeType='clickPar')
        st_cond = ET.SubElement(click_ctn, Elements.P_ST_COND_LST)
        # Interactive sequences use delay="0", main sequences use "indefinite"
        from .EffectTriggerType import EffectTriggerType
        click_delay = '0' if not self._is_main else 'indefinite'
        ET.SubElement(st_cond, Elements.P_COND, delay=click_delay)
        # The onBegin condition is added for AFTER_PREVIOUS / WITH_PREVIOUS effects
        # so they auto-start when the sequence begins (on slide show).
        if self._is_main and trigger_type in (EffectTriggerType.AFTER_PREVIOUS,
                                               EffectTriggerType.WITH_PREVIOUS):
            cond2 = ET.SubElement(st_cond, Elements.P_COND, evt='onBegin', delay='0')
            tn_ref = ET.SubElement(cond2, f'{NS.P}tn')
            tn_ref.set('val', self._seq_ctn.get('id', '2'))
        click_children = ET.SubElement(click_ctn, Elements.P_CHILD_TN_LST)

        # Build wrapper: <p:par>
        wrapper_par = ET.SubElement(click_children, Elements.P_PAR)
        wrapper_ctn = ET.SubElement(wrapper_par, Elements.P_C_TN,
                                     id=str(id_base + 1), fill='hold',
                                     nodeType='afterGroup')
        st_cond2 = ET.SubElement(wrapper_ctn, Elements.P_ST_COND_LST)
        # AFTER_PREVIOUS wrapper delays until the preceding effect finishes.
        # Compute from the last wrapper's effect delay + duration.
        # WITH_PREVIOUS and ON_CLICK start immediately (delay="0").
        wrapper_delay = '0'
        if trigger_type == EffectTriggerType.AFTER_PREVIOUS:
            wrapper_delay = self._compute_after_delay()
        ET.SubElement(st_cond2, Elements.P_COND, delay=wrapper_delay)
        wrapper_children = ET.SubElement(wrapper_ctn, Elements.P_CHILD_TN_LST)

        # Build effect node: <p:par>
        effect_par = ET.SubElement(wrapper_children, Elements.P_PAR)
        ctn_attrs = {
            'id': str(id_base + 2),
            'presetID': str(preset_id),
            'presetClass': preset_class_str,
            'presetSubtype': str(preset_subtype),
            'fill': 'hold',
            'grpId': grp_id,
            'nodeType': node_type,
        }
        # Path effects get accel/decel
        if preset_class_str == 'path':
            ctn_attrs['accel'] = '50000'
            ctn_attrs['decel'] = '50000'
        effect_ctn = ET.SubElement(effect_par, Elements.P_C_TN, **ctn_attrs)
        st_cond3 = ET.SubElement(effect_ctn, Elements.P_ST_COND_LST)
        ET.SubElement(st_cond3, Elements.P_COND, delay='0')
        effect_children = ET.SubElement(effect_ctn, Elements.P_CHILD_TN_LST)

        # Add default behaviors based on preset class
        if preset_class_str == 'entr':
            self._add_default_entrance_behavior(
                effect_children, shape_id, id_base + 3, effect_type, subtype,
                paragraph_index=paragraph_index)
        elif preset_class_str == 'path':
            self._add_default_motion_behavior(effect_children, shape_id, id_base + 3,
                                               effect_type,
                                               paragraph_index=paragraph_index)

        # Add <p:bldLst>/<p:bldP> entry
        # Commercial adds for path/entrance effects targeting the whole shape.
        # Paragraph-level animations must NOT have <p:bldP> — it would override
        # the per-paragraph <p:pRg> targeting and animate all paragraphs together.
        if preset_class_str in ('path', 'entr') and paragraph_index is None:
            self._ensure_bld_p(shape_id, grp_id)

        return click_par, effect_par

    def _ensure_bld_p(self, shape_id: str, grp_id: str):
        """Ensure a <p:bldP> entry exists in <p:bldLst> for this shape/grpId."""
        timing = self._slide_part.timing_element
        if timing is None:
            return
        bld_lst = timing.find(Elements.P_BLD_LST)
        if bld_lst is None:
            bld_lst = ET.SubElement(timing, Elements.P_BLD_LST)
        ET.SubElement(bld_lst, Elements.P_BLD_P,
                      spid=shape_id, grpId=grp_id, animBg='1')

    def _compute_after_delay(self) -> str:
        """Compute the delay for an AFTER_PREVIOUS wrapper based on preceding effects."""
        child_tn = self._get_seq_child_tn_lst()
        click_groups = child_tn.findall(Elements.P_PAR)
        if not click_groups:
            return '500'
        # Look at the last click-group's last wrapper
        last_cg = click_groups[-1]
        last_cg_ctn = last_cg.find(Elements.P_C_TN)
        last_cg_children = last_cg_ctn.find(Elements.P_CHILD_TN_LST) if last_cg_ctn is not None else None
        if last_cg_children is None:
            return '500'
        wrappers = last_cg_children.findall(Elements.P_PAR)
        if not wrappers:
            return '500'
        # Sum up: last wrapper's delay + its effect's (delay + duration)
        last_wrapper = wrappers[-1]
        lw_ctn = last_wrapper.find(Elements.P_C_TN)
        # Wrapper's own delay
        lw_st = lw_ctn.find(Elements.P_ST_COND_LST) if lw_ctn is not None else None
        lw_cond = lw_st.find(Elements.P_COND) if lw_st is not None else None
        lw_delay = int(lw_cond.get('delay', '0')) if lw_cond is not None else 0
        # Find the effect node inside
        lw_children = lw_ctn.find(Elements.P_CHILD_TN_LST) if lw_ctn is not None else None
        eff_delay = 0
        eff_dur = 500  # default
        if lw_children is not None:
            eff_par = lw_children.find(Elements.P_PAR)
            if eff_par is not None:
                eff_ctn = eff_par.find(Elements.P_C_TN)
                if eff_ctn is not None:
                    # Effect's own delay
                    est = eff_ctn.find(Elements.P_ST_COND_LST)
                    if est is not None:
                        ec = est.find(Elements.P_COND)
                        if ec is not None:
                            try:
                                eff_delay = int(ec.get('delay', '0'))
                            except ValueError:
                                eff_delay = 0
                    # Effect's duration from animEffect/anim behavior
                    eff_child_tn = eff_ctn.find(Elements.P_CHILD_TN_LST)
                    if eff_child_tn is not None:
                        for tag in (Elements.P_ANIM_EFFECT, Elements.P_ANIM):
                            for bhvr in eff_child_tn.findall(tag):
                                cb = bhvr.find(Elements.P_C_BHVR)
                                if cb is not None:
                                    bctn = cb.find(Elements.P_C_TN)
                                    if bctn is not None:
                                        d = bctn.get('dur')
                                        if d and d != 'indefinite':
                                            try:
                                                eff_dur = int(d)
                                            except ValueError:
                                                pass
                                            break
        total = lw_delay + eff_delay + eff_dur
        return str(total)

    # Map EffectType to the OOXML filter string for <p:animEffect>
    _EFFECT_FILTER_MAP = {
        'Fade': 'fade',
        'Blinds': 'blinds',
        'Box': 'box',
        'Checkerboard': 'checkerboard',
        'Circle': 'circle',
        'Diamond': 'diamond',
        'Dissolve': 'dissolve',
        'Plus': 'plus',
        'RandomBars': 'randomBar',
        'Split': 'split',
        'Strips': 'strips',
        'Wedge': 'wedge',
        'Wheel': 'wheel',
        'Wipe': 'wipe',
    }

    # Map EffectSubtype to the filter parameter name for <p:animEffect>
    _SUBTYPE_FILTER_PARAM = {
        'Horizontal': 'horizontal', 'Vertical': 'vertical',
        'Across': 'across', 'Left': 'left', 'Right': 'right',
        'Top': 'up', 'Bottom': 'down',
        'In': 'in', 'Out': 'out',
        'HorizontalIn': 'inHorizontal', 'HorizontalOut': 'outHorizontal',
        'VerticalIn': 'inVertical', 'VerticalOut': 'outVertical',
    }

    @staticmethod
    def _build_sp_tgt(parent: ET._Element, shape_id: str, paragraph_index=None):
        """Build <p:spTgt spid="..."> optionally with <p:txEl><p:pRg> for paragraph targeting."""
        sp_tgt = ET.SubElement(parent, Elements.P_SP_TGT, spid=shape_id)
        if paragraph_index is not None:
            tx_el = ET.SubElement(sp_tgt, f'{NS.P}txEl')
            ET.SubElement(tx_el, f'{NS.P}pRg',
                          st=str(paragraph_index), end=str(paragraph_index))
        return sp_tgt

    def _add_default_entrance_behavior(self, parent: ET._Element, shape_id: str,
                                        ctn_id: int, effect_type=None, subtype=None,
                                        paragraph_index=None):
        """Add the default <p:set> + <p:animEffect> behaviors for entrance effects."""
        # 1) <p:set> for visibility
        set_elem = ET.SubElement(parent, Elements.P_SET)
        cbhvr = ET.SubElement(set_elem, Elements.P_C_BHVR)
        ctn = ET.SubElement(cbhvr, Elements.P_C_TN, id=str(ctn_id), dur='1', fill='hold')
        st = ET.SubElement(ctn, Elements.P_ST_COND_LST)
        ET.SubElement(st, Elements.P_COND, delay='0')
        tgt_el = ET.SubElement(cbhvr, Elements.P_TGT_EL)
        self._build_sp_tgt(tgt_el, shape_id, paragraph_index)
        attr_lst = ET.SubElement(cbhvr, Elements.P_ATTR_NAME_LST)
        attr_name = ET.SubElement(attr_lst, Elements.P_ATTR_NAME)
        attr_name.text = 'style.visibility'
        to_elem = ET.SubElement(set_elem, Elements.P_TO)
        ET.SubElement(to_elem, Elements.P_STR_VAL, val='visible')

        # 2) Effect-specific behavior
        if effect_type is not None:
            from .EffectType import EffectType
            from .EffectSubtype import EffectSubtype as ES

            if effect_type == EffectType.FLY:
                # FLY uses <p:anim> property animations for position
                self._add_fly_behavior(parent, shape_id, ctn_id + 1, subtype,
                                       paragraph_index=paragraph_index)
            else:
                # Other entrance effects use <p:animEffect> filter transition
                filter_name = self._EFFECT_FILTER_MAP.get(effect_type.value)
                if filter_name:
                    if subtype is not None:
                        param = self._SUBTYPE_FILTER_PARAM.get(subtype.value)
                        if param:
                            filter_name = f'{filter_name}({param})'
                    anim_eff = ET.SubElement(parent, Elements.P_ANIM_EFFECT,
                                             transition='in', filter=filter_name)
                    cbhvr2 = ET.SubElement(anim_eff, Elements.P_C_BHVR)
                    ET.SubElement(cbhvr2, Elements.P_C_TN, id=str(ctn_id + 1), dur='500')
                    tgt2 = ET.SubElement(cbhvr2, Elements.P_TGT_EL)
                    self._build_sp_tgt(tgt2, shape_id, paragraph_index)

    def _add_fly_behavior(self, parent, shape_id, ctn_id, subtype, paragraph_index=None):
        """Add <p:anim> property animations for FLY entrance effect."""
        from .EffectSubtype import EffectSubtype as ES

        # Determine which axis to animate and the starting formula
        # FLY moves the shape from off-screen to its final position
        # Formulas verified against PowerPoint output.
        # '1' = 100% of slide dimension in PPT formula coords.
        _FLY_PARAMS = {
            ES.LEFT:         ('ppt_x', '0-#ppt_w/2', '#ppt_x', 'ppt_y', '#ppt_y', '#ppt_y'),
            ES.RIGHT:        ('ppt_x', '1+#ppt_w/2', '#ppt_x', 'ppt_y', '#ppt_y', '#ppt_y'),
            ES.TOP:          ('ppt_x', '#ppt_x', '#ppt_x', 'ppt_y', '0-#ppt_h/2', '#ppt_y'),
            ES.BOTTOM:       ('ppt_x', '#ppt_x', '#ppt_x', 'ppt_y', '1+#ppt_h/2', '#ppt_y'),
            ES.TOP_LEFT:     ('ppt_x', '0-#ppt_w/2', '#ppt_x', 'ppt_y', '0-#ppt_h/2', '#ppt_y'),
            ES.TOP_RIGHT:    ('ppt_x', '1+#ppt_w/2', '#ppt_x', 'ppt_y', '0-#ppt_h/2', '#ppt_y'),
            ES.BOTTOM_LEFT:  ('ppt_x', '0-#ppt_w/2', '#ppt_x', 'ppt_y', '1+#ppt_h/2', '#ppt_y'),
            ES.BOTTOM_RIGHT: ('ppt_x', '1+#ppt_w/2', '#ppt_x', 'ppt_y', '1+#ppt_h/2', '#ppt_y'),
        }
        params = _FLY_PARAMS.get(subtype, _FLY_PARAMS[ES.LEFT])
        x_attr, x_from, x_to, y_attr, y_from, y_to = params

        for attr, val_from, val_to, cid_offset in [
            (x_attr, x_from, x_to, 0),
            (y_attr, y_from, y_to, 1),
        ]:
            anim = ET.SubElement(parent, Elements.P_ANIM, calcmode='lin', valueType='num')
            cbhvr = ET.SubElement(anim, Elements.P_C_BHVR, additive='base')
            ET.SubElement(cbhvr, Elements.P_C_TN, id=str(ctn_id + cid_offset),
                          dur='500', fill='hold')
            tgt = ET.SubElement(cbhvr, Elements.P_TGT_EL)
            self._build_sp_tgt(tgt, shape_id, paragraph_index)
            anl = ET.SubElement(cbhvr, Elements.P_ATTR_NAME_LST)
            an = ET.SubElement(anl, Elements.P_ATTR_NAME)
            an.text = attr

            tav_lst = ET.SubElement(anim, f'{NS.P}tavLst')
            tav0 = ET.SubElement(tav_lst, f'{NS.P}tav', tm='0')
            val0 = ET.SubElement(tav0, f'{NS.P}val')
            ET.SubElement(val0, Elements.P_STR_VAL, val=val_from)
            tav1 = ET.SubElement(tav_lst, f'{NS.P}tav', tm='100000')
            val1 = ET.SubElement(tav1, f'{NS.P}val')
            ET.SubElement(val1, Elements.P_STR_VAL, val=val_to)

    # Predefined SVG path data for common motion path presets
    _PRESET_PATH_DATA = {
        'PathFootball': 'M 0 0 C 0.03 -0.05062 0.075 -0.08259 0.125 -0.08259 C 0.175 -0.08259 0.22 -0.05062 0.25 0 C 0.22 0.05062 0.175 0.08259 0.125 0.08259 C 0.075 0.08259 0.03 0.05062 0 0 Z',
        'PathCircle': 'M 0 0 C 0.06 -0.06 0.145 -0.1 0.235 -0.1 C 0.325 -0.1 0.41 -0.06 0.47 0 C 0.41 0.06 0.325 0.1 0.235 0.1 C 0.145 0.1 0.06 0.06 0 0 Z',
        'PathDiamond': 'M 0 0 L 0.125 -0.1 L 0.25 0 L 0.125 0.1 Z',
        'PathHeart': 'M 0 0 C 0.035 -0.04 0.07 -0.065 0.125 -0.065 C 0.18 -0.065 0.215 -0.04 0.25 0 C 0.215 0.04 0.18 0.065 0.125 0.065 C 0.07 0.065 0.035 0.04 0 0 Z',
        'PathSquare': 'M 0 0 L 0.25 0 L 0.25 0.188 L 0 0.188 Z',
        'PathHexagon': 'M 0 0 L 0.063 -0.094 L 0.188 -0.094 L 0.25 0 L 0.188 0.094 L 0.063 0.094 Z',
        'PathRight': 'M 0 0 L 0.25 0 E',
        'PathLeft': 'M 0 0 L -0.25 0 E',
        'PathDown': 'M 0 0 L 0 0.25 E',
        'PathUp': 'M 0 0 L 0 -0.25 E',
    }

    def _add_default_motion_behavior(self, parent: ET._Element, shape_id: str,
                                      ctn_id: int, effect_type=None,
                                      paragraph_index=None):
        """Add the default <p:animMotion> behavior for path effects."""
        # Look up preset path data
        path_data = ''
        if effect_type is not None:
            path_data = self._PRESET_PATH_DATA.get(effect_type.value, '')

        anim_motion = ET.SubElement(parent, Elements.P_ANIM_MOTION,
                                     origin='layout', path=path_data,
                                     pathEditMode='relative', ptsTypes='')
        cbhvr = ET.SubElement(anim_motion, Elements.P_C_BHVR)
        ET.SubElement(cbhvr, Elements.P_C_TN, id=str(ctn_id), dur='2000', fill='hold')
        tgt_el = ET.SubElement(cbhvr, Elements.P_TGT_EL)
        self._build_sp_tgt(tgt_el, shape_id, paragraph_index)
        attr_lst = ET.SubElement(cbhvr, Elements.P_ATTR_NAME_LST)
        an1 = ET.SubElement(attr_lst, Elements.P_ATTR_NAME)
        an1.text = 'ppt_x'
        an2 = ET.SubElement(attr_lst, Elements.P_ATTR_NAME)
        an2.text = 'ppt_y'

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def count(self) -> int:
        self._load_effects()
        return len(self._effects)

    @property
    def trigger_shape(self) -> IShape:
        if self._trigger_shape_val is not None:
            return self._trigger_shape_val
        if not self._is_main and self._seq_ctn is not None:
            # Interactive sequences store trigger shape in stCondLst
            st_cond = self._seq_ctn.find(Elements.P_ST_COND_LST)
            if st_cond is not None:
                cond = st_cond.find(Elements.P_COND)
                if cond is not None:
                    tgt = cond.find(Elements.P_TGT_EL)
                    if tgt is not None:
                        sp_tgt = tgt.find(Elements.P_SP_TGT)
                        if sp_tgt is not None:
                            spid = sp_tgt.get('spid')
                            if spid and self._parent_slide:
                                try:
                                    shapes = self._parent_slide.shapes
                                    for i in range(len(shapes)):
                                        s = shapes[i]
                                        if hasattr(s, 'unique_id') and s.unique_id == int(spid):
                                            return s
                                except Exception:
                                    pass
        return None

    @trigger_shape.setter
    def trigger_shape(self, value: IShape):
        self._trigger_shape_val = value

    @property
    def as_i_enumerable(self) -> Any:
        self._load_effects()
        return iter(self._effects)

    @overload
    def add_effect(self, shape, effect_type, subtype, trigger_type) -> IEffect:
        ...

    @overload
    def add_effect(self, paragraph, effect_type, subtype, trigger_type) -> IEffect:
        ...

    @overload
    def add_effect(self, chart, type, index, effect_type, subtype, trigger_type) -> IEffect:
        ...

    @overload
    def add_effect(self, chart, type, series_index, categories_index, effect_type, subtype, trigger_type) -> IEffect:
        ...

    def add_effect(self, *args, **kwargs) -> IEffect:
        """Add an animation effect to the sequence."""
        from .Effect import Effect
        from .EffectTriggerType import EffectTriggerType
        from ..IParagraph import IParagraph

        if len(args) == 4:
            target, effect_type, subtype, trigger_type = args
        else:
            raise ValueError(f"add_effect expects 4 arguments (shape_or_paragraph, effect_type, subtype, trigger_type), got {len(args)}")

        # Detect paragraph overload: first arg is IParagraph → paragraph-level animation
        paragraph_index = None
        if isinstance(target, IParagraph):
            paragraph = target
            shape, paragraph_index = self._resolve_paragraph_target(paragraph)
        else:
            shape = target

        # Ensure timing structure exists
        self._slide_part.ensure_timing_element()

        # Build the XML
        click_par, effect_par = self._build_effect_xml(shape, effect_type, subtype, trigger_type,
                                                        paragraph_index=paragraph_index)

        child_tn = self._get_seq_child_tn_lst()

        if trigger_type in (EffectTriggerType.AFTER_PREVIOUS, EffectTriggerType.WITH_PREVIOUS):
            # Append the wrapper <p:par> into the LAST existing click-group
            existing = child_tn.findall(Elements.P_PAR)
            if existing:
                last_click = existing[-1]
                last_ctn = last_click.find(Elements.P_C_TN)
                last_children = last_ctn.find(Elements.P_CHILD_TN_LST) if last_ctn is not None else None
                if last_children is not None:
                    # click_par is the new click-group; extract its wrapper <p:par>
                    new_ctn = click_par.find(Elements.P_C_TN)
                    new_children = new_ctn.find(Elements.P_CHILD_TN_LST) if new_ctn is not None else None
                    if new_children is not None:
                        for wrapper in list(new_children):
                            last_children.append(wrapper)
                    # Don't append click_par itself — we reused the last one
                else:
                    child_tn.append(click_par)
            else:
                child_tn.append(click_par)
        else:
            child_tn.append(click_par)

        # Create Effect object
        eff = Effect()
        eff._init_internal(effect_par, self, self._slide_part, self._parent_slide)

        # Update cache — initialise if needed, but do not re-parse
        if self._effects is None:
            self._effects = []
        self._effects.append(eff)

        return eff

    def remove(self, item) -> None:
        self._load_effects()
        if item in self._effects:
            self._effects.remove(item)
            self._remove_effect_xml(item)
            self._remove_bld_p(item)

    def remove_at(self, index) -> None:
        self._load_effects()
        item = self._effects.pop(index)
        self._remove_effect_xml(item)
        self._remove_bld_p(item)

    def _remove_effect_xml(self, effect):
        """Remove the wrapper for this effect from XML.

        If the click-group has other wrappers, only this wrapper is removed.
        If the click-group becomes empty, the entire click-group is removed.
        """
        # Navigate: effect_par -> wrapper_childTnLst -> wrapper_ctn -> wrapper_par
        #   -> click_childTnLst -> click_ctn -> click_par -> seq_childTnLst
        effect_par = effect._effect_par
        wrapper_children = effect_par.getparent()
        if wrapper_children is None:
            return
        wrapper_ctn = wrapper_children.getparent()
        if wrapper_ctn is None:
            return
        wrapper_par = wrapper_ctn.getparent()
        if wrapper_par is None:
            return
        click_children = wrapper_par.getparent()
        if click_children is None:
            return

        # Remove the wrapper <p:par> from the click-group's childTnLst
        click_children.remove(wrapper_par)

        # If no wrappers left, remove the entire click-group
        if len(click_children) == 0:
            click_ctn = click_children.getparent()
            if click_ctn is not None:
                click_par = click_ctn.getparent()
                if click_par is not None:
                    seq_children = click_par.getparent()
                    if seq_children is not None:
                        seq_children.remove(click_par)

    def _remove_bld_p(self, effect):
        """Remove the <p:bldP> entry for a removed effect."""
        if effect._ctn is None or self._slide_part is None:
            return
        grp_id = effect._ctn.get('grpId')
        shape_id = effect._get_target_shape_id()
        if shape_id is None or grp_id is None:
            return
        timing = self._slide_part.timing_element
        if timing is None:
            return
        bld_lst = timing.find(Elements.P_BLD_LST)
        if bld_lst is None:
            return
        for bp in list(bld_lst.findall(Elements.P_BLD_P)):
            if bp.get('spid') == str(shape_id) and bp.get('grpId') == grp_id:
                bld_lst.remove(bp)
                break
        # Remove empty bldLst
        if len(bld_lst) == 0:
            timing.remove(bld_lst)

    def clear(self) -> None:
        self._load_effects()
        child_tn = self._seq_ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn is not None:
            for child in list(child_tn):
                child_tn.remove(child)
        self._effects.clear()

    def remove_by_shape(self, shape) -> None:
        self._load_effects()
        shape_id = shape.unique_id if hasattr(shape, 'unique_id') else None
        if shape_id is None:
            return
        to_remove = [e for e in self._effects if e._get_target_shape_id() == shape_id]
        for e in to_remove:
            self.remove(e)
        self._consolidate_click_groups()

    def _consolidate_click_groups(self):
        """Merge orphaned afterEffect/withEffect click-groups into the preceding one."""
        child_tn = self._seq_ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn is None:
            return
        click_groups = child_tn.findall(Elements.P_PAR)
        i = 1
        while i < len(click_groups):
            cg = click_groups[i]
            cg_ctn = cg.find(Elements.P_C_TN)
            cg_children = cg_ctn.find(Elements.P_CHILD_TN_LST) if cg_ctn is not None else None
            if cg_children is None or len(cg_children) == 0:
                child_tn.remove(cg)
                click_groups = child_tn.findall(Elements.P_PAR)
                continue
            # Check if all effects in this click-group are afterEffect or withEffect
            all_non_click = True
            for wrapper in cg_children.findall(Elements.P_PAR):
                w_ctn = wrapper.find(Elements.P_C_TN)
                w_children = w_ctn.find(Elements.P_CHILD_TN_LST) if w_ctn is not None else None
                if w_children is not None:
                    for ep in w_children.findall(Elements.P_PAR):
                        ep_ctn = ep.find(Elements.P_C_TN)
                        if ep_ctn is not None and ep_ctn.get('nodeType') == 'clickEffect':
                            all_non_click = False
                            break
            if all_non_click and i > 0:
                # Move all wrappers into the preceding click-group
                prev_cg = click_groups[i - 1]
                prev_ctn = prev_cg.find(Elements.P_C_TN)
                prev_children = prev_ctn.find(Elements.P_CHILD_TN_LST) if prev_ctn is not None else None
                if prev_children is not None:
                    for wrapper in list(cg_children):
                        prev_children.append(wrapper)
                child_tn.remove(cg)
                click_groups = child_tn.findall(Elements.P_PAR)
                continue
            i += 1

    def get_effects_by_shape(self, shape) -> list[IEffect]:
        self._load_effects()
        shape_id = shape.unique_id if hasattr(shape, 'unique_id') else None
        if shape_id is None:
            return []
        return [e for e in self._effects if e._get_target_shape_id() == shape_id]

    def get_effects_by_paragraph(self, paragraph) -> list[IEffect]:
        """Get effects that target a specific paragraph."""
        self._load_effects()

        # Resolve paragraph's parent shape and index
        p_elem = paragraph._p_element
        txbody = paragraph._txbody_element
        if txbody is None and p_elem is not None:
            txbody = p_elem.getparent()
        if txbody is None or p_elem is None:
            return []

        # Find paragraph index
        para_index = None
        for i, ap in enumerate(txbody.findall(Elements.A_P)):
            if ap is p_elem:
                para_index = i
                break
        if para_index is None:
            return []

        # Find shape id from parent element
        shape_elem = txbody.getparent()
        shape_id = None
        if shape_elem is not None:
            nv = shape_elem.find(f'{NS.P}nvSpPr')
            if nv is not None:
                cnv_pr = nv.find(f'{NS.P}cNvPr')
                if cnv_pr is not None:
                    shape_id = cnv_pr.get('id')
        if shape_id is None:
            return []

        # Filter effects: match shape id AND paragraph range
        result = []
        for eff in self._effects:
            if eff._ctn is None:
                continue
            for sp_tgt in eff._ctn.iter(Elements.P_SP_TGT):
                if sp_tgt.get('spid') != shape_id:
                    continue
                tx_el = sp_tgt.find(f'{NS.P}txEl')
                if tx_el is not None:
                    p_rg = tx_el.find(f'{NS.P}pRg')
                    if p_rg is not None:
                        st = p_rg.get('st')
                        end = p_rg.get('end')
                        if st is not None and int(st) <= para_index <= int(end):
                            result.append(eff)
                            break
        return result

    def get_count(self, shape) -> int:
        return len(self.get_effects_by_shape(shape))

    def __getitem__(self, index: int) -> IEffect:
        self._load_effects()
        return self._effects[index]

    def __len__(self):
        self._load_effects()
        return len(self._effects)

    def __iter__(self):
        self._load_effects()
        return iter(self._effects)
