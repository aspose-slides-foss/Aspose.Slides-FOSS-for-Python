"""ECMA-376 child sequences, and an ordered insert built on them.

The DrawingML complex types these writers produce are ``xsd:sequence``: the
order of the children is part of the schema, not a matter of taste.  Children
are created lazily, as the caller sets the properties that need them, so
appending makes the order of the file the order the caller happened to make the
assignments in.  The same formatting then produces a valid file or an invalid
one depending on the order it was expressed in, which is worse than consistent
breakage because the failure will not reproduce for whoever reports it.

``insert_in_order`` puts a new child at the position its sequence gives it.
Containers that are not listed here, and children that are not in their
container's sequence, are appended as before.

Sequences are keyed by the container's local name because the same type appears
under more than one namespace prefix: shape properties are ``p:spPr`` on a
slide, ``c:spPr`` in a chart part and ``a:spPr`` in a table cell, and all three
take the same ``a``-namespaced children.
"""

from __future__ import annotations

import lxml.etree as ET

from .constants import NS

#: EG_FillProperties — one fill, whichever kind, occupies a single position.
_FILL = ("noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill")

#: EG_EffectProperties.
_EFFECT = ("effectLst", "effectDag")


def _sequence(*positions) -> dict[str, int]:
    """Expand a sequence of names and choice groups into ``{tag: rank}``."""
    ranks: dict[str, int] = {}
    for rank, position in enumerate(positions):
        names = (position,) if isinstance(position, str) else position
        for name in names:
            ranks[f"{NS.A}{name}"] = rank
    return ranks


# CT_TextCharacterProperties — ECMA-376 Part 1, 21.1.2.3.9.
_TEXT_CHARACTER_PROPERTIES = _sequence(
    "ln", _FILL, _EFFECT, "highlight", ("uLnTx", "uLn"), ("uFillTx", "uFill"),
    "latin", "ea", "cs", "sym", "hlinkClick", "hlinkMouseOver", "rtl", "extLst",
)

CHILD_SEQUENCES: dict[str, dict[str, int]] = {
    # CT_TextCharacterProperties, under each of its three element names.
    "rPr": _TEXT_CHARACTER_PROPERTIES,
    "defRPr": _TEXT_CHARACTER_PROPERTIES,
    "endParaRPr": _TEXT_CHARACTER_PROPERTIES,
    # CT_ShapeProperties — 20.1.2.2.35.
    "spPr": _sequence(
        "xfrm", ("custGeom", "prstGeom"), _FILL, "ln", _EFFECT,
        "scene3d", "sp3d", "extLst",
    ),
    # CT_LineProperties — 20.1.2.2.24.  Aliased below onto every element name
    # that carries it: the underline line and the six table cell borders.
    "ln": _sequence(
        _FILL, ("prstDash", "custDash"), ("round", "bevel", "miter"),
        "headEnd", "tailEnd", "extLst",
    ),
    # CT_TableCellProperties — 21.1.3.17.
    "tcPr": _sequence(
        "lnL", "lnR", "lnT", "lnB", "lnTlToBr", "lnBlToTr", "cell3D", _FILL,
        "headers", "extLst",
    ),
    # CT_TableProperties — 21.1.3.15.
    "tblPr": _sequence(_FILL, _EFFECT, ("tableStyle", "tableStyleId"), "extLst"),
    # CT_BackgroundProperties — 19.3.1.2.
    "bgPr": _sequence(_FILL, _EFFECT, "extLst"),
    # CT_TextUnderlineFillGroupWrapper and CT_FillOverlayEffect: one fill.
    "uFill": _sequence(_FILL),
    "fillOverlay": _sequence(_FILL),
    # CT_Scene3D — 20.1.4.1.26.
    "scene3d": _sequence("camera", "lightRig", "backdrop", "extLst"),
    # CT_NonVisualDrawingProps — 20.1.2.2.8.
    "cNvPr": _sequence("hlinkClick", "hlinkMouseOver", "extLst"),
}

for _line_element in ("uLn", "lnL", "lnR", "lnT", "lnB", "lnTlToBr", "lnBlToTr"):
    CHILD_SEQUENCES[_line_element] = CHILD_SEQUENCES["ln"]
del _line_element


def _local_name(tag: str) -> str:
    return tag.rsplit('}', 1)[-1]


def insert_in_order(parent: ET._Element, element: ET._Element) -> ET._Element:
    """Insert ``element`` under ``parent`` where its schema sequence puts it."""
    ranks = CHILD_SEQUENCES.get(_local_name(parent.tag))
    rank = ranks.get(element.tag) if ranks else None
    if rank is None:
        parent.append(element)
        return element
    for index, child in enumerate(parent):
        child_rank = ranks.get(child.tag)
        if child_rank is not None and child_rank > rank:
            parent.insert(index, element)
            return element
    parent.append(element)
    return element


def sub_element_in_order(parent: ET._Element, tag: str, **attributes) -> ET._Element:
    """``ET.SubElement`` that respects the container's schema sequence."""
    element = ET.Element(tag)
    for name, value in attributes.items():
        element.set(name, value)
    return insert_in_order(parent, element)
