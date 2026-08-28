"""Reading and writing ``<a:hlinkClick>`` and ``<a:hlinkMouseOver>``.

A hyperlink is two things that have to stay in step: the element inside the
run properties or the non-visual drawing properties, and an *external*
relationship in the owning part's ``.rels`` that its ``r:id`` resolves to.
Writing one without the other produces a package a strict consumer rejects, so
both sides live here and no caller assembles them by hand.
"""

from __future__ import annotations

import lxml.etree as ET

from ..opc.relationships import REL_TYPES
from .child_order import sub_element_in_order
from .constants import NS

R_ID = f"{NS.R}id"


def _rels_manager(part):
    return getattr(part, '_rels_manager', None) if part is not None else None


def get_hyperlink(parent: ET._Element, part, tag: str):
    """Return the hyperlink held by ``parent``'s ``tag`` child, or ``None``."""
    from ...Hyperlink import Hyperlink

    element = parent.find(tag) if parent is not None else None
    if element is None:
        return None
    rels = _rels_manager(part)
    rel_id = element.get(R_ID)
    target = ''
    if rel_id and rels is not None:
        relationship = rels.get_relationship(rel_id)
        if relationship is not None:
            target = relationship.target
    return Hyperlink(
        target,
        tooltip=element.get('tooltip'),
        target_frame=element.get('tgtFrame'),
    )


def set_hyperlink(parent: ET._Element, part, tag: str, value) -> None:
    """Set or clear the hyperlink held by ``parent``'s ``tag`` child.

    ``value`` is a URL string, an :class:`~aspose.slides_foss.Hyperlink`, or
    ``None`` to remove the link and the relationship it owns.
    """
    from ...Hyperlink import Hyperlink

    if parent is None:
        raise ValueError('this object is not attached to a slide, so a hyperlink cannot be stored')

    rels = _rels_manager(part)
    existing = parent.find(tag)
    if existing is not None:
        old_rel_id = existing.get(R_ID)
        if old_rel_id and rels is not None:
            rels.remove_relationship(old_rel_id)
        parent.remove(existing)

    if value is None:
        if rels is not None:
            rels.save()
        return

    link = Hyperlink(value) if isinstance(value, str) else value
    url = link.external_url
    if not url:
        raise ValueError('a hyperlink needs a target URL')
    if rels is None:
        raise ValueError(
            'this object is not attached to a slide, so the hyperlink relationship '
            'cannot be created; add the shape to a slide first'
        )

    rel_id = rels.add_relationship(REL_TYPES['hyperlink'], url, target_mode='External')
    rels.save()

    element = sub_element_in_order(parent, tag)
    element.set(R_ID, rel_id)
    if link.tooltip:
        element.set('tooltip', link.tooltip)
    if link.target_frame:
        element.set('tgtFrame', link.target_frame)
