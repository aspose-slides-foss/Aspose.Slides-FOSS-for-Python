"""Tests for SlideCollection operations and Slide properties."""
from aspose.slides_foss import Presentation, ShapeType


def test_add_empty_slide():
    """add_empty_slide increases slide count."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        assert len(pres.slides) == 2


def test_insert_empty_slide():
    """insert_empty_slide places a slide at the given index."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        pres.slides.insert_empty_slide(1, layout)
        assert len(pres.slides) == 3


def test_remove_slide_by_ref():
    """Removing a slide by reference decreases count."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        assert len(pres.slides) == 2
        pres.slides.remove(pres.slides[1])
        assert len(pres.slides) == 1


def test_remove_slide_at():
    """remove_at removes by index."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        pres.slides.remove_at(1)
        assert len(pres.slides) == 1


def test_slide_hidden(tmp_pptx):
    """Setting hidden persists across save/reload."""
    pres = Presentation()
    pres.slides[0].hidden = True
    assert pres.slides[0].hidden is True

    pres2 = tmp_pptx(pres)
    assert pres2.slides[0].hidden is True
    pres2.dispose()


def test_clone_slide():
    """add_clone duplicates a slide with its shapes."""
    with Presentation() as pres:
        slide = pres.slides[0]
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        pres.slides.add_clone(slide)
        assert len(pres.slides) == 2
        assert len(pres.slides[1].shapes) >= 1


def test_slide_layout_access():
    """Each slide exposes its layout_slide."""
    with Presentation() as pres:
        assert pres.slides[0].layout_slide is not None


def test_slide_name(tmp_pptx):
    """Slide name persists after save/reload."""
    pres = Presentation()
    pres.slides[0].name = "MySlide"
    assert pres.slides[0].name == "MySlide"

    pres2 = tmp_pptx(pres)
    assert pres2.slides[0].name == "MySlide"
    pres2.dispose()


def test_iterate_slides():
    """Slides are iterable."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        slides = list(pres.slides)
        assert len(slides) == 2


def test_index_of():
    """index_of returns the correct position."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        assert pres.slides.index_of(pres.slides[0]) == 0
        assert pres.slides.index_of(pres.slides[1]) == 1
