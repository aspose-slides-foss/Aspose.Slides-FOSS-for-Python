from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .ITiming import ITiming

if TYPE_CHECKING:
    from .EffectRestartType import EffectRestartType
    from .EffectTriggerType import EffectTriggerType

from .._internal.pptx.constants import NS, Elements


class Timing(ITiming):
    """Represents animation timing."""

    def _init_internal(self, ctn_elem: ET._Element):
        """Initialize from a <p:cTn> element."""
        self._ctn = ctn_elem

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _update_next_wrapper_delay(self):
        """When duration or delay changes, update the next sibling wrapper's afterGroup delay."""
        # Navigate: effect cTn -> effect par -> wrapper childTnLst -> wrapper cTn -> wrapper par
        #   -> click-group childTnLst
        # Then find the next wrapper after ours and update its delay.
        effect_par = self._ctn.getparent()
        if effect_par is None:
            return
        wrapper_children = effect_par.getparent()  # wrapper's childTnLst
        if wrapper_children is None:
            return
        wrapper_ctn = wrapper_children.getparent()
        if wrapper_ctn is None:
            return
        wrapper_par = wrapper_ctn.getparent()
        if wrapper_par is None:
            return
        click_children = wrapper_par.getparent()  # click-group's childTnLst
        if click_children is None:
            return

        # Find our wrapper's index and the next one
        wrappers = list(click_children)
        try:
            idx = wrappers.index(wrapper_par)
        except ValueError:
            return
        if idx + 1 >= len(wrappers):
            return

        next_wrapper = wrappers[idx + 1]
        nw_ctn = next_wrapper.find(Elements.P_C_TN)
        if nw_ctn is None or nw_ctn.get('nodeType') != 'afterGroup':
            return

        # Compute: our wrapper delay + our effect delay + our effect duration
        our_wrapper_delay = 0
        wst = wrapper_ctn.find(Elements.P_ST_COND_LST)
        if wst is not None:
            wc = wst.find(Elements.P_COND)
            if wc is not None:
                try:
                    our_wrapper_delay = int(wc.get('delay', '0'))
                except ValueError:
                    pass

        our_effect_delay = 0
        cond = self._get_delay_cond()
        if cond is not None:
            try:
                our_effect_delay = int(cond.get('delay', '0'))
            except ValueError:
                pass

        our_dur = 500  # default
        child_tn = self._ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn is not None:
            for tag in (Elements.P_ANIM_EFFECT, Elements.P_ANIM):
                for bhvr in child_tn.findall(tag):
                    cb = bhvr.find(Elements.P_C_BHVR)
                    if cb is not None:
                        bctn = cb.find(Elements.P_C_TN)
                        if bctn is not None:
                            d = bctn.get('dur')
                            if d and d != 'indefinite':
                                try:
                                    our_dur = int(d)
                                except ValueError:
                                    pass
                                break

        total = our_wrapper_delay + our_effect_delay + our_dur
        nw_st = nw_ctn.find(Elements.P_ST_COND_LST)
        if nw_st is not None:
            nc = nw_st.find(Elements.P_COND)
            if nc is not None:
                nc.set('delay', str(total))

    def _get_delay_cond(self) -> Optional[ET._Element]:
        """Return the <p:cond> element from <p:stCondLst>, or None."""
        st = self._ctn.find(Elements.P_ST_COND_LST)
        if st is not None:
            return st.find(Elements.P_COND)
        return None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def accelerate(self) -> float:
        val = self._ctn.get('accel')
        if val is not None:
            return int(val) / 100000.0
        return 0.0

    @accelerate.setter
    def accelerate(self, value: float):
        self._ctn.set('accel', str(int(value * 100000)))

    @property
    def decelerate(self) -> float:
        val = self._ctn.get('decel')
        if val is not None:
            return int(val) / 100000.0
        return 0.0

    @decelerate.setter
    def decelerate(self, value: float):
        self._ctn.set('decel', str(int(value * 100000)))

    @property
    def auto_reverse(self) -> bool:
        return self._ctn.get('autoRev') == '1'

    @auto_reverse.setter
    def auto_reverse(self, value: bool):
        self._ctn.set('autoRev', '1' if value else '0')

    @property
    def duration(self) -> float:
        # First check behavior children (animEffect, anim) for explicit duration
        child_tn = self._ctn.find(Elements.P_CHILD_TN_LST)
        if child_tn is not None:
            for bhvr_tag in (Elements.P_ANIM_EFFECT, Elements.P_ANIM):
                for bhvr in child_tn.findall(bhvr_tag):
                    cb = bhvr.find(Elements.P_C_BHVR)
                    if cb is not None:
                        bctn = cb.find(Elements.P_C_TN)
                        if bctn is not None:
                            val = bctn.get('dur')
                            if val is not None and val != 'indefinite':
                                return int(val) / 1000.0
        # Fall back to cTn dur
        val = self._ctn.get('dur')
        if val is None or val == 'indefinite':
            return -1.0
        return int(val) / 1000.0

    @duration.setter
    def duration(self, value: float):
        dur_str = 'indefinite' if value < 0 else str(int(value * 1000))
        # Set duration on behavior children (animEffect, anim), NOT on the effect cTn.
        # The effect cTn dur controls the overall timeline container; the behavior
        # cTn dur controls the actual visual effect duration.
        child_tn = self._ctn.find(Elements.P_CHILD_TN_LST)
        updated = False
        if child_tn is not None:
            for bhvr_tag in (Elements.P_ANIM_EFFECT, Elements.P_ANIM):
                for bhvr in child_tn.findall(bhvr_tag):
                    cb = bhvr.find(Elements.P_C_BHVR)
                    if cb is not None:
                        bctn = cb.find(Elements.P_C_TN)
                        if bctn is not None:
                            bctn.set('dur', dur_str)
                            updated = True
        if not updated:
            # No behavior children — set on cTn directly (e.g., path effects)
            self._ctn.set('dur', dur_str)
        # Update next sibling wrapper's afterGroup delay if it exists
        self._update_next_wrapper_delay()

    @property
    def repeat_count(self) -> float:
        val = self._ctn.get('repeatCount')
        if val is None:
            return 1.0
        if val == 'indefinite':
            return -1.0
        return int(val) / 1000.0

    @repeat_count.setter
    def repeat_count(self, value: float):
        if value < 0:
            self._ctn.set('repeatCount', 'indefinite')
        else:
            self._ctn.set('repeatCount', str(int(value * 1000)))

    @property
    def repeat_until_end_slide(self) -> bool:
        return self._ctn.get('repeatCount') == 'indefinite' and self._ctn.get('repeatDur') == 'indefinite'

    @repeat_until_end_slide.setter
    def repeat_until_end_slide(self, value: bool):
        if value:
            self._ctn.set('repeatCount', 'indefinite')
            self._ctn.set('repeatDur', 'indefinite')

    @property
    def repeat_until_next_click(self) -> bool:
        return self._ctn.get('repeatCount') == 'indefinite' and self._ctn.get('repeatDur') != 'indefinite'

    @repeat_until_next_click.setter
    def repeat_until_next_click(self, value: bool):
        if value:
            self._ctn.set('repeatCount', 'indefinite')
            if 'repeatDur' in self._ctn.attrib:
                del self._ctn.attrib['repeatDur']

    @property
    def repeat_duration(self) -> float:
        val = self._ctn.get('repeatDur')
        if val is None or val == 'indefinite':
            return -1.0
        return int(val) / 1000.0

    @repeat_duration.setter
    def repeat_duration(self, value: float):
        if value < 0:
            self._ctn.set('repeatDur', 'indefinite')
        else:
            self._ctn.set('repeatDur', str(int(value * 1000)))

    @property
    def restart(self) -> EffectRestartType:
        from .EffectRestartType import EffectRestartType
        val = self._ctn.get('restart')
        _map = {
            'always': EffectRestartType.ALWAYS,
            'whenNotActive': EffectRestartType.WHEN_NOT_ACTIVE,
            'never': EffectRestartType.NEVER,
        }
        return _map.get(val, EffectRestartType.NOT_DEFINED)

    @restart.setter
    def restart(self, value: EffectRestartType):
        from .EffectRestartType import EffectRestartType
        _map = {
            EffectRestartType.ALWAYS: 'always',
            EffectRestartType.WHEN_NOT_ACTIVE: 'whenNotActive',
            EffectRestartType.NEVER: 'never',
        }
        xml_val = _map.get(value)
        if xml_val:
            self._ctn.set('restart', xml_val)
        elif 'restart' in self._ctn.attrib:
            del self._ctn.attrib['restart']

    @property
    def rewind(self) -> bool:
        fill = self._ctn.get('fill')
        return fill == 'remove'

    @rewind.setter
    def rewind(self, value: bool):
        self._ctn.set('fill', 'remove' if value else 'hold')

    @property
    def speed(self) -> float:
        val = self._ctn.get('spd')
        if val is not None:
            return int(val) / 100000.0
        return 1.0

    @speed.setter
    def speed(self, value: float):
        self._ctn.set('spd', str(int(value * 100000)))

    @property
    def trigger_delay_time(self) -> float:
        cond = self._get_delay_cond()
        if cond is not None:
            delay = cond.get('delay', '0')
            if delay == 'indefinite':
                return -1.0
            try:
                return int(delay) / 1000.0
            except ValueError:
                return 0.0
        return 0.0

    @trigger_delay_time.setter
    def trigger_delay_time(self, value: float):
        cond = self._get_delay_cond()
        if cond is None:
            st = self._ctn.find(Elements.P_ST_COND_LST)
            if st is None:
                st = ET.SubElement(self._ctn, Elements.P_ST_COND_LST)
            cond = ET.SubElement(st, Elements.P_COND)
        cond.set('delay', str(int(value * 1000)))
        self._update_next_wrapper_delay()

    @property
    def trigger_type(self) -> EffectTriggerType:
        from .EffectTriggerType import EffectTriggerType
        from .._internal.pptx.animation_mappings import NODE_TYPE_TO_TRIGGER
        node_type = self._ctn.get('nodeType', '')
        return NODE_TYPE_TO_TRIGGER.get(node_type, EffectTriggerType.ON_CLICK)

    @trigger_type.setter
    def trigger_type(self, value: EffectTriggerType):
        from .._internal.pptx.animation_mappings import TRIGGER_TO_NODE_TYPE
        xml_val = TRIGGER_TO_NODE_TYPE.get(value)
        if xml_val:
            self._ctn.set('nodeType', xml_val)
