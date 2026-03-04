"""
Text formatting — PortionFormat and ParagraphFormat properties.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import (
    Presentation, ShapeType, NullableBool, FillType,
    TextUnderlineType, TextStrikethroughType, TextCapType, TextAlignment,
    FontData,
)
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def bold_italic_underline():
    """Set bold, italic, and underline on text."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
        shape.text_frame.text = "Bold, Italic, Underline"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.font_bold = NullableBool.TRUE
        fmt.font_italic = NullableBool.TRUE
        fmt.font_underline = TextUnderlineType.SINGLE

        print(f"bold={fmt.font_bold}, italic={fmt.font_italic}, underline={fmt.font_underline}")
        pres.save(os.path.join(OUT, "bold_italic_underline.pptx"), SaveFormat.PPTX)


def strikethrough_and_caps():
    """Set strikethrough and text capitalization."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
        shape.text_frame.text = "Strikethrough & All Caps"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.strikethrough_type = TextStrikethroughType.SINGLE
        fmt.text_cap_type = TextCapType.ALL

        print(f"strikethrough={fmt.strikethrough_type}, caps={fmt.text_cap_type}")
        pres.save(os.path.join(OUT, "strikethrough_caps.pptx"), SaveFormat.PPTX)


def font_size_and_spacing():
    """Set font height (size) and character spacing."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 80)
        shape.text_frame.text = "Large spaced text"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.font_height = 28
        fmt.spacing = 5  # extra spacing between characters

        print(f"font_height={fmt.font_height}, spacing={fmt.spacing}")
        pres.save(os.path.join(OUT, "font_size_spacing.pptx"), SaveFormat.PPTX)


def superscript_subscript():
    """Use escapement for superscript and subscript text."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 80)
        shape.text_frame.text = "H"  # initialize with text so portion exists

        from aspose.slides_foss import Portion
        para = shape.text_frame.paragraphs[0]

        # Subscript
        sub = Portion("2")
        sub.portion_format.escapement = -30  # negative = subscript
        para.portions.add(sub)

        # Normal
        normal = Portion("O")
        para.portions.add(normal)

        print(f"Text with sub/superscript: '{shape.text_frame.text}'")
        pres.save(os.path.join(OUT, "super_subscript.pptx"), SaveFormat.PPTX)


def latin_font():
    """Set the Latin font for a text portion."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
        shape.text_frame.text = "Custom Font"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.latin_font = FontData("Courier New")

        print(f"latin_font: {fmt.latin_font.font_name}")
        pres.save(os.path.join(OUT, "latin_font.pptx"), SaveFormat.PPTX)


def text_color():
    """Set text color via portion fill_format."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
        shape.text_frame.text = "Red Text"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.fill_format.fill_type = FillType.SOLID
        fmt.fill_format.solid_fill_color.color = Color.red

        print("Text color set to red")
        pres.save(os.path.join(OUT, "text_color.pptx"), SaveFormat.PPTX)


def highlight_color():
    """Set highlight color on text."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
        shape.text_frame.text = "Highlighted Text"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.highlight_color.color = Color.yellow

        print("Highlight color set to yellow")
        pres.save(os.path.join(OUT, "highlight_color.pptx"), SaveFormat.PPTX)


def language_id():
    """Set the language ID on a text portion."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
        shape.text_frame.text = "English text"

        fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
        fmt.language_id = "en-US"

        print(f"language_id: {fmt.language_id}")
        pres.save(os.path.join(OUT, "language_id.pptx"), SaveFormat.PPTX)


def paragraph_alignment():
    """Set paragraph alignment."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)

        # Set text and center it
        shape.text_frame.text = "Centered text"
        shape.text_frame.paragraphs[0].paragraph_format.alignment = TextAlignment.CENTER

        print(f"alignment: {shape.text_frame.paragraphs[0].paragraph_format.alignment}")
        pres.save(os.path.join(OUT, "paragraph_alignment.pptx"), SaveFormat.PPTX)


def paragraph_spacing():
    """Set paragraph spacing: before, after, and within."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)
        shape.text_frame.text = "Spaced paragraph"

        pf = shape.text_frame.paragraphs[0].paragraph_format
        pf.space_before = 20  # points before paragraph
        pf.space_after = 10   # points after paragraph
        pf.space_within = 150 # line spacing (percentage)

        print(f"space_before={pf.space_before}, space_after={pf.space_after}, space_within={pf.space_within}")
        pres.save(os.path.join(OUT, "paragraph_spacing.pptx"), SaveFormat.PPTX)


def paragraph_indent():
    """Set paragraph margins and indent."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)
        shape.text_frame.text = "Indented paragraph"

        pf = shape.text_frame.paragraphs[0].paragraph_format
        pf.margin_left = 50
        pf.indent = -20  # hanging indent

        print(f"margin_left={pf.margin_left}, indent={pf.indent}")
        pres.save(os.path.join(OUT, "paragraph_indent.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    bold_italic_underline()
    strikethrough_and_caps()
    font_size_and_spacing()
    superscript_subscript()
    latin_font()
    text_color()
    highlight_color()
    language_id()
    paragraph_alignment()
    paragraph_spacing()
    paragraph_indent()
    print("\n=== test_text_formatting.py completed ===")
