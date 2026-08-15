"""Recomputing the ``docProps/app.xml`` summary from the package.

The extended properties part carries a summary of the document: how many
slides it has, how many are hidden, how many notes pages, how much text, and
the title of each slide.  Nothing in the format keeps it in step with the
content, so a part copied from a template and never regenerated describes the
template forever — a three-slide deck that reports one slide, and a slide list
naming a title the deck does not contain.

This module reads the counts back out of the package itself, after the slide
parts have been written, so the summary describes the file that is about to be
saved rather than the file it was copied from.
"""

from __future__ import annotations

import re
from typing import Optional

from lxml import etree

from .app_properties_part import AppPropertiesPart, HeadingPairData
from .constants import NAMESPACES

_P = f"{{{NAMESPACES['p']}}}"
_A = f"{{{NAMESPACES['a']}}}"
_R = f"{{{NAMESPACES['r']}}}"
_PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"

_SLIDE_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
_NOTES_SLIDE_PART = re.compile(r"^ppt/notesSlides/notesSlide\d+\.xml$")

#: What PowerPoint records for a slide whose title placeholder is empty.
_UNTITLED = "PowerPoint Presentation"

#: The heading pair whose entries in TitlesOfParts are the slide titles.
_SLIDE_TITLES = "Slide Titles"


def _parse(package, part_name: str) -> Optional[etree._Element]:
    data = package.get_part(part_name)
    if not data:
        return None
    try:
        return etree.fromstring(data)
    except etree.XMLSyntaxError:
        return None


def _slide_part_names(package) -> list[str]:
    """The slide parts, in presentation order, as ``p:sldIdLst`` gives them."""
    presentation = _parse(package, 'ppt/presentation.xml')
    relationships = _parse(package, 'ppt/_rels/presentation.xml.rels')
    if presentation is None or relationships is None:
        return []

    targets = {
        element.get('Id'): element.get('Target', '')
        for element in relationships.findall(f"{_PR}Relationship")
        if element.get('Type') == _SLIDE_REL_TYPE
    }

    names = []
    for slide_id in presentation.iter(f"{_P}sldId"):
        target = targets.get(slide_id.get(f"{_R}id"))
        if not target:
            continue
        if target.startswith('/'):
            names.append(target.lstrip('/'))
        else:
            names.append('ppt/' + target.lstrip('./'))
    return names


def _title_of(slide: etree._Element) -> str:
    """The text of the slide's title placeholder, or PowerPoint's stand-in."""
    for placeholder in slide.iter(f"{_P}ph"):
        if placeholder.get('type') not in ('title', 'ctrTitle'):
            continue
        shape = placeholder
        while shape is not None and shape.tag != f"{_P}sp":
            shape = shape.getparent()
        if shape is None:
            continue
        text = ''.join(node.text or '' for node in shape.iter(f"{_A}t")).strip()
        if text:
            return text
    return _UNTITLED


def _text_counts(root: etree._Element) -> tuple[int, int]:
    """``(paragraphs, words)`` for one part: paragraphs that carry text."""
    paragraphs = 0
    words = 0
    for paragraph in root.iter(f"{_A}p"):
        text = ''.join(node.text or '' for node in paragraph.iter(f"{_A}t"))
        if text.strip():
            paragraphs += 1
            words += len(text.split())
    return paragraphs, words


def _replace_slide_titles(app: AppPropertiesPart, titles: list[str]) -> None:
    """Put ``titles`` in the Slide Titles section of the parts vector.

    ``TitlesOfParts`` is one flat vector whose entries are divided between the
    heading pairs in order, so the slide titles cannot be replaced without
    knowing how many entries the pairs before them claim.
    """
    pairs = app.heading_pairs
    names = [pair.name for pair in pairs]
    if _SLIDE_TITLES not in names:
        app.heading_pairs = pairs + [HeadingPairData(_SLIDE_TITLES, len(titles))]
        app.titles_of_parts = list(app.titles_of_parts) + titles
        return

    index = names.index(_SLIDE_TITLES)
    before = sum(pair.count for pair in pairs[:index])
    after = sum(pair.count for pair in pairs[index + 1:])

    entries = list(app.titles_of_parts)
    tail = entries[len(entries) - after:] if after else []
    app.titles_of_parts = entries[:before] + titles + tail
    pairs[index].count = len(titles)


def refresh_document_summary(package) -> None:
    """Rewrite ``docProps/app.xml``'s counts and titles from the package."""
    if not package.has_part('docProps/app.xml'):
        return

    slide_parts = _slide_part_names(package)
    notes_parts = [n for n in package.get_part_names() if _NOTES_SLIDE_PART.match(n)]

    hidden = 0
    paragraphs = 0
    words = 0
    titles = []
    for part_name in slide_parts:
        slide = _parse(package, part_name)
        if slide is None:
            continue
        if slide.get('show') == '0':
            hidden += 1
        part_paragraphs, part_words = _text_counts(slide)
        paragraphs += part_paragraphs
        words += part_words
        titles.append(_title_of(slide))

    for part_name in notes_parts:
        notes = _parse(package, part_name)
        if notes is None:
            continue
        part_paragraphs, part_words = _text_counts(notes)
        paragraphs += part_paragraphs
        words += part_words

    app = AppPropertiesPart(package)
    app.slides = len(slide_parts)
    app.hidden_slides = hidden
    app.notes = len(notes_parts)
    app.paragraphs = paragraphs
    app.words = words
    _replace_slide_titles(app, titles)
    app.mark_dirty()
    app.save()
