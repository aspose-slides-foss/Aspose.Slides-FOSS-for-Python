"""A misspelt property must fail where it is written, on every object.

Python accepts an assignment to any name, so `slide.slide_show_transtion = ...`
or `portion.txt = "Hello"` used to succeed, store a value nothing reads, and
leave the setting out of the saved file.  From outside that is exactly what a
working call looks like until somebody opens the result.

The format classes and shapes already refused such an assignment.  The
objects a caller reaches first — the presentation, its slides, text frames,
paragraphs, portions, table cells, the slide transition and hyperlinks — did
not.  They must refuse it too.
"""

from __future__ import annotations

import pytest

from aspose.slides_foss import Hyperlink, Presentation, ShapeType


def _objects(pres):
    slide = pres.slides[0]
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50.0, 50.0, 200.0, 100.0)
    shape.add_text_frame("Text")
    paragraph = shape.text_frame.paragraphs[0]
    table = slide.shapes.add_table(50.0, 200.0, [100.0, 100.0], [40.0, 40.0])
    return {
        "Presentation": pres,
        "Slide": slide,
        "LayoutSlide": pres.layout_slides[0],
        "MasterSlide": pres.masters[0],
        "NotesSlide": slide.notes_slide_manager.add_notes_slide(),
        "TextFrame": shape.text_frame,
        "Paragraph": paragraph,
        "Portion": paragraph.portions[0],
        "Cell": table.rows[0][0],
        "SlideShowTransition": slide.slide_show_transition,
        "Hyperlink": Hyperlink("https://example.com/"),
    }


NAMES = [
    "Presentation", "Slide", "LayoutSlide", "MasterSlide", "NotesSlide", "TextFrame",
    "Paragraph", "Portion", "Cell", "SlideShowTransition", "Hyperlink",
]


@pytest.mark.parametrize("name", NAMES)
def test_an_unknown_property_is_rejected(name):
    """Assigning to a name the object has no property for raises `AttributeError`."""
    pres = Presentation()
    try:
        target = _objects(pres)[name]
        with pytest.raises(AttributeError, match="has no property 'definitely_not_a_property'"):
            target.definitely_not_a_property = 1
    finally:
        pres.dispose()


def test_a_real_property_is_still_assigned():
    """The guard refuses unknown names only; a real setter still takes effect."""
    pres = Presentation()
    try:
        objects = _objects(pres)
        objects["Portion"].text = "Changed"
        assert objects["Portion"].text == "Changed"
    finally:
        pres.dispose()
