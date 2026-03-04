"""
Comments — CommentAuthorCollection, CommentCollection, Comment properties, Slide.get_slide_comments().
"""
import os
import sys
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation
from aspose.slides_foss.drawing import PointF
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def add_comment_author():
    """Add comment authors to a presentation."""
    with Presentation() as pres:
        authors = pres.comment_authors

        author1 = authors.add_author("Alice", "A")
        author2 = authors.add_author("Bob", "B")

        print(f"Authors count: {len(authors)}")
        print(f"  Author 0: name='{author1.name}', initials='{author1.initials}'")
        print(f"  Author 1: name='{author2.name}', initials='{author2.initials}'")

        pres.save(os.path.join(OUT, "comment_authors.pptx"), SaveFormat.PPTX)


def add_comments():
    """Add comments to a slide."""
    with Presentation() as pres:
        author = pres.comment_authors.add_author("Alice", "A")

        # Add a comment on the first slide
        slide = pres.slides[0]
        pos = PointF(2.0, 3.0)  # position in cm
        now = datetime.datetime.now()

        comment = author.comments.add_comment("This is a review comment.", slide, pos, now)
        print(f"Comment text: '{comment.text}'")
        print(f"Comment position: ({comment.position.x}, {comment.position.y})")
        print(f"Comment created_time: {comment.created_time}")
        print(f"Comment author: {comment.author.name}")

        pres.save(os.path.join(OUT, "add_comments.pptx"), SaveFormat.PPTX)


def insert_comment():
    """Insert a comment at a specific index."""
    with Presentation() as pres:
        author = pres.comment_authors.add_author("Alice", "A")
        slide = pres.slides[0]
        now = datetime.datetime.now()

        author.comments.add_comment("First comment", slide, PointF(1.0, 1.0), now)
        author.comments.add_comment("Third comment", slide, PointF(1.0, 3.0), now)

        # Insert at index 1
        author.comments.insert_comment(1, "Second comment (inserted)", slide, PointF(1.0, 2.0), now)

        print(f"Total comments: {len(author.comments)}")
        for i, c in enumerate(author.comments):
            print(f"  [{i}] '{c.text}'")

        pres.save(os.path.join(OUT, "insert_comment.pptx"), SaveFormat.PPTX)


def get_slide_comments():
    """Retrieve comments for a specific slide."""
    with Presentation() as pres:
        author1 = pres.comment_authors.add_author("Alice", "A")
        author2 = pres.comment_authors.add_author("Bob", "B")
        slide = pres.slides[0]
        now = datetime.datetime.now()

        author1.comments.add_comment("Alice's comment", slide, PointF(1.0, 1.0), now)
        author2.comments.add_comment("Bob's comment", slide, PointF(2.0, 2.0), now)

        # Get all comments on the slide
        all_comments = slide.get_slide_comments(None)
        print(f"All slide comments: {len(all_comments)}")
        for c in all_comments:
            print(f"  '{c.text}' by {c.author.name}")

        # Get only Bob's comments
        bob_comments = slide.get_slide_comments(author2)
        print(f"Bob's comments: {len(bob_comments)}")

        pres.save(os.path.join(OUT, "slide_comments.pptx"), SaveFormat.PPTX)


def remove_comments():
    """Remove comments and clear the collection."""
    with Presentation() as pres:
        author = pres.comment_authors.add_author("Alice", "A")
        slide = pres.slides[0]
        now = datetime.datetime.now()

        author.comments.add_comment("Comment 1", slide, PointF(1.0, 1.0), now)
        author.comments.add_comment("Comment 2", slide, PointF(2.0, 2.0), now)
        author.comments.add_comment("Comment 3", slide, PointF(3.0, 3.0), now)
        print(f"Before removal: {len(author.comments)} comments")

        # Remove by index
        author.comments.remove_at(1)
        print(f"After remove_at(1): {len(author.comments)} comments")

        # Clear all
        author.comments.clear()
        print(f"After clear: {len(author.comments)} comments")

        pres.save(os.path.join(OUT, "remove_comments.pptx"), SaveFormat.PPTX)


def remove_author():
    """Remove a comment author."""
    with Presentation() as pres:
        authors = pres.comment_authors
        author1 = authors.add_author("Alice", "A")
        author2 = authors.add_author("Bob", "B")
        print(f"Before: {len(authors)} authors")

        authors.remove(author1)
        print(f"After removing Alice: {len(authors)} authors")

        pres.save(os.path.join(OUT, "remove_author.pptx"), SaveFormat.PPTX)


def parent_comment():
    """Access the parent_comment property (reply threading)."""
    with Presentation() as pres:
        author = pres.comment_authors.add_author("Alice", "A")
        slide = pres.slides[0]
        now = datetime.datetime.now()

        parent = author.comments.add_comment("Parent comment", slide, PointF(1.0, 1.0), now)
        print(f"Parent comment: '{parent.text}'")
        print(f"parent_comment of parent: {parent.parent_comment}")

        pres.save(os.path.join(OUT, "parent_comment.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    add_comment_author()
    add_comments()
    insert_comment()
    get_slide_comments()
    remove_comments()
    remove_author()
    parent_comment()
    print("\n=== test_comments.py completed ===")
