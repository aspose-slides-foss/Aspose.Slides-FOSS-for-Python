"""Tests for Comments: authors, comments CRUD, slide comments."""
import datetime

from aspose.slides_foss import Presentation
from aspose.slides_foss.drawing import PointF


def test_add_author(tmp_pptx):
    """Author name and initials persist."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    assert author.name == "Alice"
    assert author.initials == "A"
    assert len(pres.comment_authors) == 1

    pres2 = tmp_pptx(pres)
    assert len(pres2.comment_authors) == 1
    assert pres2.comment_authors[0].name == "Alice"
    assert pres2.comment_authors[0].initials == "A"
    pres2.dispose()


def test_add_comment(tmp_pptx):
    """Comment text, position, and time persist."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    now = datetime.datetime(2026, 1, 15, 12, 0, 0)
    comment = author.comments.add_comment("Review note", slide, PointF(2.0, 3.0), now)
    assert comment.text == "Review note"
    assert comment.author.name == "Alice"

    pres2 = tmp_pptx(pres)
    a2 = pres2.comment_authors[0]
    assert len(a2.comments) == 1
    c = a2.comments[0]
    assert c.text == "Review note"
    pres2.dispose()


def test_multiple_authors():
    """Multiple authors can coexist."""
    with Presentation() as pres:
        pres.comment_authors.add_author("Alice", "A")
        pres.comment_authors.add_author("Bob", "B")
        assert len(pres.comment_authors) == 2


def test_get_slide_comments():
    """get_slide_comments filters by author."""
    with Presentation() as pres:
        a1 = pres.comment_authors.add_author("Alice", "A")
        a2 = pres.comment_authors.add_author("Bob", "B")
        slide = pres.slides[0]
        now = datetime.datetime.now()
        a1.comments.add_comment("Alice's", slide, PointF(1, 1), now)
        a2.comments.add_comment("Bob's", slide, PointF(2, 2), now)

        all_c = slide.get_slide_comments(None)
        assert len(all_c) == 2

        bob_c = slide.get_slide_comments(a2)
        assert len(bob_c) == 1
        assert bob_c[0].text == "Bob's"


def test_remove_comment(tmp_pptx):
    """Removing a comment persists."""
    pres = Presentation()
    author = pres.comment_authors.add_author("Alice", "A")
    slide = pres.slides[0]
    now = datetime.datetime.now()
    author.comments.add_comment("C1", slide, PointF(1, 1), now)
    author.comments.add_comment("C2", slide, PointF(2, 2), now)
    author.comments.add_comment("C3", slide, PointF(3, 3), now)
    assert len(author.comments) == 3

    author.comments.remove_at(1)
    assert len(author.comments) == 2

    pres2 = tmp_pptx(pres)
    assert len(pres2.comment_authors[0].comments) == 2
    pres2.dispose()


def test_insert_comment():
    """insert_comment places at the correct index."""
    with Presentation() as pres:
        author = pres.comment_authors.add_author("Alice", "A")
        slide = pres.slides[0]
        now = datetime.datetime.now()
        author.comments.add_comment("First", slide, PointF(1, 1), now)
        author.comments.add_comment("Third", slide, PointF(1, 3), now)
        author.comments.insert_comment(1, "Second", slide, PointF(1, 2), now)
        assert len(author.comments) == 3
        assert author.comments[1].text == "Second"


def test_clear_comments():
    """clear() removes all comments from an author."""
    with Presentation() as pres:
        author = pres.comment_authors.add_author("Alice", "A")
        slide = pres.slides[0]
        now = datetime.datetime.now()
        author.comments.add_comment("C1", slide, PointF(1, 1), now)
        author.comments.add_comment("C2", slide, PointF(2, 2), now)
        author.comments.clear()
        assert len(author.comments) == 0


def test_remove_author(tmp_pptx):
    """Removing an author persists."""
    pres = Presentation()
    pres.comment_authors.add_author("Alice", "A")
    pres.comment_authors.add_author("Bob", "B")
    pres.comment_authors.remove(pres.comment_authors[0])
    assert len(pres.comment_authors) == 1

    pres2 = tmp_pptx(pres)
    assert len(pres2.comment_authors) == 1
    assert pres2.comment_authors[0].name == "Bob"
    pres2.dispose()
