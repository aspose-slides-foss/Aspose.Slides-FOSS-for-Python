"""
TextFrameFormat — margins, wrap, anchoring, autofit, columns, rotation, vertical text.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import (
    Presentation, ShapeType, NullableBool,
    TextAutofitType, TextVerticalType,
)
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def text_frame_margins():
    """Set internal margins on a text frame."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 150)
        shape.text_frame.text = "Text with margins"

        tff = shape.text_frame.text_frame_format
        tff.margin_left = 20
        tff.margin_right = 20
        tff.margin_top = 10
        tff.margin_bottom = 10

        print(f"Margins: L={tff.margin_left}, R={tff.margin_right}, T={tff.margin_top}, B={tff.margin_bottom}")
        pres.save(os.path.join(OUT, "text_frame_margins.pptx"), SaveFormat.PPTX)


def word_wrap():
    """Enable or disable word wrap in a text frame."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        shape.text_frame.text = "This is a long text that should wrap within the shape boundaries."

        tff = shape.text_frame.text_frame_format
        tff.word_wrap = NullableBool.TRUE

        print(f"word_wrap: {tff.word_wrap}")
        pres.save(os.path.join(OUT, "word_wrap.pptx"), SaveFormat.PPTX)


def anchoring_type():
    """Set text anchoring (vertical alignment within the shape)."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 200)
        shape.text_frame.text = "Bottom-anchored text"

        from aspose.slides_foss.TextAnchorType import TextAnchorType
        tff = shape.text_frame.text_frame_format
        tff.anchoring_type = TextAnchorType.BOTTOM

        print(f"anchoring_type: {tff.anchoring_type}")
        pres.save(os.path.join(OUT, "anchoring_type.pptx"), SaveFormat.PPTX)


def center_text():
    """Center text vertically in the shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 200)
        shape.text_frame.text = "Centered text"

        tff = shape.text_frame.text_frame_format
        tff.center_text = NullableBool.TRUE

        print(f"center_text: {tff.center_text}")
        pres.save(os.path.join(OUT, "center_text.pptx"), SaveFormat.PPTX)


def vertical_text():
    """Set text direction to vertical."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 100, 300)
        shape.text_frame.text = "Vertical"

        tff = shape.text_frame.text_frame_format
        tff.text_vertical_type = TextVerticalType.VERTICAL

        print(f"text_vertical_type: {tff.text_vertical_type}")
        pres.save(os.path.join(OUT, "vertical_text.pptx"), SaveFormat.PPTX)


def autofit_type():
    """Set autofit type on a text frame."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)
        shape.text_frame.text = "Auto-shrink text that is quite long and might overflow the shape."

        tff = shape.text_frame.text_frame_format
        tff.autofit_type = TextAutofitType.NORMAL  # shrink text to fit

        print(f"autofit_type: {tff.autofit_type}")
        pres.save(os.path.join(OUT, "autofit_type.pptx"), SaveFormat.PPTX)


def columns():
    """Set column count and column spacing in a text frame."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 500, 200)
        shape.text_frame.text = (
            "This text is split across multiple columns. "
            "Column layout helps organize content in a wider shape."
        )

        tff = shape.text_frame.text_frame_format
        tff.column_count = 2
        tff.column_spacing = 20

        print(f"column_count={tff.column_count}, column_spacing={tff.column_spacing}")
        pres.save(os.path.join(OUT, "columns.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    text_frame_margins()
    word_wrap()
    anchoring_type()
    center_text()
    vertical_text()
    autofit_type()
    columns()
    print("\n=== test_text_frame_format.py completed ===")
