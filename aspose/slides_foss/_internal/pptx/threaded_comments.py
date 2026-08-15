"""Writing modern threaded comments.

A reply is not expressible in the classic comment list: ``CT_Comment`` has no
attribute for a parent, so a reply written there is simply a second, unrelated
comment and the thread is lost the moment the file is saved.  PowerPoint 2018
moved threading into parts of its own — ``ppt/threadedComments/`` for the
threads and ``ppt/authors.xml`` for the people in them — and that is where a
reply has to go to survive.

The classic list is still written, because readers older than 2018 show only
that, and its replies are linked with the ``p15:threadingInfo`` extension the
same versions of PowerPoint use.  What is *not* written is a ``parentCmId``
attribute on ``p:cm``: it is not in the schema and no consumer renders it.

Identifiers are derived from the slide, the author and the comment index
rather than generated fresh, so saving the same deck twice produces the same
identifiers instead of churning the file.
"""

from __future__ import annotations

import uuid
from typing import Optional

import lxml.etree as ET

from ..opc import ContentTypesManager, RelationshipsManager
from ..opc.content_types import CONTENT_TYPES
from ..opc.relationships import REL_TYPES
from .constants import NAMESPACES

_P_NS = NAMESPACES['p']
_A_NS = NAMESPACES['a']
_P15_NS = NAMESPACES['p15']
_P188_NS = NAMESPACES['p188']

_P = f"{{{_P_NS}}}"
_A = f"{{{_A_NS}}}"
_P15 = f"{{{_P15_NS}}}"
_P188 = f"{{{_P188_NS}}}"

AUTHORS_PART_NAME = 'ppt/authors.xml'
PRESENTATION_PART_NAME = 'ppt/presentation.xml'

#: The `p:ext` uri PowerPoint uses for threading information on a classic comment.
THREADING_INFO_URI = '{C676402C-5697-4E1C-873F-D02D1690AC5C}'

#: Namespace for the derived identifiers, so they are stable across saves.
_ID_NAMESPACE = uuid.UUID('6f9619ff-8b86-d011-b42d-00c04fc964ff')


def _guid(*parts) -> str:
    return '{%s}' % str(uuid.uuid5(_ID_NAMESPACE, '|'.join(str(p) for p in parts))).upper()


def comment_guid(slide_part_name: str, author_id, idx) -> str:
    """The threaded identifier of one classic comment."""
    return _guid('comment', slide_part_name, author_id, idx)


def author_guid(author_id, name: str) -> str:
    """The threaded identifier of one comment author."""
    return _guid('author', author_id, name)


def parent_of(comment_elem: ET._Element) -> Optional[tuple]:
    """The ``(authorId, idx)`` this classic comment replies to, if any."""
    for ext in comment_elem.iter(f"{_P}ext"):
        if ext.get('uri') != THREADING_INFO_URI:
            continue
        parent = ext.find(f"{_P15}threadingInfo/{_P15}parentCm")
        if parent is not None:
            return parent.get('authorId'), parent.get('idx')
    return None


def set_parent(comment_elem: ET._Element, parent: Optional[tuple]) -> None:
    """Record, or clear, the comment this classic comment replies to."""
    for ext_lst in comment_elem.findall(f"{_P}extLst"):
        for ext in list(ext_lst):
            if ext.get('uri') == THREADING_INFO_URI:
                ext_lst.remove(ext)
        if len(ext_lst) == 0:
            comment_elem.remove(ext_lst)
    # The invalid attribute earlier versions of this library wrote.
    comment_elem.attrib.pop('parentCmId', None)
    if parent is None:
        return

    author_id, idx = parent
    ext_lst = comment_elem.find(f"{_P}extLst")
    if ext_lst is None:
        ext_lst = ET.SubElement(comment_elem, f"{_P}extLst")
    ext = ET.SubElement(ext_lst, f"{_P}ext")
    ext.set('uri', THREADING_INFO_URI)
    info = ET.SubElement(ext, f"{_P15}threadingInfo", nsmap={'p15': _P15_NS})
    info.set('timeZoneBias', '0')
    parent_cm = ET.SubElement(info, f"{_P15}parentCm")
    parent_cm.set('authorId', str(author_id))
    parent_cm.set('idx', str(idx))


def _serialise(root: ET._Element) -> bytes:
    ET.indent(root, space='  ')
    return ET.tostring(
        root, pretty_print=True, xml_declaration=True, encoding='UTF-8', standalone=True,
    )


def _relative_target(from_part: str, to_part: str) -> str:
    from .comments_part import CommentsPart
    return CommentsPart._compute_relative_target(from_part, to_part)


def _ensure_relationship(package, source_part: str, rel_type: str, target: str) -> None:
    """Add the relationship unless the part already has one of that type."""
    rels = RelationshipsManager(package, source_part)
    if rels.get_relationships_by_type(rel_type):
        return
    rels.add_relationship(rel_type, target)
    rels.save()


