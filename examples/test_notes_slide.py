"""
Notes slides — NotesSlideManager, NotesSlide, NotesSize, header/footer manager.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def add_notes_slide():
    """Add a notes slide to a slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        manager = slide.notes_slide_manager

        # Add notes slide
        notes_slide = manager.add_notes_slide()
        print(f"Notes slide added: {notes_slide is not None}")

        # Set notes text
        notes_slide.notes_text_frame.text = "These are speaker notes for slide 1."
        print(f"Notes text: '{notes_slide.notes_text_frame.text}'")

        pres.save(os.path.join(OUT, "add_notes.pptx"), SaveFormat.PPTX)


def access_notes_slide():
    """Access notes slide through the manager."""
    with Presentation() as pres:
        slide = pres.slides[0]
        manager = slide.notes_slide_manager

        # Initially no notes
        manager.add_notes_slide()
        notes = manager.notes_slide
        print(f"Has notes slide: {notes is not None}")

        if notes:
            notes.notes_text_frame.text = "Speaker notes content"
            print(f"Notes text: '{notes.notes_text_frame.text}'")

        pres.save(os.path.join(OUT, "access_notes.pptx"), SaveFormat.PPTX)


def remove_notes_slide():
    """Remove a notes slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        manager = slide.notes_slide_manager

        # Add then remove
        manager.add_notes_slide()
        print(f"Before removal: notes_slide is {manager.notes_slide is not None}")

        manager.remove_notes_slide()
        print(f"After removal: notes_slide is {manager.notes_slide is not None}")

        pres.save(os.path.join(OUT, "remove_notes.pptx"), SaveFormat.PPTX)


def notes_slide_shapes():
    """Access shapes on a notes slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        notes_slide = slide.notes_slide_manager.add_notes_slide()

        print(f"Notes slide shapes: {len(notes_slide.shapes)}")
        for i, shape in enumerate(notes_slide.shapes):
            print(f"  Shape {i}: name='{shape.name}'")


def notes_size():
    """Get and set the notes size for the presentation."""
    with Presentation() as pres:
        ns = pres.notes_size
        size = ns.size
        print(f"Notes size: width={size.width}, height={size.height}")


def header_footer_manager():
    """Manage header and footer visibility on notes slides."""
    with Presentation() as pres:
        slide = pres.slides[0]
        notes_slide = slide.notes_slide_manager.add_notes_slide()
        notes_slide.notes_text_frame.text = "Notes with header/footer"

        hfm = notes_slide.header_footer_manager

        # Set visibility and text via methods
        hfm.set_footer_visibility(True)
        hfm.set_footer_text("Confidential")

        hfm.set_slide_number_visibility(True)
        hfm.set_date_time_visibility(True)
        hfm.set_date_time_text("2026-01-01")

        print(f"Footer visible: {hfm.is_footer_visible}")
        print(f"Slide number visible: {hfm.is_slide_number_visible}")
        print(f"DateTime visible: {hfm.is_date_time_visible}")

        pres.save(os.path.join(OUT, "notes_header_footer.pptx"), SaveFormat.PPTX)


def notes_parent_slide():
    """Access the parent slide from a notes slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        notes = slide.notes_slide_manager.add_notes_slide()
        print(f"Notes parent_slide is same as slide: {notes.parent_slide is slide}")


if __name__ == "__main__":
    add_notes_slide()
    access_notes_slide()
    remove_notes_slide()
    notes_slide_shapes()
    notes_size()
    header_footer_manager()
    notes_parent_slide()
    print("\n=== test_notes_slide.py completed ===")
