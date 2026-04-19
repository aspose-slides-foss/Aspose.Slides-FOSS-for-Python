from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

from .._internal.pptx.constants import Elements


class Behavior(IBehavior):
    """Represent base class behavior of effect."""

    def _init_internal(self, elem: ET._Element):
        """Initialize from a behavior XML element (<p:set>, <p:anim>, etc.)."""
        self._elem = elem
        self._timing_cache = None

    def _get_cbhvr(self) -> Optional[ET._Element]:
        """Get the <p:cBhvr> child element."""
        return self._elem.find(Elements.P_C_BHVR)

    def _get_cbhvr_ctn(self) -> Optional[ET._Element]:
        """Get the <p:cTn> inside <p:cBhvr>."""
        cbhvr = self._get_cbhvr()
        if cbhvr is not None:
            return cbhvr.find(Elements.P_C_TN)
        return None

    @property
    def accumulate(self) -> NullableBool:
        from ..NullableBool import NullableBool
        cbhvr = self._get_cbhvr()
        if cbhvr is not None:
            val = cbhvr.get('accumulate')
            if val == 'always':
                return NullableBool.TRUE
            if val == 'none':
                return NullableBool.FALSE
        return NullableBool.NOT_DEFINED

    @accumulate.setter
    def accumulate(self, value: NullableBool):
        from ..NullableBool import NullableBool
        cbhvr = self._get_cbhvr()
        if cbhvr is not None:
            if value == NullableBool.TRUE:
                cbhvr.set('accumulate', 'always')
            elif value == NullableBool.FALSE:
                cbhvr.set('accumulate', 'none')
            elif 'accumulate' in cbhvr.attrib:
                del cbhvr.attrib['accumulate']

    @property
    def additive(self) -> BehaviorAdditiveType:
        from .BehaviorAdditiveType import BehaviorAdditiveType
        cbhvr = self._get_cbhvr()
        if cbhvr is not None:
            val = cbhvr.get('additive')
            _map = {
                'base': BehaviorAdditiveType.BASE,
                'sum': BehaviorAdditiveType.SUM,
                'repl': BehaviorAdditiveType.REPLACE,
                'mult': BehaviorAdditiveType.MULTIPLY,
                'none': BehaviorAdditiveType.NONE,
            }
            return _map.get(val, BehaviorAdditiveType.NOT_DEFINED)
        return BehaviorAdditiveType.NOT_DEFINED

    @additive.setter
    def additive(self, value: BehaviorAdditiveType):
        from .BehaviorAdditiveType import BehaviorAdditiveType
        cbhvr = self._get_cbhvr()
        if cbhvr is not None:
            _map = {
                BehaviorAdditiveType.BASE: 'base',
                BehaviorAdditiveType.SUM: 'sum',
                BehaviorAdditiveType.REPLACE: 'repl',
                BehaviorAdditiveType.MULTIPLY: 'mult',
                BehaviorAdditiveType.NONE: 'none',
            }
            xml_val = _map.get(value)
            if xml_val:
                cbhvr.set('additive', xml_val)
            elif 'additive' in cbhvr.attrib:
                del cbhvr.attrib['additive']

    @property
    def properties(self) -> IBehaviorPropertyCollection:
        from .BehaviorPropertyCollection import BehaviorPropertyCollection
        coll = BehaviorPropertyCollection()
        cbhvr = self._get_cbhvr()
        if cbhvr is not None:
            attr_lst = cbhvr.find(Elements.P_ATTR_NAME_LST)
            coll._init_internal(attr_lst, cbhvr)
        else:
            coll._init_internal(None, None)
        return coll

    @property
    def timing(self) -> ITiming:
        if self._timing_cache is None:
            from .Timing import Timing
            ctn = self._get_cbhvr_ctn()
            if ctn is not None:
                t = Timing()
                t._init_internal(ctn)
                self._timing_cache = t
        return self._timing_cache

    @timing.setter
    def timing(self, value: ITiming):
        self._timing_cache = value
