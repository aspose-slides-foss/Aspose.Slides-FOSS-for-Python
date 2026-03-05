"""Tests for TextFrame, Paragraph, and Portion CRUD."""
from aspose.slides_foss import Presentation, ShapeType, Portion


def test_text_frame_text():
    """Setting text_frame.text and reading it back."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
        shape.text_frame.text = "Hello, World!"
        assert shape.text_frame.text == "Hello, World!"


def test_overwrite_text():
    """Overwriting text replaces the previous value."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
        shape.text_frame.text = "First"
        shape.text_frame.text = "Second"
        assert shape.text_frame.text == "Second"


def test_paragraphs_count():
    """Setting text creates exactly one paragraph."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
        shape.text_frame.text = "Line"
        assert shape.text_frame.paragraphs.count >= 1


def test_paragraph_text():
    """Reading and modifying paragraph text."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
        shape.text_frame.text = "Original"
        para = shape.text_frame.paragraphs[0]
        assert para.text == "Original"
        para.text = "Modified"
        assert para.text == "Modified"


def test_portions_count():
    """A simple text creates at least one portion."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
        shape.text_frame.text = "Hello"
        assert shape.text_frame.paragraphs[0].portions.count >= 1


def test_add_portion():
    """Adding a Portion appends text."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 100)
        shape.text_frame.text = "Hello "
        new_portion = Portion("World!")
        shape.text_frame.paragraphs[0].portions.add(new_portion)
        assert "World!" in shape.text_frame.text


def test_text_persists(tmp_pptx):
    """Text survives a save/reload cycle."""
    pres = Presentation()
    pres.slides[0].shapes.clear()
    shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
    shape.text_frame.text = "Persistent text"

    pres2 = tmp_pptx(pres)
    assert pres2.slides[0].shapes[0].text_frame.text == "Persistent text"
    pres2.dispose()


def test_add_text_frame():
    """add_text_frame on a shape created without text."""
    with Presentation() as pres:
        shape = pres.slides[0].shapes.add_auto_shape(
            ShapeType.RECTANGLE, 50, 50, 300, 100, False
        )
        shape.add_text_frame("via add_text_frame")
        assert shape.text_frame.text == "via add_text_frame"
