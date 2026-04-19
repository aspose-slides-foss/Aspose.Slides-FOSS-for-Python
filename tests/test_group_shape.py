"""Tests for GroupShape creation, child shapes, and persistence."""
from aspose.slides_foss import Presentation, ShapeType, GroupShape


def _blank_slide(pres):
    """Return a slide with all placeholder shapes removed."""
    slide = pres.slides[0]
    slide.shapes.clear()
    return slide


def test_add_group_shape():
    """add_group_shape creates a GroupShape in the slide's shape collection."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert isinstance(group, GroupShape)
        assert len(slide.shapes) == 1


def test_group_shape_has_empty_child_collection():
    """A new group shape starts with zero child shapes."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert len(group.shapes) == 0


def test_add_auto_shapes_inside_group():
    """AutoShapes can be added inside a group shape."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        group.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        group.shapes.add_auto_shape(ShapeType.ELLIPSE, 350, 100, 150, 150)
        assert len(group.shapes) == 2
        assert len(slide.shapes) == 1


def test_group_child_shape_properties():
    """Child shapes inside a group have correct properties."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        shape = group.shapes.add_auto_shape(ShapeType.RECTANGLE, 300, 100, 100, 100)
        assert shape.shape_type == ShapeType.RECTANGLE
        assert shape.x == 300
        assert shape.y == 100
        assert shape.width == 100
        assert shape.height == 100


def test_group_shape_name():
    """Group shape has an auto-generated name."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert group.name.startswith("Group")


def test_group_shape_is_text_holder():
    """GroupShape.is_text_holder returns False."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert group.is_text_holder is False


def test_group_shape_as_i_shape():
    """as_i_shape returns the group shape itself."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert group.as_i_shape is group


def test_child_shape_is_grouped():
    """Shapes inside a group report is_grouped = True."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        shape = group.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 50, 50)
        assert shape.is_grouped is True


def test_group_shape_parent_group():
    """The child collection's parent_group points to the GroupShape."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert group.shapes.parent_group is group


def test_slide_shapes_parent_group_is_none():
    """The slide-level shape collection has no parent group."""
    with Presentation() as pres:
        slide = pres.slides[0]
        assert slide.shapes.parent_group is None


def test_group_shape_lock_defaults():
    """All lock flags are False by default."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        lock = group.group_shape_lock
        assert lock.grouping_locked is False
        assert lock.ungrouping_locked is False
        assert lock.select_locked is False
        assert lock.rotation_locked is False
        assert lock.aspect_ratio_locked is False
        assert lock.position_locked is False
        assert lock.size_locked is False
        assert lock.no_locks is True


def test_group_shape_lock_set():
    """Lock flags can be set and read back."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        group.group_shape_lock.ungrouping_locked = True
        assert group.group_shape_lock.ungrouping_locked is True
        assert group.group_shape_lock.no_locks is False


def test_group_shape_persists_after_save(tmp_pptx):
    """Group shape and its children survive save/reload."""
    pres = Presentation()
    slide = _blank_slide(pres)
    group = slide.shapes.add_group_shape()
    group.shapes.add_auto_shape(ShapeType.RECTANGLE, 300, 100, 100, 100)
    group.shapes.add_auto_shape(ShapeType.RECTANGLE, 500, 100, 100, 100)
    group.name = "TestGroup"

    pres2 = tmp_pptx(pres)
    slide2 = pres2.slides[0]
    assert len(slide2.shapes) == 1

    reloaded = slide2.shapes[0]
    assert isinstance(reloaded, GroupShape)
    assert reloaded.name == "TestGroup"
    assert len(reloaded.shapes) == 2
    pres2.dispose()


def test_group_shape_alternative_text(tmp_pptx):
    """Group shape alternative text persists."""
    pres = Presentation()
    slide = _blank_slide(pres)
    group = slide.shapes.add_group_shape()
    group.alternative_text = "A group of shapes"

    pres2 = tmp_pptx(pres)
    reloaded = pres2.slides[0].shapes[0]
    assert reloaded.alternative_text == "A group of shapes"
    pres2.dispose()


def test_remove_group_shape():
    """Group shape can be removed from the slide."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        assert len(slide.shapes) == 1
        slide.shapes.remove(group)
        assert len(slide.shapes) == 0


def test_iterate_group_children():
    """Child shapes of a group are iterable."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        group = slide.shapes.add_group_shape()
        group.shapes.add_auto_shape(ShapeType.RECTANGLE, 0, 0, 50, 50)
        group.shapes.add_auto_shape(ShapeType.ELLIPSE, 60, 0, 50, 50)
        group.shapes.add_auto_shape(ShapeType.TRIANGLE, 120, 0, 50, 50)
        children = list(group.shapes)
        assert len(children) == 3


def test_isinstance_detection():
    """GroupShape can be detected with isinstance when iterating slide shapes."""
    with Presentation() as pres:
        slide = _blank_slide(pres)
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 10, 10, 50, 50)
        slide.shapes.add_group_shape()
        groups = [s for s in slide.shapes if isinstance(s, GroupShape)]
        assert len(groups) == 1
