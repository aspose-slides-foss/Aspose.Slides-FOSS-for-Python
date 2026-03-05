"""Tests for ShapeCollection operations and shape frame properties."""
from aspose.slides_foss import Presentation, ShapeType


def _blank_slide(pres):
    """Return a slide with all placeholder shapes removed."""
    slide = pres.slides[0]
    slide.shapes.clear()
    return slide


def test_add_auto_shape():
    """add_auto_shape adds a rectangle with correct type."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        assert len(slide.shapes) == 1
        assert shape.shape_type == ShapeType.RECTANGLE


def test_multiple_shape_types():
    """Various ShapeType values are preserved."""
    types = [ShapeType.RECTANGLE, ShapeType.ELLIPSE, ShapeType.TRIANGLE]
    with Presentation() as pres:
        slide = _blank_slide(pres)
        for st in types:
            s = slide.shapes.add_auto_shape(st, 10, 10, 100, 100)
            assert s.shape_type == st
        assert len(slide.shapes) == 3


def test_insert_auto_shape():
    """insert_auto_shape places a shape at the requested index."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        slide.shapes.insert_auto_shape(1, ShapeType.TRIANGLE, 150, 200, 100, 100)
        assert len(slide.shapes) == 3


def test_remove_shape():
    """Removing a shape by reference decreases count."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        s = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        assert len(slide.shapes) == 2
        slide.shapes.remove(s)
        assert len(slide.shapes) == 1


def test_remove_at():
    """remove_at removes by index."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        slide.shapes.remove_at(0)
        assert len(slide.shapes) == 1


def test_clear_shapes():
    """clear() empties the shape collection."""
    with Presentation() as pres:
        slide = pres.slides[0]
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.clear()
        assert len(slide.shapes) == 0


def test_shape_frame_properties(tmp_pptx):
    """x, y, width, height, rotation persist after save/reload."""
    pres = Presentation()
    slide = _blank_slide(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 200, 200, 300, 250)
    shape.rotation = 45

    pres2 = tmp_pptx(pres)
    s2 = pres2.slides[0].shapes[0]
    assert s2.x == 200
    assert s2.y == 200
    assert s2.width == 300
    assert s2.height == 250
    assert s2.rotation == 45
    pres2.dispose()


def test_reorder_shapes():
    """reorder() changes the z-order of shapes."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        ellipse = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        slide.shapes.reorder(0, ellipse)
        assert slide.shapes[0].shape_type == ShapeType.ELLIPSE


def test_iterate_shapes():
    """Shapes collection is iterable."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        shapes = list(slide.shapes)
        assert len(shapes) == 2


def test_shape_persists_after_reload(tmp_pptx):
    """Shapes survive a save/reload cycle."""
    pres = Presentation()
    slide = _blank_slide(pres)
    slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

    pres2 = tmp_pptx(pres)
    assert len(pres2.slides[0].shapes) >= 1
    assert pres2.slides[0].shapes[0].shape_type == ShapeType.RECTANGLE
    pres2.dispose()
