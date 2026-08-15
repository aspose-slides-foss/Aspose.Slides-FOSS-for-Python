"""A reply must still be a reply after the file has been saved.

`comment.parent_comment = other` is accepted, reads back correctly from the
in-memory object, and is gone the moment the file is written: the saved package
carries no link between the two comments at all, and reopening it gives `None`
on both.  PowerPoint shows two independent flat comments.

This is the cleanest example in the suite of a defect that a read-back
assertion cannot see.  The library agrees with itself, because both sides of
the round trip go through the same in-memory object; only the bytes disagree.

Modern PowerPoint threading is a separate part — `ppt/threadedComments/`,
content type `application/vnd.ms-powerpoint.threadedcomments+xml`, namespace
`http://schemas.microsoft.com/office/powerpoint/2018/8/main`, with `p188:cm`
elements carrying `@id` and `@parentId`.  The legacy `p:cm` element has no
attribute for a parent, so the reply cannot be expressed there: `parentCmId` is
not in the schema and no consumer renders it.
"""

from __future__ import annotations

import datetime

from aspose.slides_foss import Presentation
from aspose.slides_foss.drawing import PointF

THREADED_CONTENT_TYPE = "application/vnd.ms-powerpoint.threadedcomments+xml"

CLASSIC = "ppt/comments/slide1.xml"

#: The `p:ext` uri PowerPoint looks for on a classic comment to find its thread.
THREADING_INFO_URI = "{C676402C-5697-4E1C-873F-D02D1690AC5C}"


def test_a_comment_reply_survives_being_saved(produced):
    """The parent/child link must be in the package, not only in memory."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    when = datetime.datetime(2026, 1, 15, 12, 0, 0)
    root = author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), when)
    reply = author.comments.add_comment("Reviewed", slide, PointF(2.0, 3.0), when)
    reply.parent_comment = root

    pkg = produced(pres)

    threaded_parts = pkg.parts_matching(r"^ppt/threadedComments/.*\.xml$")
    assert threaded_parts, (
        "a reply was written but the package has no ppt/threadedComments/ part, "
        "so the reply is a second independent comment. parts: %r"
        % sorted(pkg.namelist)
    )

    part = threaded_parts[0]
    assert pkg.content_type_of(part) == THREADED_CONTENT_TYPE

    comments = pkg.findall(part, "//p188:cm")
    assert len(comments) == 2, (
        "expected the root comment and its reply, found %d" % len(comments)
    )

    parented = [c for c in comments if c.get("parentId")]
    assert len(parented) == 1, (
        "exactly one of the two comments must carry @parentId; %d do"
        % len(parented)
    )
    root_ids = {c.get("id") for c in comments if not c.get("parentId")}
    assert parented[0].get("parentId") in root_ids, (
        "@parentId does not name the other comment"
    )


def test_the_classic_comment_carries_the_extension_powerpoint_reads(produced):
    """`p15:threadingInfo` on the classic `p:cm` is what renders the reply.

    The modern part alone is not enough.  PowerPoint takes the parent from the
    `p15:threadingInfo/p15:parentCm` extension on the *classic* list; a file
    that has a correct `ppt/threadedComments/` part and no extension opens
    without complaint and shows two independent flat comments, which is the
    worst shape this defect can take — the thread is lost and nothing says so.
    """
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    when = datetime.datetime(2026, 1, 15, 12, 0, 0)
    root = author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), when)
    reply = author.comments.add_comment("Reviewed", slide, PointF(2.0, 3.0), when)
    reply.parent_comment = root

    pkg = produced(pres)

    comments = pkg.findall(CLASSIC, "//p:cmLst/p:cm")
    assert len(comments) == 2, "expected two classic comments, found %d" % len(comments)

    parents = pkg.findall(
        CLASSIC,
        "//p:cm/p:extLst/p:ext[@uri='%s']/p15:threadingInfo/p15:parentCm"
        % THREADING_INFO_URI,
    )
    assert len(parents) == 1, (
        "exactly one classic comment must carry p15:threadingInfo/p15:parentCm; "
        "%d do, so PowerPoint has nothing to build the thread from.\n%s"
        % (len(parents), pkg.text(CLASSIC))
    )

    parent = parents[0]
    roots = [c for c in comments if not c.findall(".//{*}parentCm")]
    assert len(roots) == 1, "exactly one comment must be a thread root"
    assert parent.get("authorId") == roots[0].get("authorId"), (
        "p15:parentCm/@authorId is %r but the root comment's is %r"
        % (parent.get("authorId"), roots[0].get("authorId"))
    )
    assert parent.get("idx") == roots[0].get("idx"), (
        "p15:parentCm/@idx is %r but the root comment's is %r"
        % (parent.get("idx"), roots[0].get("idx"))
    )

    # `parentCmId` is not in CT_Comment and no consumer renders it.
    for comment in comments:
        assert "parentCmId" not in comment.attrib, (
            "the invalid parentCmId attribute is back on <p:cm>: %r"
            % dict(comment.attrib)
        )


def test_every_threaded_comment_declares_when_it_was_created(produced):
    """`@created` is required on `p188:cm`, whatever the classic list says."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    when = datetime.datetime(2026, 1, 15, 12, 0, 0)
    author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), when)

    pkg = produced(pres)

    part = pkg.parts_matching(r"^ppt/threadedComments/.*\.xml$")[0]
    for comment in pkg.findall(part, "//p188:cm"):
        assert comment.get("created"), (
            "<p188:cm> without @created: %r" % dict(comment.attrib)
        )


def test_a_commented_deck_leaves_the_package_consistent(produced):
    """Comment parts must be content-typed and their relationships resolvable."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    when = datetime.datetime(2026, 1, 15, 12, 0, 0)
    root = author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), when)
    reply = author.comments.add_comment("Reviewed", slide, PointF(2.0, 3.0), when)
    reply.parent_comment = root

    pkg = produced(pres)

    pkg.assert_package_is_consistent()
