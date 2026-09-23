"""An edit made through a comment must reach the file, and must not undo another.

Every way of reaching a comment — `author.comments`, `slide.get_slide_comments`,
the comment `add_comment` returns — worked on its own copy of the slide's
comment part, and an edit wrote its copy back whole.  Three failures followed,
none of them visible to a test that reads the comment back from memory:

* `text`, `created_time` and `position` changed the copy and never wrote it,
  so the saved file kept the old value and nothing said so;
* a handle read before another comment was added to the slide wrote back a
  list without that comment: give it a parent or remove it, and the comment
  added since was gone from the file;
* adding a comment worked on a copy kept from an earlier addition to the same
  slide, so an edit made in between through another handle was undone.

An edit now starts from the part as the package holds it, finds the comment
by its author and index, and writes the part back at once; an addition reads
the part again every time.  Each test edits the comment "first" through one
handle and adds or keeps "other" through another, then reads the XML.
"""

from __future__ import annotations

import datetime

import pytest

from aspose.slides_foss import Presentation
from aspose.slides_foss.drawing import PointF

from .harness import NS, REL_TYPE

WHEN = datetime.datetime(2026, 1, 2, 3, 4, 5)
LATER = datetime.datetime(2027, 6, 7, 8, 9, 10)
SLIDE = "ppt/slides/slide1.xml"


def _position(cm):
    pos = cm.find("p:pos", NS)
    return int(pos.get("x")), int(pos.get("y"))


def _parent(cm):
    parent = cm.find(".//p15:parentCm", NS)
    return None if parent is None else (parent.get("authorId"), parent.get("idx"))


def _set(name, value):
    def edit(comment, other):
        setattr(comment, name, value)
    return edit


def _reply_to_other(comment, other):
    comment.parent_comment = other


def _remove(comment, other):
    comment.remove()


#: name -> (the edit made to "first" given "other"; the text "first" has in the
#: file afterwards, or None if it must be gone; what its `p:cm` must carry).
EDITS = {
    "position": (
        _set("position", PointF(2.54, 5.08)),
        "first",
        lambda cm, other: _position(cm) == (576, 1152),
    ),
    "text": (_set("text", "edited"), "edited", lambda cm, other: True),
    "created_time": (
        _set("created_time", LATER),
        "first",
        lambda cm, other: cm.get("dt") == "2027-06-07T08:09:10.000",
    ),
    "parent_comment": (
        _reply_to_other,
        "first",
        lambda cm, other: _parent(cm) == (other.get("authorId"), other.get("idx")),
    ),
    "remove": (_remove, None, None),
}


def _assert_edited(pkg, edit, kept):
    """Slide 1's comments are ``kept`` plus the edited one, and the edit is in the file."""
    _, text_after, holds = EDITS[edit]
    parts = [
        pkg._resolve_target(pkg.rels_part_for(SLIDE), rel["target"])
        for rel in pkg.relationships(SLIDE).values()
        if rel["type"] == REL_TYPE["comments"]
    ]
    assert len(parts) == 1, "slide 1 has %d comment parts: %r" % (len(parts), parts)
    xml = pkg.text(parts[0])
    comments = pkg.findall(parts[0], "//p:cmLst/p:cm")
    texts = [cm.findtext("p:text", namespaces=NS) for cm in comments]
    expected = sorted(kept + ([text_after] if text_after else []))
    assert sorted(texts) == expected, (
        "after the %s edit slide 1 must carry the comments %r; the file has %r\n%s"
        % (edit, expected, texts, xml)
    )
    if text_after:
        by_text = dict(zip(texts, comments))
        assert holds(by_text[text_after], by_text["other"]), (
            "the %s edit is not in the file\n%s" % (edit, xml)
        )
    assert _position(dict(zip(texts, comments))["other"]) == (454, 454), (
        "the comment that was not edited moved\n%s" % xml
    )


def _deck():
    pres = Presentation()
    author = pres.comment_authors.add_author("Reviewer", "RV")
    return pres, author, pres.slides[0]


@pytest.mark.parametrize("edit", list(EDITS))
def test_an_edit_reaches_the_file(produced, edit):
    """The simplest case: one handle, edited, then the deck saved."""
    pres, author, slide = _deck()
    first = author.comments.add_comment("first", slide, PointF(1, 1), WHEN)
    other = author.comments.add_comment("other", slide, PointF(2, 2), WHEN)
    EDITS[edit][0](first, other)
    _assert_edited(produced(pres), edit, ["other"])


@pytest.mark.parametrize("edit", list(EDITS))
def test_an_edit_through_a_handle_read_earlier_keeps_a_comment_added_since(produced, edit):
    """A handle read before "other" existed must not write a list without it."""
    pres, author, slide = _deck()
    author.comments.add_comment("first", slide, PointF(1, 1), WHEN)
    earlier = slide.get_slide_comments(None)[0]
    other = author.comments.add_comment("other", slide, PointF(2, 2), WHEN)
    EDITS[edit][0](earlier, other)
    _assert_edited(produced(pres), edit, ["other"])


@pytest.mark.parametrize("edit", list(EDITS))
def test_an_edit_survives_a_comment_added_after_it(produced, edit):
    """Add, edit through `author.comments`, add again: the second addition keeps the edit."""
    pres, author, slide = _deck()
    author.comments.add_comment("first", slide, PointF(1, 1), WHEN)
    author.comments.add_comment("other", slide, PointF(2, 2), WHEN)
    EDITS[edit][0](author.comments[0], author.comments[1])
    author.comments.add_comment("later", slide, PointF(3, 3), WHEN)
    _assert_edited(produced(pres), edit, ["other", "later"])