def _ensure_override(package, part_name: str, content_type: str) -> None:
    content_types = ContentTypesManager(package)
    if content_types.get_content_type(part_name) == content_type:
        return
    content_types.add_override(part_name, content_type)
    content_types.save()


def _authors(package) -> dict:
    """``{authorId: (name, initials)}`` from the classic authors part."""
    from .comment_authors_part import PART_NAME as AUTHORS_CLASSIC

    data = package.get_part(AUTHORS_CLASSIC)
    if not data:
        return {}
    root = ET.fromstring(data)
    return {
        element.get('id', '0'): (element.get('name', ''), element.get('initials', ''))
        for element in root.findall(f"{_P}cmAuthor")
    }


def _write_authors_part(package, authors: dict) -> None:
    root = ET.Element(f"{_P188}authorLst", nsmap={'p188': _P188_NS})
    for author_id, (name, initials) in sorted(authors.items(), key=lambda item: item[0]):
        element = ET.SubElement(root, f"{_P188}author")
        element.set('id', author_guid(author_id, name))
        element.set('name', name)
        element.set('initials', initials)
        element.set('userId', name)
        element.set('providerId', 'None')
    package.set_part(AUTHORS_PART_NAME, _serialise(root))
    _ensure_override(package, AUTHORS_PART_NAME, CONTENT_TYPES['authors'])
    _ensure_relationship(
        package, PRESENTATION_PART_NAME, REL_TYPES['authors'],
        _relative_target(PRESENTATION_PART_NAME, AUTHORS_PART_NAME),
    )


def _text_body(parent: ET._Element, text: str) -> None:
    body = ET.SubElement(parent, f"{_P188}txBody")
    ET.SubElement(body, f"{_A}bodyPr")
    ET.SubElement(body, f"{_A}lstStyle")
    paragraph = ET.SubElement(body, f"{_A}p")
    run = ET.SubElement(paragraph, f"{_A}r")
    run_text = ET.SubElement(run, f"{_A}t")
    run_text.text = text


def _threaded_part_name(package, slide_part_name: str) -> str:
    """The threaded part this slide already uses, or the next free name."""
    rels = RelationshipsManager(package, slide_part_name)
    existing = rels.get_relationships_by_type(REL_TYPES['threadedComment'])
    if existing:
        from .comments_part import CommentsPart
        return CommentsPart._resolve_target(slide_part_name, existing[0].target)

    number = 1
    while package.has_part(f"ppt/threadedComments/threadedComment{number}.xml"):
        number += 1
    return f"ppt/threadedComments/threadedComment{number}.xml"


def _write_thread(package, slide_part_name: str, comments_part_name: str, authors: dict) -> None:
    data = package.get_part(comments_part_name)
    if not data:
        return
    comments = ET.fromstring(data).findall(f"{_P}cm")
    if not comments:
        return

    root = ET.Element(f"{_P188}cmLst", nsmap={'a': _A_NS, 'p188': _P188_NS})
    for comment in comments:
        author_id = comment.get('authorId', '0')
        idx = comment.get('idx', '0')
        name = authors.get(author_id, ('', ''))[0]

        element = ET.SubElement(root, f"{_P188}cm")
        element.set('id', comment_guid(slide_part_name, author_id, idx))
        parent = parent_of(comment)
        if parent is not None:
            element.set('parentId', comment_guid(slide_part_name, parent[0], parent[1]))
        element.set('authorId', author_guid(author_id, name))
        created = comment.get('dt')
        if created:
            element.set('created', created)

        position = comment.find(f"{_P}pos")
        if parent is None and position is not None:
            # Only the comment that starts a thread carries the marker.
            thread_position = ET.SubElement(element, f"{_P188}pos")
            thread_position.set('x', position.get('x', '0'))
            thread_position.set('y', position.get('y', '0'))

        text_element = comment.find(f"{_P}text")
        _text_body(element, text_element.text or '' if text_element is not None else '')

    part_name = _threaded_part_name(package, slide_part_name)
    package.set_part(part_name, _serialise(root))
    _ensure_override(package, part_name, CONTENT_TYPES['threadedComments'])
    _ensure_relationship(
        package, slide_part_name, REL_TYPES['threadedComment'],
        _relative_target(slide_part_name, part_name),
    )


def write_threaded_comments(package) -> None:
    """Mirror every slide's classic comment list into a modern thread part."""
    from .comments_part import CommentsPart

    authors = _authors(package)
    if not authors:
        return
    wrote_any = False

    for slide_part_name in sorted(package.get_part_names()):
        if not slide_part_name.startswith('ppt/slides/slide'):
            continue
        if not slide_part_name.endswith('.xml'):
            continue
        rels = RelationshipsManager(package, slide_part_name)
        classic = rels.get_relationships_by_type(REL_TYPES['comments'])
        if not classic:
            continue
        comments_part_name = CommentsPart._resolve_target(slide_part_name, classic[0].target)
        if not package.has_part(comments_part_name):
            continue
        _write_thread(package, slide_part_name, comments_part_name, authors)
        wrote_any = True

    if wrote_any:
        _write_authors_part(package, authors)
