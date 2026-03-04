"""
Presentation — create, load, save, context manager, and core properties.
"""
import os
import io
import datetime
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def create_new_presentation():
    """Create a brand-new empty presentation and save it."""
    pres = Presentation()
    print(f"New presentation has {len(pres.slides)} slide(s)")
    pres.save(os.path.join(OUT, "new_presentation.pptx"), SaveFormat.PPTX)
    pres.dispose()
    print("Saved new_presentation.pptx")


def load_and_resave():
    """Load a previously-saved file and resave it."""
    path = os.path.join(OUT, "new_presentation.pptx")
    pres = Presentation(path)
    print(f"Loaded presentation with {len(pres.slides)} slide(s)")
    pres.save(os.path.join(OUT, "resaved_presentation.pptx"), SaveFormat.PPTX)
    pres.dispose()
    print("Saved resaved_presentation.pptx")


def save_to_stream():
    """Save a presentation to a BytesIO stream."""
    pres = Presentation()
    stream = io.BytesIO()
    pres.save(stream, SaveFormat.PPTX)
    print(f"Saved to stream, size = {stream.tell()} bytes")
    pres.dispose()


def context_manager():
    """Use the presentation as a context manager."""
    with Presentation() as pres:
        print(f"Inside context manager, slides: {len(pres.slides)}")
        pres.save(os.path.join(OUT, "context_manager.pptx"), SaveFormat.PPTX)
    print("Context manager exited cleanly")


def first_slide_number():
    """Get and set the first slide number."""
    with Presentation() as pres:
        print(f"Default first_slide_number: {pres.first_slide_number}")
        pres.first_slide_number = 5
        print(f"Changed first_slide_number: {pres.first_slide_number}")
        pres.save(os.path.join(OUT, "first_slide_number.pptx"), SaveFormat.PPTX)


def current_date_time_property():
    """Get and set current_date_time on the presentation."""
    with Presentation() as pres:
        now = datetime.datetime.now()
        pres.current_date_time = now
        print(f"current_date_time set to: {pres.current_date_time}")


def source_format_property():
    """Read the source_format of a presentation."""
    with Presentation() as pres:
        print(f"source_format: {pres.source_format}")


if __name__ == "__main__":
    create_new_presentation()
    load_and_resave()
    save_to_stream()
    context_manager()
    first_slide_number()
    current_date_time_property()
    source_format_property()
    print("\n=== test_presentation.py completed ===")
