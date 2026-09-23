"""A comment must appear where the caller put it.

The schema types `p:cm/p:pos` as `a:CT_Point2D`, whose coordinates are EMU
everywhere else in DrawingML, but PowerPoint writes and reads a comment's
position in a unit of its own: an eighth of a point, 576 to the inch.  A
comment PowerPoint places 10 pt from the top-left corner of the slide is saved
as `<p:pos x="80" y="80"/>`, and the reply it cascades 12 pt below it as
`y="176"`.  Positions were written in EMU, 360 000 to the centimetre and so
1587.5 times PowerPoint's unit: a comment at 2 cm by 3 cm was written as
`x="720000" y="1080000"`, which PowerPoint places 90 000 pt from the left edge
of a slide 960 pt wide.

A comment's position is a `PointF` in centimetres from the top-left corner of
the slide, which is what the library has always meant by it; only the value in
the file changes.

`position` could also be assigned and was then lost: the setter changed the
comment in memory and never wrote it back, so the saved file kept the old
position without a word.

Most tests here write a deck and read the XML.  The ones that open a deck read
PowerPoint's own bytes — the comment part below is exactly what PowerPoint
saved — so the expected value comes from PowerPoint, not from this library's
writer, and a reader and a writer that share a mistake cannot agree on it.
"""

from __future__ import annotations

import datetime
import os
import zipfile

import pytest

from aspose.slides_foss import Presentation
from aspose.slides_foss.drawing import PointF
from aspose.slides_foss.export import SaveFormat

from .harness import NS, REL_TYPE, ProducedPackage

WHEN = datetime.datetime(2026, 1, 2, 3, 4, 5)

#: PowerPoint's comment-position units per centimetre: 576 per inch.
UNITS_PER_CM = 576 / 2.54

#: EMU per PowerPoint comment-position unit: 12 700 EMU per point, 8 units per point.
EMU_PER_UNIT = 12700 / 8

#: EMU per centimetre, the unit earlier versions wrote.
EMU_PER_CM = 360000

#: A comment and a reply to it, exactly as PowerPoint 16.0 saved them after
#: `Comments.Add2(Left=10, Top=10)` and `Replies.Add2`: the comment at 10 pt by
#: 10 pt, the reply cascaded 12 pt below it.  PowerPoint reports Left 10, Top 10
#: for the comment.
POWERPOINT_COMMENTS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<p:cmLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cm authorId="1" dt="2026-09-23T13:59:25.986" idx="1"><p:pos x="80" y="80"/>'
    '<p:text>Parent comment</p:text><p:extLst>'
    '<p:ext uri="{C676402C-5697-4E1C-873F-D02D1690AC5C}">'
    '<p15:threadingInfo xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/main" '
    'timeZoneBias="-240"/></p:ext></p:extLst></p:cm>'
    '<p:cm authorId="1" dt="2026-09-23T13:59:26.025" idx="2"><p:pos x="80" y="176"/>'
    '<p:text>Reply to parent</p:text><p:extLst>'
    '<p:ext uri="{C676402C-5697-4E1C-873F-D02D1690AC5C}">'
    '<p15:threadingInfo xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/main" '
    'timeZoneBias="-240"><p15:parentCm authorId="1" idx="1"/></p15:threadingInfo>'
    '</p:ext></p:extLst></p:cm></p:cmLst>'
)

#: The comment-author part PowerPoint saved with them.
POWERPOINT_AUTHORS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<p:cmAuthorLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cmAuthor id="1" name="Alice Ref" initials="AR" lastIdx="2" clrIdx="0"><p:extLst>'
    '<p:ext uri="{19B8F6BF-5375-455C-9EA6-DF929625EA0E}">'
    '<p15:presenceInfo xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/main" '
    'userId="Alice Ref" providerId="None"/></p:ext></p:extLst></p:cmAuthor></p:cmAuthorLst>'
)

#: Where PowerPoint put its two comments, in points: (Left, Top).
POWERPOINT_PLACED = {"Parent comment": (10, 10), "Reply to parent": (10, 22)}

