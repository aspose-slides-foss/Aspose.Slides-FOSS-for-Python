"""Tests for FillFormat: solid, gradient, pattern, picture, no-fill."""
from aspose.slides_foss import (
    Presentation, ShapeType, FillType,
    GradientShape, PatternStyle, PictureFillMode,
)
from aspose.slides_foss.drawing import Color

from conftest import create_test_png


def _clear(pres):
    pres.slides[0].shapes.clear()
    return pres.slides[0]


def test_solid_fill(tmp_pptx):
    """Solid fill colour persists after save/reload."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
    shape.fill_format.fill_type = FillType.SOLID
    shape.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 128, 255)

    pres2 = tmp_pptx(pres)
    ff = pres2.slides[0].shapes[0].fill_format
    assert ff.fill_type == FillType.SOLID
    c = ff.solid_fill_color.color
    assert c.r == 0 and c.g == 128 and c.b == 255
    pres2.dispose()


def test_gradient_fill(tmp_pptx):
    """Gradient stops and angle persist."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 150)
    shape.fill_format.fill_type = FillType.GRADIENT
    gf = shape.fill_format.gradient_format
    gf.gradient_shape = GradientShape.LINEAR
    gf.linear_gradient_angle = 45
    gf.gradient_stops.add(0.0, Color.blue)
    gf.gradient_stops.add(1.0, Color.red)

    pres2 = tmp_pptx(pres)
    ff2 = pres2.slides[0].shapes[0].fill_format
    assert ff2.fill_type == FillType.GRADIENT
    assert len(ff2.gradient_format.gradient_stops) >= 2
    pres2.dispose()


def test_pattern_fill(tmp_pptx):
    """Pattern style and colours persist."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
    shape.fill_format.fill_type = FillType.PATTERN
    pf = shape.fill_format.pattern_format
    pf.pattern_style = PatternStyle.PERCENT50
    pf.fore_color.color = Color.dark_blue
    pf.back_color.color = Color.light_yellow

    pres2 = tmp_pptx(pres)
    ff2 = pres2.slides[0].shapes[0].fill_format
    assert ff2.fill_type == FillType.PATTERN
    assert ff2.pattern_format.pattern_style == PatternStyle.PERCENT50
    pres2.dispose()


def test_no_fill(tmp_pptx):
    """NO_FILL type persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
    shape.fill_format.fill_type = FillType.NO_FILL

    pres2 = tmp_pptx(pres)
    assert pres2.slides[0].shapes[0].fill_format.fill_type == FillType.NO_FILL
    pres2.dispose()


def test_picture_fill(tmp_pptx):
    """Picture fill with an image persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 200)
    shape.fill_format.fill_type = FillType.PICTURE
    pff = shape.fill_format.picture_fill_format
    pff.picture_fill_mode = PictureFillMode.STRETCH
    img = pres.images.add_image(create_test_png(0, 255, 0))
    pff.picture.image = img

    pres2 = tmp_pptx(pres)
    ff2 = pres2.slides[0].shapes[0].fill_format
    assert ff2.fill_type == FillType.PICTURE
    pres2.dispose()
