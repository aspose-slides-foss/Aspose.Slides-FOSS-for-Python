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