CLASSIC_PART = "ppt/comments/comment1.xml"
SLIDE = "ppt/slides/slide1.xml"
THREADS = r"^ppt/threadedComments/.*\.xml$"


def _points_to_cm(points):
    return points / 72 * 2.54


def _comment_part(pkg):
    """The classic comment part slide 1's relationships name."""
    parts = [
        pkg._resolve_target(pkg.rels_part_for(SLIDE), rel["target"])
        for rel in pkg.relationships(SLIDE).values()
        if rel["type"] == REL_TYPE["comments"]
    ]
    assert len(parts) == 1, "slide 1 has %d comment parts: %r" % (len(parts), parts)
    return parts[0]


def _positions(pkg):
    """``{text: (x, y)}`` as written in every `p:cm/p:pos` of slide 1."""
    out = {}
    for comment in pkg.findall(_comment_part(pkg), "//p:cmLst/p:cm"):
        pos = comment.find("p:pos", NS)
        assert pos is not None, "a comment has no p:pos"
        out[comment.findtext("p:text", namespaces=NS)] = (int(pos.get("x")), int(pos.get("y")))
    return out


def _powerpoint_deck(directory):
    """A deck whose slide 1 carries PowerPoint's comment and reply, byte for byte."""
    source = os.path.join(directory, "blank.pptx")
    pres = Presentation()
    pres.save(source, SaveFormat.PPTX)
    pres.dispose()

    comments_rel = (
        '<Relationship Id="rId90" Type="%s" Target="../comments/comment1.xml"/>'
        % REL_TYPE["comments"]
    )
    authors_rel = (
        '<Relationship Id="rId91" Type="%s/commentAuthors" Target="commentAuthors.xml"/>'
        % NS["r"]
    )
    overrides = (
        '<Override PartName="/ppt/comments/comment1.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.presentationml.comments+xml"/>'
        '<Override PartName="/ppt/commentAuthors.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.presentationml.commentAuthors+xml"/>'
    )
    edits = {
        "ppt/slides/_rels/slide1.xml.rels": ("</Relationships>", comments_rel + "</Relationships>"),
        "ppt/_rels/presentation.xml.rels": ("</Relationships>", authors_rel + "</Relationships>"),
        "[Content_Types].xml": ("</Types>", overrides + "</Types>"),
    }

    deck = os.path.join(directory, "powerpoint-comments.pptx")
    with zipfile.ZipFile(source) as src, zipfile.ZipFile(deck, "w", zipfile.ZIP_DEFLATED) as dst:
        names = src.namelist()
        assert "ppt/commentAuthors.xml" not in names, "fixture: the blank deck has comment authors"
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename in edits:
                old, new = edits[item.filename]
                text = data.decode("utf-8")
                assert text.count(old) == 1, "fixture: no %s in %s" % (old, item.filename)
                data = text.replace(old, new).encode("utf-8")
            dst.writestr(item, data)
        dst.writestr(CLASSIC_PART, POWERPOINT_COMMENTS.encode("utf-8"))
        dst.writestr("ppt/commentAuthors.xml", POWERPOINT_AUTHORS.encode("utf-8"))
    return deck


def _add(pres, how, x_cm, y_cm):
    """Place one comment on slide 1 at ``(x_cm, y_cm)`` in the way ``how`` names."""
    author = pres.comment_authors.add_author("Reviewer", "RV")
    slide = pres.slides[0]
    if how == "add_comment":
        author.comments.add_comment("Here", slide, PointF(x_cm, y_cm), WHEN)
    elif how == "insert_comment":
        author.comments.insert_comment(0, "Here", slide, PointF(x_cm, y_cm), WHEN)
    elif how == "position setter":
        comment = author.comments.add_comment("Here", slide, PointF(1.0, 1.0), WHEN)
        comment.position = PointF(x_cm, y_cm)
    else:
        raise AssertionError(how)


