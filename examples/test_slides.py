"""
Slides — SlideCollection operations and Slide properties.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def add_empty_slides():
    """Add empty slides using different layouts."""
    with Presentation() as pres:
        # Every new presentation has at least one layout
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        pres.slides.add_empty_slide(layout)
        print(f"After adding 2 slides: {len(pres.slides)} total")
        pres.save(os.path.join(OUT, "add_empty_slides.pptx"), SaveFormat.PPTX)


def insert_empty_slide():
    """Insert an empty slide at a specific index."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        # Insert at position 1 (between the first two slides)
        pres.slides.insert_empty_slide(1, layout)
        print(f"After insert: {len(pres.slides)} slides")
        pres.save(os.path.join(OUT, "insert_empty_slide.pptx"), SaveFormat.PPTX)


def clone_slide():
    """Clone slides using add_clone and insert_clone."""
    with Presentation() as pres:
        # Add a shape to the first slide so we can verify cloning
        from aspose.slides_foss import ShapeType
        slide = pres.slides[0]
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        # Clone to end
        pres.slides.add_clone(slide)
        print(f"After add_clone: {len(pres.slides)} slides")

        # Insert clone at position 1
        pres.slides.insert_clone(1, slide)
        print(f"After insert_clone: {len(pres.slides)} slides")

        pres.save(os.path.join(OUT, "clone_slide.pptx"), SaveFormat.PPTX)


def remove_slides():
    """Remove slides by reference and by index."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        pres.slides.add_empty_slide(layout)
        print(f"Before removal: {len(pres.slides)} slides")

        # Remove by index
        pres.slides.remove_at(2)
        print(f"After remove_at(2): {len(pres.slides)} slides")

        # Remove by reference
        pres.slides.remove(pres.slides[1])
        print(f"After remove(slide): {len(pres.slides)} slides")

        pres.save(os.path.join(OUT, "remove_slides.pptx"), SaveFormat.PPTX)


def slide_properties():
    """Access Slide properties: slide_number, hidden, layout_slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        print(f"slide_number: {slide.slide_number}")
        print(f"hidden: {slide.hidden}")
        print(f"layout_slide type: {type(slide.layout_slide).__name__}")

        # Hide the slide
        slide.hidden = True
        print(f"hidden after set: {slide.hidden}")

        pres.save(os.path.join(OUT, "slide_properties.pptx"), SaveFormat.PPTX)


def index_of_and_to_array():
    """Use index_of and to_array on SlideCollection."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)

        idx = pres.slides.index_of(pres.slides[0])
        print(f"index_of first slide: {idx}")

        arr = pres.slides.to_array()
        print(f"to_array length: {len(arr)}")


def iterate_slides():
    """Iterate over slides in a presentation."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        pres.slides.add_empty_slide(layout)

        for i, slide in enumerate(pres.slides):
            print(f"  Slide {i}: {type(slide).__name__}")


def remove_via_slide_method():
    """Remove a slide using slide.remove()."""
    with Presentation() as pres:
        layout = pres.layout_slides[0]
        pres.slides.add_empty_slide(layout)
        print(f"Before: {len(pres.slides)} slides")

        pres.slides[1].remove()
        print(f"After slide.remove(): {len(pres.slides)} slides")


if __name__ == "__main__":
    add_empty_slides()
    insert_empty_slide()
    clone_slide()
    remove_slides()
    slide_properties()
    index_of_and_to_array()
    iterate_slides()
    remove_via_slide_method()
    print("\n=== test_slides.py completed ===")
