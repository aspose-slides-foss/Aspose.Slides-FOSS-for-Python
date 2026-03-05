"""Tests for LineFormat: colour, width, dash style."""
from aspose.slides_foss import (
    Presentation, ShapeType, FillType,
    LineDashStyle,
)
from aspose.slides_foss.drawing import Color


def _clear(pres):
    pres.slides[0].shapes.clear()
    return pres.slides[0]


def test_line_color_and_width(tmp_pptx):
    """Line colour and width persist after save/reload."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
    lf = shape.line_format
    lf.width = 5
    lf.fill_format.fill_type = FillType.SOLID
    lf.fill_format.solid_fill_color.color = Color.dark_red

    pres2 = tmp_pptx(pres)
    lf2 = pres2.slides[0].shapes[0].line_format
    assert lf2.width == 5
    assert lf2.fill_format.fill_type == FillType.SOLID
    c = lf2.fill_format.solid_fill_color.color
    assert c.r == Color.dark_red.r
    pres2.dispose()


def test_line_dash_style(tmp_pptx):
    """Dash style persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
    lf = shape.line_format
    lf.width = 3
    lf.dash_style = LineDashStyle.DASH
    lf.fill_format.fill_type = FillType.SOLID
    lf.fill_format.solid_fill_color.color = Color.black

    pres2 = tmp_pptx(pres)
    lf2 = pres2.slides[0].shapes[0].line_format
    assert lf2.dash_style == LineDashStyle.DASH
    pres2.dispose()


def test_multiple_dash_styles():
    """Various dash styles can be set in-memory."""
    styles = [LineDashStyle.SOLID, LineDashStyle.DASH, LineDashStyle.DOT, LineDashStyle.DASH_DOT]
    with Presentation() as pres:
        slide = pres.slides[0]
        for style in styles:
            shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 50)
            shape.line_format.dash_style = style
            assert shape.line_format.dash_style == style