@pytest.mark.parametrize("how", ["add_comment", "insert_comment", "position setter"])
def test_a_comment_is_written_in_the_unit_powerpoint_reads(produced, how):
    """One inch across and two down must be written as PowerPoint writes 72 pt and 144 pt."""
    pres = Presentation()
    _add(pres, how, 2.54, 5.08)
    pkg = produced(pres)

    assert _positions(pkg) == {"Here": (576, 1152)}, (
        "a comment placed 2.54 cm by 5.08 cm from the corner (72 pt by 144 pt) "
        "must be written <p:pos x=\"576\" y=\"1152\"/>, in eighths of a point, "
        "as PowerPoint writes it; the file says %r\n%s"
        % (_positions(pkg), pkg.text(_comment_part(pkg)))
    )
    pkg.assert_package_is_consistent()


@pytest.mark.parametrize(
    "x_cm, y_cm",
    [(0, 0), (1, 1), (2, 3), (2, 3.5), (12.7, 9.525), (25.4, 19.05), (33.8, 19.0)],
)
def test_a_comment_placed_on_the_slide_lies_on_the_slide(produced, x_cm, y_cm):
    """Every position on the slide must be written as a position on the slide."""
    pres = Presentation()
    _add(pres, "add_comment", x_cm, y_cm)
    pkg = produced(pres)

    size = pkg.find_one("ppt/presentation.xml", "/p:presentation/p:sldSz")
    width = int(size.get("cx")) / EMU_PER_UNIT
    height = int(size.get("cy")) / EMU_PER_UNIT
    x, y = _positions(pkg)["Here"]
    assert 0 <= x <= width and 0 <= y <= height, (
        "a comment at %s cm by %s cm is written at x=%d y=%d, outside a slide "
        "%d by %d eighths of a point" % (x_cm, y_cm, x, y, width, height)
    )
    assert (x, y) == (round(x_cm * UNITS_PER_CM), round(y_cm * UNITS_PER_CM))


def test_a_comment_powerpoint_placed_reads_back_where_powerpoint_shows_it(tmp_path):
    """PowerPoint's `x="80" y="80"` is 10 pt by 10 pt, which is 0.3528 cm by 0.3528 cm."""
    pres = Presentation(_powerpoint_deck(str(tmp_path)))
    try:
        read = {
            comment.text: (comment.position.x, comment.position.y)
            for comment in pres.slides[0].get_slide_comments(None)
        }
    finally:
        pres.dispose()

    expected = {
        text: (_points_to_cm(left), _points_to_cm(top))
        for text, (left, top) in POWERPOINT_PLACED.items()
    }
    assert set(read) == set(expected), read
    for text, (x, y) in expected.items():
        assert read[text] == (pytest.approx(x, abs=1e-6), pytest.approx(y, abs=1e-6)), (
            "%r: PowerPoint shows it at %r pt, which is (%.4f, %.4f) cm; the "
            "library reads (%r, %r) cm" % (text, POWERPOINT_PLACED[text], x, y, *read[text])
        )


def test_a_powerpoint_deck_saved_untouched_keeps_its_comment_positions(produced, tmp_path):
    """Opening and saving must not move a comment.

    Passes on the unfixed code too: a deck whose comments are never touched
    does not reach the comment writer.  It guards that it stays that way.
    """
    pres = Presentation(_powerpoint_deck(str(tmp_path)))
    pkg = produced(pres, name="resaved.pptx")

    assert _positions(pkg) == {"Parent comment": (80, 80), "Reply to parent": (80, 176)}


