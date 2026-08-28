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

The thread part is a mirror of the classic list, rebuilt from it on every
save.  That is a deliberate limitation with a cost: a deck authored in
PowerPoint can hold resolved status, @-mentions and a reply-to-a-reply chain
in the modern part, none of which the classic list can express, and none of
which survives being regenerated from it.  There is no reliable way back —
a classic comment and a modern one are joined by nothing but their author and
index, and PowerPoint's identifiers are random rather than derived — so a
caller who touches ``comment_authors`` on such a deck loses whatever only the
modern part could say.  Loading and saving without touching comments does not
reach this code and is unaffected.
"""

from __future__ import annotations

import posixpath
import uuid
from typing import Optional

import lxml.etree as ET

from ..opc import ContentTypesManager, RelationshipsManager
from ..opc.content_types import CONTENT_TYPES
from ..opc.relationships import REL_TYPES, RELS_NS
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
THREADED_DIR = 'ppt/threadedComments/'

#: ``@created`` is required on ``p188:cm``, and a classic ``p:cm`` need not
#: carry ``@dt``.  A comment loaded without a time gets this rather than the
#: time of the save, which would rewrite the part on every save for no reason.
UNKNOWN_CREATED = '1970-01-01T00:00:00.000'

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


def _ensure_relationship(rels, rel_type: str, target: str) -> None:
    """Add the relationship to ``rels`` unless it already has one of that type."""
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


def _remove_part(package, part_name: str) -> None:
    """Delete a part and the ``Override`` that describes it."""
    package.delete_part(part_name)
    content_types = ContentTypesManager(package)
    if content_types.remove_override(part_name):
        content_types.save()


def _slide_rels(package, slide_part_name: str, live_rels: Optional[dict]):
    """The relationships manager whose contents will actually reach the file.

    A ``SlidePart`` reads its relationships once, at construction, and writes
    that set back over the package on every save.  A relationship added here
    through a *second* manager is therefore erased by the next save of the
    slide, which is how one comment came to allocate a new thread part on each
    save and orphan the one before it.  The caller passes the live managers so
    the relationship is added to the set that survives.
    """
    if live_rels is not None:
        rels = live_rels.get(slide_part_name)
        if rels is not None:
            return rels
    return RelationshipsManager(package, slide_part_name)


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
        RelationshipsManager(package, PRESENTATION_PART_NAME),
        REL_TYPES['authors'],
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


def _threaded_part_name(package, slide_part_name: str, rels) -> str:
    """The threaded part this slide already uses, or the next free name."""
    existing = rels.get_relationships_by_type(REL_TYPES['threadedComment'])
    if existing:
        from .comments_part import CommentsPart
        return CommentsPart._resolve_target(slide_part_name, existing[0].target)

    number = 1
    while package.has_part(f"{THREADED_DIR}threadedComment{number}.xml"):
        number += 1
    return f"{THREADED_DIR}threadedComment{number}.xml"


def _remove_thread(package, slide_part_name: str, rels) -> None:
    """Drop this slide's thread part, its ``Override`` and its relationship.

    Leaving the part in place when the classic list is empty keeps every
    comment the user deleted in the shipped file, in full text.
    """
    from .comments_part import CommentsPart

    existing = rels.get_relationships_by_type(REL_TYPES['threadedComment'])
    if not existing:
        return
    for relationship in existing:
        _remove_part(
            package,
            CommentsPart._resolve_target(slide_part_name, relationship.target),
        )
        rels.remove_relationship(relationship.id)
    rels.save()


def _prune_orphaned_threads(package) -> None:
    """Delete every thread part no relationship in the package names.

    Earlier versions allocated a new thread part on every save and left the
    previous one behind, complete with its own ``Override``, so nothing
    dangled and no consistency check objected — while a comment the user had
    deleted stayed in the file.  Opening such a package and saving it again
    clears them out.
    """
    named = set()
    for part_name in package.get_part_names():
        if not part_name.endswith('.rels'):
            continue
        data = package.get_part(part_name)
        if not data:
            continue
        try:
            root = ET.fromstring(data)
        except ET.XMLSyntaxError:
            continue
        owner_dir = posixpath.dirname(posixpath.dirname(part_name))
        for relationship in root.findall(f"{RELS_NS}Relationship"):
            if relationship.get('TargetMode') == 'External':
                continue
            target = relationship.get('Target') or ''
            if target.startswith('/'):
                named.add(target.lstrip('/'))
            else:
                named.add(posixpath.normpath(posixpath.join(owner_dir, target)))

    for part_name in list(package.get_part_names()):
        if part_name.startswith(THREADED_DIR) and part_name not in named:
            _remove_part(package, part_name)


def _write_thread(package, slide_part_name: str, comments: list, authors: dict, rels) -> None:
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
        element.set('created', comment.get('dt') or UNKNOWN_CREATED)

        position = comment.find(f"{_P}pos")
        if parent is None and position is not None:
            # Only the comment that starts a thread carries the marker.
            thread_position = ET.SubElement(element, f"{_P188}pos")
            thread_position.set('x', position.get('x', '0'))
            thread_position.set('y', position.get('y', '0'))

        text_element = comment.find(f"{_P}text")
        _text_body(element, text_element.text or '' if text_element is not None else '')

    part_name = _threaded_part_name(package, slide_part_name, rels)
    package.set_part(part_name, _serialise(root))
    _ensure_override(package, part_name, CONTENT_TYPES['threadedComments'])
    _ensure_relationship(
        rels, REL_TYPES['threadedComment'],
        _relative_target(slide_part_name, part_name),
    )


def _classic_comments(package, slide_part_name: str, rels) -> list:
    """This slide's classic ``p:cm`` elements, empty if it has none."""
    from .comments_part import CommentsPart

    classic = rels.get_relationships_by_type(REL_TYPES['comments'])
    if not classic:
        return []
    part_name = CommentsPart._resolve_target(slide_part_name, classic[0].target)
    data = package.get_part(part_name)
    if not data:
        return []
    return ET.fromstring(data).findall(f"{_P}cm")


def write_threaded_comments(package, slide_rels: Optional[dict] = None) -> None:
    """Mirror every slide's classic comment list into a modern thread part.

    ``slide_rels`` maps a slide part name to the relationships manager the
    caller will write for that slide.  It has to be the same object the slide
    part holds — see :func:`_slide_rels` for why a fresh one silently loses
    the relationship.
    """
    authors = _authors(package)
    wrote_any = False

    for slide_part_name in sorted(package.get_part_names()):
        if not slide_part_name.startswith('ppt/slides/slide'):
            continue
        if not slide_part_name.endswith('.xml'):
            continue
        rels = _slide_rels(package, slide_part_name, slide_rels)
        comments = _classic_comments(package, slide_part_name, rels)
        if comments and authors:
            _write_thread(package, slide_part_name, comments, authors, rels)
            wrote_any = True
        else:
            _remove_thread(package, slide_part_name, rels)

    _prune_orphaned_threads(package)

    if wrote_any:
        _write_authors_part(package, authors)
