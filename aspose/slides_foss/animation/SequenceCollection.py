from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import lxml.etree as ET
from .ISequenceCollection import ISequenceCollection
from .._internal.base_collection import BaseCollection
from .._internal.pptx.constants import Elements

if TYPE_CHECKING:
    from .ISequence import ISequence
    from .Sequence import Sequence


class SequenceCollection(BaseCollection, ISequenceCollection):
    """Represents collection of interactive sequences."""

    def _init_internal(self, root_child_tn_lst: ET._Element, slide_part, parent_slide):
        """Initialize from the root <p:childTnLst> that contains all <p:seq> elements.

        Interactive sequences are <p:seq> elements with nodeType='interactiveSeq'.
        """
        self._root_child_tn = root_child_tn_lst
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._items: list = []
        self._parse()

    def _parse(self):
        from .Sequence import Sequence as SequenceImpl
        if self._root_child_tn is None:
            return
        for seq_elem in self._root_child_tn.findall(Elements.P_SEQ):
            seq_ctn = seq_elem.find(Elements.P_C_TN)
            if seq_ctn is not None and seq_ctn.get('nodeType') == 'interactiveSeq':
                seq = SequenceImpl()
                seq._init_internal(seq_elem, self._slide_part, self._parent_slide, is_main=False)
                self._items.append(seq)

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._items)

    def add(self, shape_trigger) -> ISequence:
        """Create a new interactive sequence triggered by a shape click."""
        from .Sequence import Sequence as SequenceImpl

        # Ensure timing structure exists
        self._slide_part.ensure_timing_element()

        # Get the root <p:childTnLst>
        timing = self._slide_part.timing_element
        tn_lst = timing.find(Elements.P_TN_LST)
        root_par = tn_lst.find(Elements.P_PAR)
        root_ctn = root_par.find(Elements.P_C_TN)
        root_child_tn = root_ctn.find(Elements.P_CHILD_TN_LST)
        if root_child_tn is None:
            root_child_tn = ET.SubElement(root_ctn, Elements.P_CHILD_TN_LST)
        self._root_child_tn = root_child_tn

        shape_id = str(shape_trigger.unique_id) if hasattr(shape_trigger, 'unique_id') else '0'
        id_base = self._slide_part.next_ctn_id()

        # Build interactive <p:seq>
        seq_elem = ET.SubElement(root_child_tn, Elements.P_SEQ, concurrent='1', nextAc='seek')
        seq_ctn = ET.SubElement(seq_elem, Elements.P_C_TN,
                                 id=str(id_base),
                                 restart='whenNotActive',
                                 fill='hold',
                                 evtFilter='cancelBubble',
                                 nodeType='interactiveSeq')

        # Start condition: onClick on trigger shape
        st_cond = ET.SubElement(seq_ctn, Elements.P_ST_COND_LST)
        cond = ET.SubElement(st_cond, Elements.P_COND, evt='onClick', delay='0')
        tgt = ET.SubElement(cond, Elements.P_TGT_EL)
        ET.SubElement(tgt, Elements.P_SP_TGT, spid=shape_id)

        # End sync
        end_sync = ET.SubElement(seq_ctn, Elements.P_END_SYNC, evt='end', delay='0')
        rtn = ET.SubElement(end_sync, Elements.P_RTN, val='all')

        # Child time node list
        ET.SubElement(seq_ctn, Elements.P_CHILD_TN_LST)

        # Next condition — re-trigger on click of the same trigger shape
        next_cond = ET.SubElement(seq_elem, Elements.P_NEXT_COND_LST)
        nc = ET.SubElement(next_cond, Elements.P_COND, evt='onClick', delay='0')
        tgt2 = ET.SubElement(nc, Elements.P_TGT_EL)
        ET.SubElement(tgt2, Elements.P_SP_TGT, spid=shape_id)

        # Create Sequence wrapper
        seq = SequenceImpl()
        seq._init_internal(seq_elem, self._slide_part, self._parent_slide, is_main=False)
        self._items.append(seq)
        return seq

    def remove(self, item) -> None:
        if item in self._items:
            self._items.remove(item)
            if self._root_child_tn is not None:
                self._root_child_tn.remove(item._seq_elem)

    def remove_at(self, index) -> None:
        item = self._items.pop(index)
        if self._root_child_tn is not None:
            self._root_child_tn.remove(item._seq_elem)

    def clear(self) -> None:
        for item in self._items:
            if self._root_child_tn is not None:
                try:
                    self._root_child_tn.remove(item._seq_elem)
                except ValueError:
                    pass
        self._items.clear()

    def __getitem__(self, index: int) -> Sequence:
        return self._items[index]

    def __len__(self):
        return len(self._items)