def test_a_powerpoint_comment_moved_onto_another_lands_exactly_on_it(produced, tmp_path):
    """Moving the reply to where the library reads the comment must write PowerPoint's 80, 80.

    This is the round trip a caller makes — read one comment's position,
    place another there — on PowerPoint's own values, so both the reading and
    the writing conversion are exercised, and a position that is not exact to
    the eighth of a point would show.  The comment authors are touched, so
    the whole comment list is written again: the comment that was not moved
    must keep its position and the reply its parent.
    """
    pres = Presentation(_powerpoint_deck(str(tmp_path)))
    comments = {c.text: c for c in pres.slides[0].get_slide_comments(None)}
    comments["Reply to parent"].position = comments["Parent comment"].position
    author = pres.comment_authors[0]
    author.comments.add_comment(
        "Placed on it", pres.slides[0], comments["Parent comment"].position, WHEN
    )
    pkg = produced(pres, name="moved.pptx")

    assert _positions(pkg) == {
        "Parent comment": (80, 80),
        "Reply to parent": (80, 80),
        "Placed on it": (80, 80),
    }, "\n" + pkg.text(_comment_part(pkg))
    parents = pkg.findall(
        _comment_part(pkg), "//p:cm[p:text='Reply to parent']//p15:parentCm"
    )
    assert [(p.get("authorId"), p.get("idx")) for p in parents] == [("1", "1")]


def _old_deck(directory):
    """A deck as an earlier version saved it: "Old" at 2 cm by 3 cm, written in EMU."""
    fresh = os.path.join(directory, "fresh.pptx")
    pres = Presentation()
    author = pres.comment_authors.add_author("Reviewer", "RV")
    author.comments.add_comment("Old", pres.slides[0], PointF(2.0, 3.0), WHEN)
    pres.save(fresh, SaveFormat.PPTX)
    pres.dispose()

    deck = os.path.join(directory, "old.pptx")
    rewritten = 0
    with zipfile.ZipFile(fresh) as src, zipfile.ZipFile(deck, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename.startswith("ppt/comments/"):
                text = data.decode("utf-8")
                assert text.count("<p:pos ") == 1, "fixture: %s" % text
                start = text.index("<p:pos ")
                end = text.index("/>", start) + 2
                data = (text[:start] + '<p:pos x="720000" y="1080000"/>' + text[end:]).encode("utf-8")
                rewritten += 1
            dst.writestr(item, data)
    assert rewritten == 1, "fixture: %d comment parts" % rewritten
    return deck


def test_an_old_comment_moved_back_stays_put_when_comments_are_added_around_it(produced, tmp_path):
    """The changelog's remedy for a file an earlier version wrote, between two additions.

    An earlier version wrote 2 cm by 3 cm as `x="720000" y="1080000"`.  The
    remedy divides the position that reads back by 1587.5.  A comment added
    before the move and one added after it must neither undo it nor be lost.
    """
    pres = Presentation(_old_deck(str(tmp_path)))
    author = pres.comment_authors[0]
    slide = pres.slides[0]
    author.comments.add_comment("Before", slide, PointF(1.0, 1.0), WHEN)
    for comment in author.comments:
        if comment.text == "Old":
            p = comment.position
            comment.position = PointF(p.x / 1587.5, p.y / 1587.5)
    author.comments.add_comment("After", slide, PointF(1.0, 2.0), WHEN)
    pkg = produced(pres, name="moved-back.pptx")

    assert _positions(pkg) == {
        "Old": (454, 680),
        "Before": (227, 227),
        "After": (227, 454),
    }, "\n" + pkg.text(_comment_part(pkg))


def test_the_thread_part_keeps_its_position_in_emu(produced):
    """The position mirrored into `ppt/threadedComments/` is unchanged by the fix.

    That part is rebuilt from the classic list whenever a save writes the
    comment authors, as this one does, and has always carried the position in
    EMU for a comment this library wrote.  Which unit PowerPoint reads there has not
    been measured, so it is left as it was: 2.54 cm is written as 914 400 EMU
    before and after.  Passes on the unfixed code too.
    """
    pres = Presentation()
    _add(pres, "add_comment", 2.54, 5.08)
    pkg = produced(pres)

    thread = pkg.parts_matching(THREADS)
    assert len(thread) == 1, thread
    pos = pkg.find_one(thread[0], "//p188:cm/p188:pos")
    assert (int(pos.get("x")), int(pos.get("y"))) == (
        round(2.54 * EMU_PER_CM),
        round(5.08 * EMU_PER_CM),
    ), pkg.text(thread[0])
