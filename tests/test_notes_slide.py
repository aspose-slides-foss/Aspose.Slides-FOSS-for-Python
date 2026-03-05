"""Tests for NotesSlide, NotesSlideManager, header/footer, NotesSize."""
from aspose.slides_foss import Presentation


def test_add_notes(tmp_pptx):
    """Notes text persists after save/reload."""
    pres = Presentation()
    slide = pres.slides[0]
    notes = slide.notes_slide_manager.add_notes_slide()
    notes.notes_text_frame.text = "Speaker notes"

    pres2 = tmp_pptx(pres)
    ns2 = pres2.slides[0].notes_slide_manager.notes_slide
    assert ns2 is not None
    assert ns2.notes_text_frame.text == "Speaker notes"
    pres2.dispose()


def test_remove_notes(tmp_pptx):
    """Removing notes persists."""
    pres = Presentation()
    mgr = pres.slides[0].notes_slide_manager
    mgr.add_notes_slide()
    assert mgr.notes_slide is not None

    mgr.remove_notes_slide()
    assert mgr.notes_slide is None

    pres2 = tmp_pptx(pres)
    assert pres2.slides[0].notes_slide_manager.notes_slide is None
    pres2.dispose()


def test_notes_header_footer(tmp_pptx):
    """Header/footer visibility persists."""
    pres = Presentation()
    notes = pres.slides[0].notes_slide_manager.add_notes_slide()
    notes.notes_text_frame.text = "Notes"
    hfm = notes.header_footer_manager
    hfm.set_footer_visibility(True)
    hfm.set_footer_text("Confidential")
    hfm.set_slide_number_visibility(True)

    assert hfm.is_footer_visible is True
    assert hfm.is_slide_number_visible is True

    pres2 = tmp_pptx(pres)
    ns2 = pres2.slides[0].notes_slide_manager.notes_slide
    hfm2 = ns2.header_footer_manager
    assert hfm2.is_footer_visible is True
    assert hfm2.is_slide_number_visible is True
    pres2.dispose()


def test_notes_parent_slide():
    """Notes slide references its parent slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        notes = slide.notes_slide_manager.add_notes_slide()
        assert notes.parent_slide is slide


def test_notes_size():
    """Notes size has positive width and height."""
    with Presentation() as pres:
        ns = pres.notes_size
        assert ns.size.width > 0
        assert ns.size.height > 0
