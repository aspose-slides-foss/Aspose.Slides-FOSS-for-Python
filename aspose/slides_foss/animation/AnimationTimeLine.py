from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from ..IAnimationTimeLine import IAnimationTimeLine
from .._internal.pptx.constants import Elements

if TYPE_CHECKING:
    from .ISequence import ISequence
    from .ISequenceCollection import ISequenceCollection
    from .ITextAnimationCollection import ITextAnimationCollection


class AnimationTimeLine(IAnimationTimeLine):
    """Represents timeline of animation."""

    def _init_internal(self, slide_part, parent_slide):
        """Initialize from a slide part.

        Args:
            slide_part: SlidePart (or LayoutSlidePart/MasterSlidePart).
            parent_slide: The Slide/LayoutSlide/MasterSlide object.
        """
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._main_sequence_cache = None
        self._interactive_sequences_cache = None
        self._text_animation_collection_cache = None

    def _get_root_child_tn_lst(self) -> Optional[ET._Element]:
        """Navigate to the root <p:childTnLst> inside <p:timing>."""
        timing = self._slide_part.timing_element
        if timing is None:
            return None
        tn_lst = timing.find(Elements.P_TN_LST)
        if tn_lst is None:
            return None
        root_par = tn_lst.find(Elements.P_PAR)
        if root_par is None:
            return None
        root_ctn = root_par.find(Elements.P_C_TN)
        if root_ctn is None:
            return None
        return root_ctn.find(Elements.P_CHILD_TN_LST)

    def _find_main_seq(self) -> Optional[ET._Element]:
        """Find the <p:seq> with nodeType='mainSeq'."""
        child_tn = self._get_root_child_tn_lst()
        if child_tn is None:
            return None
        for seq_elem in child_tn.findall(Elements.P_SEQ):
            seq_ctn = seq_elem.find(Elements.P_C_TN)
            if seq_ctn is not None and seq_ctn.get('nodeType') == 'mainSeq':
                return seq_elem
        return None

    @property
    def interactive_sequences(self) -> ISequenceCollection:
        if self._interactive_sequences_cache is None:
            from .SequenceCollection import SequenceCollection
            sc = SequenceCollection()
            child_tn = self._get_root_child_tn_lst()
            sc._init_internal(child_tn, self._slide_part, self._parent_slide)
            self._interactive_sequences_cache = sc
        return self._interactive_sequences_cache

    @property
    def main_sequence(self) -> ISequence:
        if self._main_sequence_cache is None:
            from .Sequence import Sequence
            seq_elem = self._find_main_seq()
            if seq_elem is None:
                seq_elem = self._slide_part.ensure_main_sequence()
            seq = Sequence()
            seq._init_internal(seq_elem, self._slide_part, self._parent_slide, is_main=True)
            self._main_sequence_cache = seq
        return self._main_sequence_cache

    @property
    def text_animation_collection(self) -> ITextAnimationCollection:
        if self._text_animation_collection_cache is None:
            from .TextAnimationCollection import TextAnimationCollection
            tac = TextAnimationCollection()
            timing = self._slide_part.timing_element
            bld_lst = None
            if timing is not None:
                bld_lst = timing.find(Elements.P_BLD_LST)
            tac._init_internal(bld_lst)
            self._text_animation_collection_cache = tac
        return self._text_animation_collection_cache
