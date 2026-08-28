"""Saving twice, and deleting a comment, must not leave old text in the file.

Two failures with one cause, both invisible to a test that only looks at the
part the slide currently points at:

* every save allocated a *new* ``ppt/threadedComments/threadedCommentN.xml``
  and repointed the slide at it, because the slide's relationships were read
  back from the package by a second manager while the slide part itself held —
  and rewrote — an older set.  Four saves produced four parts;
* removing every comment on a slide emptied ``ppt/comments/slideN.xml`` and
  left the thread part exactly as it was.

Together they are a disclosure: a comment the user deleted is still in the
shipped package, in full, in a part nothing points at any more.  Every orphan
keeps its own ``Override``, so no reference dangles and no consistency check
notices.

The package rule that catches the first one is that a part which no
relationship names is not part of the document (ISO/IEC 29500-2 §9.3): a
consumer reaches parts by walking relationships from ``_rels/.rels``, so an
unreachable part is dead weight that still ships.
"""

from __future__ import annotations

import datetime

from aspose.slides_foss import Presentation
from aspose.slides_foss.drawing import PointF

from .harness import ProducedPackage

WHEN = datetime.datetime(2026, 1, 15, 12, 0, 0)
THREADS = r"^ppt/threadedComments/.*\.xml$"


def _save(pres, tmp_path, name) -> ProducedPackage:
    from aspose.slides_foss.export import SaveFormat

    path = str(tmp_path / name)
    pres.save(path, SaveFormat.PPTX)
    return ProducedPackage(path)


def test_saving_the_same_deck_repeatedly_writes_one_thread_part(tmp_path):
    """A save must reuse the slide's thread part, not allocate the next number."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), WHEN)

    try:
        counts = []
        for attempt in range(1, 5):
            pkg = _save(pres, tmp_path, "save%d.pptx" % attempt)
            counts.append(len(pkg.parts_matching(THREADS)))
            pkg.close()
    finally:
        pres.dispose()

    assert counts == [1, 1, 1, 1], (
        "one comment, saved four times, produced %r thread parts; each save "
        "orphaned the previous part instead of rewriting it" % counts
    )


def test_a_deleted_comment_is_not_left_behind_in_an_orphaned_part(tmp_path):
    """Removing a comment must remove its text from the package, not hide it."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    author.comments.add_comment("keep this one", slide, PointF(1.0, 1.0), WHEN)
    doomed = author.comments.add_comment("delete this one", slide, PointF(2.0, 2.0), WHEN)

    try:
        _save(pres, tmp_path, "before.pptx").close()
        doomed.remove()
        pkg = _save(pres, tmp_path, "after.pptx")
    finally:
        pres.dispose()

    try:
        carrying = [
            part for part in pkg.namelist
            if part.endswith(".xml") and b"delete this one" in pkg.read(part)
        ]
        assert not carrying, (
            "the deleted comment's text is still in the saved package, in %r; "
            "the classic list dropped it and the thread part kept it"
            % carrying
        )
    finally:
        pkg.close()


def test_removing_every_comment_removes_the_thread_part(tmp_path):
    """An empty comment list must leave no thread part behind."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    root = author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), WHEN)
    reply = author.comments.add_comment("Reviewed", slide, PointF(2.0, 3.0), WHEN)
    reply.parent_comment = root

    try:
        _save(pres, tmp_path, "with.pptx").close()
        reply.remove()
        root.remove()
        pkg = _save(pres, tmp_path, "without.pptx")
    finally:
        pres.dispose()

    try:
        assert not pkg.parts_matching(THREADS), (
            "every comment was removed and the thread part is still in the "
            "package: %r" % pkg.parts_matching(THREADS)
        )
        pkg.assert_package_is_consistent()
    finally:
        pkg.close()


def test_a_repeatedly_saved_deck_has_no_unreachable_parts(tmp_path):
    """Nothing may ship that no relationship names."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    author.comments.add_comment("Please review", slide, PointF(2.0, 3.0), WHEN)

    try:
        _save(pres, tmp_path, "first.pptx").close()
        pkg = _save(pres, tmp_path, "second.pptx")
    finally:
        pres.dispose()

    try:
        pkg.assert_every_part_is_reachable()
    finally:
        pkg.close()
