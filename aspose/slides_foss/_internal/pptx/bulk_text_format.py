"""
Helper for applying bulk text formatting to collections of cells.

Implements the logic behind IBulkTextFormattable.set_text_format for
Table, Row, and Column classes.  The three overloads accept:
  - PortionFormat  -> applied to every run (<a:rPr>) in every cell
  - ParagraphFormat -> applied to every paragraph (<a:pPr>) in every cell
  - TextFrameFormat -> applied to every text body (<a:bodyPr>) in every cell
"""
from __future__ import annotations

import copy
import lxml.etree as ET

from .constants import Elements


def _copy_xml_attrs(src: ET._Element, dst: ET._Element) -> None:
    """Copy all attributes from *src* to *dst*, overwriting existing ones."""
    for name, value in src.attrib.items():
        dst.set(name, value)


def _replace_or_add_child(parent: ET._Element, src_child: ET._Element) -> None:
    """Replace the first child with the same tag in *parent*, or append a copy."""
    existing = parent.find(src_child.tag)
    clone = copy.deepcopy(src_child)
    if existing is not None:
        parent.replace(existing, clone)
    else:
        parent.append(clone)


def _apply_rpr_to_element(src_rpr: ET._Element, target: ET._Element) -> None:
    """Copy attributes and children from source rPr to a target rPr-like element."""
    _copy_xml_attrs(src_rpr, target)
    for child in src_rpr:
        _replace_or_add_child(target, child)


def _apply_portion_format(cells, source) -> None:
    """Apply a PortionFormat / BasePortionFormat to every run and endParaRPr in every cell."""
    if not hasattr(source, '_rpr_element') or source._rpr_element is None:
        return
    src_rpr = source._rpr_element
    for cell in cells:
        txbody = cell._tc_element.find(Elements.A_TX_BODY)
        if txbody is None:
            continue
        for p in txbody.findall(Elements.A_P):
            # Apply to runs
            for r in p.findall(Elements.A_R):
                rpr = r.find(Elements.A_R_PR)
                if rpr is None:
                    rpr = ET.Element(Elements.A_R_PR)
                    r.insert(0, rpr)
                _apply_rpr_to_element(src_rpr, rpr)
            # Apply to endParaRPr (end-of-paragraph run properties)
            end_rpr = p.find(Elements.A_END_PARA_RPR)
            if end_rpr is not None:
                _apply_rpr_to_element(src_rpr, end_rpr)


def _apply_paragraph_format(cells, source) -> None:
    """Apply a ParagraphFormat to every paragraph in every cell."""
    if not hasattr(source, '_ppr_element') or source._ppr_element is None:
        return
    src_ppr = source._ppr_element
    for cell in cells:
        txbody = cell._tc_element.find(Elements.A_TX_BODY)
        if txbody is None:
            continue
        for p in txbody.findall(Elements.A_P):
            ppr = p.find(Elements.A_P_PR)
            if ppr is None:
                ppr = ET.Element(Elements.A_P_PR)
                p.insert(0, ppr)
            _copy_xml_attrs(src_ppr, ppr)
            for child in src_ppr:
                _replace_or_add_child(ppr, child)


def _apply_text_frame_format(cells, source) -> None:
    """Apply a TextFrameFormat to every text body in every cell.

    Also propagates the ``vert`` attribute to ``<a:tcPr>`` to match
    Aspose.Slides behaviour where vertical text type is mirrored on the
    cell properties element.
    """
    if not hasattr(source, '_txbody_element') or source._txbody_element is None:
        return
    # TextFrameFormat reads from <a:bodyPr> inside the txbody
    src_body_pr = source._txbody_element.find(Elements.A_BODY_PR)
    if src_body_pr is None:
        return
    vert_val = src_body_pr.get('vert')
    for cell in cells:
        txbody = cell._tc_element.find(Elements.A_TX_BODY)
        if txbody is None:
            continue
        body_pr = txbody.find(Elements.A_BODY_PR)
        if body_pr is None:
            body_pr = ET.SubElement(txbody, Elements.A_BODY_PR)
            # Insert as first child
            txbody.insert(0, body_pr)
        _copy_xml_attrs(src_body_pr, body_pr)
        for child in src_body_pr:
            _replace_or_add_child(body_pr, child)
        # Mirror vert on <a:tcPr>
        if vert_val is not None:
            tc_pr = cell._tc_element.find(Elements.A_TC_PR)
            if tc_pr is not None:
                tc_pr.set('vert', vert_val)


def apply_text_format(cells, source, slide_part) -> None:
    """
    Dispatch to the correct applier based on the runtime type of *source*.

    Args:
        cells: iterable of Cell objects (each must have ``_tc_element``).
        source: a PortionFormat, ParagraphFormat, or TextFrameFormat instance.
        slide_part: the SlidePart to call ``save()`` on afterwards.
    """
    from ...slides.PortionFormat import PortionFormat
    from ...slides.BasePortionFormat import BasePortionFormat
    from ...slides.ParagraphFormat import ParagraphFormat
    from ...slides.TextFrameFormat import TextFrameFormat

    if isinstance(source, (PortionFormat, BasePortionFormat)):
        _apply_portion_format(cells, source)
    elif isinstance(source, ParagraphFormat):
        _apply_paragraph_format(cells, source)
    elif isinstance(source, TextFrameFormat):
        _apply_text_frame_format(cells, source)
    else:
        raise TypeError(
            f"set_text_format expects PortionFormat, ParagraphFormat, "
            f"or TextFrameFormat, got {type(source).__name__}"
        )

    if slide_part:
        slide_part.save()
