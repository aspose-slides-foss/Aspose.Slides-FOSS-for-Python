from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .ITextAnimation import ITextAnimation
from .._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .BuildType import BuildType
    from .IEffect import IEffect


class TextAnimation(ITextAnimation):
    """Represent text animation."""

    def __init__(self):
        self._build_type_val = None
        self._effect_bg = None
        self._bld_p_elem = None
        self._slide_part = None
        self._shape_id = None
        self._grp_id = None
        self._effect_ref = None  # parent Effect for paragraph decomposition

    def _init_internal(self, bld_p_elem: Optional[ET._Element] = None,
                       slide_part=None, shape_id: Optional[str] = None,
                       grp_id: Optional[str] = None, effect=None):
        self._bld_p_elem = bld_p_elem
        self._slide_part = slide_part
        self._shape_id = shape_id
        self._grp_id = grp_id
        self._effect_ref = effect
        if bld_p_elem is not None:
            self._parse_build_type()

    def _parse_build_type(self):
        from .BuildType import BuildType
        build = self._bld_p_elem.get('build', '')
        _map = {
            'whole': BuildType.AS_ONE_OBJECT,
            'allAtOnce': BuildType.ALL_PARAGRAPHS_AT_ONCE,
            'p': BuildType.BY_LEVEL_PARAGRAPHS1,
            'cust': BuildType.BY_LEVEL_PARAGRAPHS1,
        }
        self._build_type_val = _map.get(build, BuildType.AS_ONE_OBJECT)

    def _ensure_bld_p(self, build_str: str):
        """Create <p:bldLst>/<p:bldP> in the timing element if not present."""
        if self._bld_p_elem is not None:
            return
        if self._slide_part is None or self._shape_id is None:
            return

        timing = self._slide_part.timing_element
        if timing is None:
            timing = self._slide_part.ensure_timing_element()

        bld_lst = timing.find(Elements.P_BLD_LST)
        if bld_lst is None:
            bld_lst = ET.SubElement(timing, Elements.P_BLD_LST)

        attrs = {'spid': self._shape_id, 'build': build_str,
                 'uiExpand': '1', 'animBg': '1'}
        if self._grp_id:
            attrs['grpId'] = self._grp_id
        self._bld_p_elem = ET.SubElement(bld_lst, Elements.P_BLD_P, **attrs)

    def _count_paragraphs(self) -> int:
        """Count paragraphs in the target shape."""
        if self._effect_ref is None or self._effect_ref._parent_slide is None:
            return 0
        shape = self._effect_ref.target_shape
        if shape is None:
            return 0
        try:
            tf = shape.text_frame
            if tf is not None:
                paras = tf.paragraphs
                if hasattr(paras, 'count'):
                    return paras.count
                return len(paras)
        except Exception:
            pass
        return 0

    def _generate_paragraph_effects(self, as_single_group=True):
        """Generate per-paragraph click-groups in the sequence.

        If as_single_group=True, generates ONE click-group whose pRg covers
        all paragraphs (st=0, end=last). This is BY_LEVEL_PARAGRAPHS1 behavior:
        first click shows shape, second click shows all text at once.

        If as_single_group=False, generates one click-group per paragraph.
        """
        if self._effect_ref is None:
            return
        seq = self._effect_ref._sequence
        if seq is None:
            return

        n_paras = self._count_paragraphs()
        if n_paras == 0:
            return

        # Get the effect's preset info from its cTn
        src_ctn = self._effect_ref._ctn
        if src_ctn is None:
            return

        preset_id = src_ctn.get('presetID', '10')
        preset_class = src_ctn.get('presetClass', 'entr')
        preset_subtype = src_ctn.get('presetSubtype', '0')
        grp_id = src_ctn.get('grpId', '1')

        # Find the filter from animEffect if present
        filter_name = 'fade'
        child_tn_src = src_ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn_src is not None:
            for ae in child_tn_src.findall(Elements.P_ANIM_EFFECT):
                f = ae.get('filter')
                if f:
                    filter_name = f
                    break

        seq_child_tn = seq._get_seq_child_tn_lst()

        if as_single_group:
            # All paragraphs in ONE click-group, playing simultaneously.
            # Each paragraph gets its own effect <p:par> inside the wrapper,
            # first one is clickEffect, rest are withEffect.
            groups = list(range(n_paras))
        else:
            groups = list(range(n_paras))

        id_base = self._slide_part.next_ctn_id()

        # Build one click-group containing all paragraph effects
        click_par = ET.SubElement(seq_child_tn, Elements.P_PAR)
        click_ctn = ET.SubElement(click_par, Elements.P_C_TN,
                                   id=str(id_base), fill='hold',
                                   nodeType='clickPar')
        st_cond = ET.SubElement(click_ctn, Elements.P_ST_COND_LST)
        ET.SubElement(st_cond, Elements.P_COND, delay='indefinite')
        click_children = ET.SubElement(click_ctn, Elements.P_CHILD_TN_LST)
        id_base += 1

        for idx, p_idx in enumerate(groups):
            # Each paragraph gets its own wrapper <p:par>
            wrapper_par = ET.SubElement(click_children, Elements.P_PAR)
            wrapper_ctn = ET.SubElement(wrapper_par, Elements.P_C_TN,
                                         id=str(id_base), fill='hold',
                                         nodeType='afterGroup')
            st2 = ET.SubElement(wrapper_ctn, Elements.P_ST_COND_LST)
            ET.SubElement(st2, Elements.P_COND, delay='0')
            wrapper_children = ET.SubElement(wrapper_ctn, Elements.P_CHILD_TN_LST)
            id_base += 1

            # Effect node — first is clickEffect, rest are withEffect for simultaneous play
            node_type = 'clickEffect' if (idx == 0 and not as_single_group) else 'withEffect'
            if as_single_group:
                node_type = 'clickEffect'

            effect_par = ET.SubElement(wrapper_children, Elements.P_PAR)
            effect_ctn = ET.SubElement(effect_par, Elements.P_C_TN,
                                        id=str(id_base),
                                        presetID=preset_id,
                                        presetClass=preset_class,
                                        presetSubtype=preset_subtype,
                                        fill='hold', grpId=grp_id,
                                        nodeType=node_type)
            st3 = ET.SubElement(effect_ctn, Elements.P_ST_COND_LST)
            ET.SubElement(st3, Elements.P_COND, delay='0')
            eff_children = ET.SubElement(effect_ctn, Elements.P_CHILD_TN_LST)
            id_base += 1

            # <p:set> targeting this paragraph
            set_elem = ET.SubElement(eff_children, Elements.P_SET)
            cbhvr = ET.SubElement(set_elem, Elements.P_C_BHVR)
            ctn = ET.SubElement(cbhvr, Elements.P_C_TN,
                                id=str(id_base), dur='1', fill='hold')
            st4 = ET.SubElement(ctn, Elements.P_ST_COND_LST)
            ET.SubElement(st4, Elements.P_COND, delay='0')
            tgt = ET.SubElement(cbhvr, Elements.P_TGT_EL)
            sp_tgt = ET.SubElement(tgt, Elements.P_SP_TGT, spid=self._shape_id)
            tx_el = ET.SubElement(sp_tgt, f'{NS.P}txEl')
            ET.SubElement(tx_el, f'{NS.P}pRg', st=str(p_idx), end=str(p_idx))
            anl = ET.SubElement(cbhvr, Elements.P_ATTR_NAME_LST)
            an = ET.SubElement(anl, Elements.P_ATTR_NAME)
            an.text = 'style.visibility'
            to_el = ET.SubElement(set_elem, Elements.P_TO)
            ET.SubElement(to_el, Elements.P_STR_VAL, val='visible')
            id_base += 1

            # <p:animEffect> targeting this paragraph
            anim_eff = ET.SubElement(eff_children, Elements.P_ANIM_EFFECT,
                                     transition='in', filter=filter_name)
            cbhvr2 = ET.SubElement(anim_eff, Elements.P_C_BHVR)
            ET.SubElement(cbhvr2, Elements.P_C_TN, id=str(id_base), dur='500')
            tgt2 = ET.SubElement(cbhvr2, Elements.P_TGT_EL)
            sp_tgt2 = ET.SubElement(tgt2, Elements.P_SP_TGT, spid=self._shape_id)
            tx_el2 = ET.SubElement(sp_tgt2, f'{NS.P}txEl')
            ET.SubElement(tx_el2, f'{NS.P}pRg', st=str(p_idx), end=str(p_idx))
            id_base += 1

    @property
    def build_type(self) -> BuildType:
        from .BuildType import BuildType
        return self._build_type_val or BuildType.AS_ONE_OBJECT

    @build_type.setter
    def build_type(self, value: BuildType):
        from .BuildType import BuildType
        self._build_type_val = value
        _map = {
            BuildType.AS_ONE_OBJECT: 'whole',
            BuildType.ALL_PARAGRAPHS_AT_ONCE: 'allAtOnce',
            BuildType.BY_LEVEL_PARAGRAPHS1: 'p',
            BuildType.BY_LEVEL_PARAGRAPHS2: 'p',
            BuildType.BY_LEVEL_PARAGRAPHS3: 'p',
            BuildType.BY_LEVEL_PARAGRAPHS4: 'p',
            BuildType.BY_LEVEL_PARAGRAPHS5: 'p',
        }
        build_str = _map.get(value, 'whole')
        if self._bld_p_elem is not None:
            if value == BuildType.AS_ONE_OBJECT:
                parent = self._bld_p_elem.getparent()
                if parent is not None:
                    parent.remove(self._bld_p_elem)
                    if len(parent) == 0:
                        gp = parent.getparent()
                        if gp is not None:
                            gp.remove(parent)
                self._bld_p_elem = None
            else:
                self._bld_p_elem.set('build', build_str)
        elif value != BuildType.AS_ONE_OBJECT:
            self._ensure_bld_p(build_str)

        # Generate per-paragraph sub-effects for paragraph build types
        if value in (BuildType.BY_LEVEL_PARAGRAPHS1, BuildType.ALL_PARAGRAPHS_AT_ONCE):
            # BY_LEVEL_PARAGRAPHS1: all paragraphs appear as one group on the next click
            self._generate_paragraph_effects(as_single_group=True)
        elif value in (BuildType.BY_LEVEL_PARAGRAPHS2, BuildType.BY_LEVEL_PARAGRAPHS3,
                       BuildType.BY_LEVEL_PARAGRAPHS4, BuildType.BY_LEVEL_PARAGRAPHS5):
            self._generate_paragraph_effects(as_single_group=False)

    @property
    def effect_animate_background_shape(self) -> IEffect:
        return self._effect_bg

    @effect_animate_background_shape.setter
    def effect_animate_background_shape(self, value: IEffect):
        self._effect_bg = value

    def add_effect(self, effect_type, subtype, trigger_type) -> IEffect:
        raise NotImplementedError("TextAnimation.add_effect not yet implemented")
