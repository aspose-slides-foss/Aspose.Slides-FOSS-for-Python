"""Tests for text formatting: bold, italic, underline, font, colour, alignment."""
from aspose.slides_foss import (
    Presentation, ShapeType, NullableBool, FillType,
    TextUnderlineType, TextStrikethroughType, TextAlignment,
    FontData,
)
from aspose.slides_foss.drawing import Color


def _shaped(pres):
    """Helper: clear slide, add a rectangle with text and return (shape, portion_format)."""
    pres.slides[0].shapes.clear()
    shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 60)
    shape.text_frame.text = "Sample"
    fmt = shape.text_frame.paragraphs[0].portions[0].portion_format
    return shape, fmt


def test_bold_italic(tmp_pptx):
    """Bold and italic persist after save/reload."""
    pres = Presentation()
    _, fmt = _shaped(pres)
    fmt.font_bold = NullableBool.TRUE
    fmt.font_italic = NullableBool.TRUE

    pres2 = tmp_pptx(pres)
    fmt2 = pres2.slides[0].shapes[0].text_frame.paragraphs[0].portions[0].portion_format
    assert fmt2.font_bold == NullableBool.TRUE
    assert fmt2.font_italic == NullableBool.TRUE
    pres2.dispose()


def test_underline(tmp_pptx):
    """Underline type persists."""
    pres = Presentation()
    _, fmt = _shaped(pres)
    fmt.font_underline = TextUnderlineType.SINGLE

    pres2 = tmp_pptx(pres)
    fmt2 = pres2.slides[0].shapes[0].text_frame.paragraphs[0].portions[0].portion_format
    assert fmt2.font_underline == TextUnderlineType.SINGLE
    pres2.dispose()


def test_strikethrough(tmp_pptx):
    """Strikethrough type persists."""
    pres = Presentation()
    _, fmt = _shaped(pres)
    fmt.strikethrough_type = TextStrikethroughType.SINGLE

    pres2 = tmp_pptx(pres)
    fmt2 = pres2.slides[0].shapes[0].text_frame.paragraphs[0].portions[0].portion_format
    assert fmt2.strikethrough_type == TextStrikethroughType.SINGLE
    pres2.dispose()


def test_font_size(tmp_pptx):
    """font_height persists."""
    pres = Presentation()
    _, fmt = _shaped(pres)
    fmt.font_height = 28

    pres2 = tmp_pptx(pres)
    fmt2 = pres2.slides[0].shapes[0].text_frame.paragraphs[0].portions[0].portion_format
    assert fmt2.font_height == 28
    pres2.dispose()


def test_font_color(tmp_pptx):
    """Solid fill colour on portion text persists."""
    pres = Presentation()
    _, fmt = _shaped(pres)
    fmt.fill_format.fill_type = FillType.SOLID
    fmt.fill_format.solid_fill_color.color = Color.red

    pres2 = tmp_pptx(pres)
    fmt2 = pres2.slides[0].shapes[0].text_frame.paragraphs[0].portions[0].portion_format
    assert fmt2.fill_format.fill_type == FillType.SOLID
    c = fmt2.fill_format.solid_fill_color.color
    assert c.r == 255 and c.g == 0 and c.b == 0
    pres2.dispose()


def test_latin_font(tmp_pptx):
    """latin_font persists."""
    pres = Presentation()
    _, fmt = _shaped(pres)
    fmt.latin_font = FontData("Courier New")

    pres2 = tmp_pptx(pres)
    fmt2 = pres2.slides[0].shapes[0].text_frame.paragraphs[0].portions[0].portion_format
    assert fmt2.latin_font.font_name == "Courier New"
    pres2.dispose()


def test_paragraph_alignment(tmp_pptx):
    """Paragraph alignment persists."""
    pres = Presentation()
    pres.slides[0].shapes.clear()
    shape = pres.slides[0].shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)
    shape.text_frame.text = "Centered"
    shape.text_frame.paragraphs[0].paragraph_format.alignment = TextAlignment.CENTER

    pres2 = tmp_pptx(pres)
    pf = pres2.slides[0].shapes[0].text_frame.paragraphs[0].paragraph_format
    assert pf.alignment == TextAlignment.CENTER
    pres2.dispose()
