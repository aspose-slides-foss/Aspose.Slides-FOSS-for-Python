"""
Text — TextFrame, Paragraph, and Portion basics.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def text_frame_get_set():
    """Get and set the text of a TextFrame directly."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 100)

        # Set text
        shape.text_frame.text = "Hello, World!"
        print(f"TextFrame.text: '{shape.text_frame.text}'")

        # Overwrite text
        shape.text_frame.text = "Updated text"
        print(f"After update: '{shape.text_frame.text}'")

        pres.save(os.path.join(OUT, "text_frame.pptx"), SaveFormat.PPTX)


def paragraphs_collection():
    """Access paragraphs in a text frame."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 200)
        shape.text_frame.text = "First paragraph"

        print(f"Number of paragraphs: {shape.text_frame.paragraphs.count}")

        for i, para in enumerate(shape.text_frame.paragraphs):
            print(f"  Paragraph {i}: '{para.text}'")


def paragraph_text():
    """Get and set individual paragraph text."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 200)
        shape.text_frame.text = "First line"

        para = shape.text_frame.paragraphs[0]
        print(f"Paragraph text: '{para.text}'")

        # Set paragraph text
        para.text = "Modified paragraph"
        print(f"After set: '{para.text}'")

        pres.save(os.path.join(OUT, "paragraph_text.pptx"), SaveFormat.PPTX)


def portions_collection():
    """Access portions within a paragraph."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 200)
        shape.text_frame.text = "Hello"

        para = shape.text_frame.paragraphs[0]
        print(f"Number of portions: {para.portions.count}")

        for i, portion in enumerate(para.portions):
            print(f"  Portion {i}: '{portion.text}'")


def portion_text():
    """Get and set portion text."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 200)
        shape.text_frame.text = "Original"

        portion = shape.text_frame.paragraphs[0].portions[0]
        print(f"Portion text: '{portion.text}'")

        portion.text = "Changed"
        print(f"After set: '{portion.text}'")
        print(f"TextFrame now: '{shape.text_frame.text}'")

        pres.save(os.path.join(OUT, "portion_text.pptx"), SaveFormat.PPTX)


def create_new_portion():
    """Create a new Portion and add it to a paragraph."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 400, 200)
        shape.text_frame.text = "Hello "

        # Create a new portion with text
        from aspose.slides_foss import Portion
        new_portion = Portion("World!")
        shape.text_frame.paragraphs[0].portions.add(new_portion)

        print(f"TextFrame text: '{shape.text_frame.text}'")
        print(f"Portions count: {shape.text_frame.paragraphs[0].portions.count}")

        pres.save(os.path.join(OUT, "new_portion.pptx"), SaveFormat.PPTX)


def add_text_frame():
    """Use add_text_frame to set initial text on a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(
            ShapeType.RECTANGLE, 50, 50, 300, 100, False
        )

        # add_text_frame creates the text frame with initial text
        shape.add_text_frame("Text via add_text_frame")
        print(f"Text: '{shape.text_frame.text}'")

        pres.save(os.path.join(OUT, "add_text_frame.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    text_frame_get_set()
    paragraphs_collection()
    paragraph_text()
    portions_collection()
    portion_text()
    create_new_portion()
    add_text_frame()
    print("\n=== test_text.py completed ===")
