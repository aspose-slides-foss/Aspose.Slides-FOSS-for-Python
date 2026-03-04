"""
Shapes — ShapeCollection operations and shape frame properties.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def add_auto_shapes():
    """Add various auto shapes to a slide."""
    with Presentation() as pres:
        slide = pres.slides[0]

        # Add a rectangle
        rect = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        print(f"Added rectangle: {rect.shape_type}")

        # Add an ellipse
        ellipse = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        print(f"Added ellipse: {ellipse.shape_type}")

        # Add a rounded rectangle
        rrect = slide.shapes.add_auto_shape(ShapeType.ROUND_CORNER_RECTANGLE, 50, 200, 200, 100)
        print(f"Added rounded rectangle: {rrect.shape_type}")

        print(f"Total shapes: {len(slide.shapes)}")
        pres.save(os.path.join(OUT, "add_auto_shapes.pptx"), SaveFormat.PPTX)


def insert_auto_shape():
    """Insert an auto shape at a specific index."""
    with Presentation() as pres:
        slide = pres.slides[0]
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)

        # Insert a triangle at index 1
        tri = slide.shapes.insert_auto_shape(1, ShapeType.TRIANGLE, 150, 200, 100, 100)
        print(f"Inserted triangle at index 1, total shapes: {len(slide.shapes)}")
        pres.save(os.path.join(OUT, "insert_auto_shape.pptx"), SaveFormat.PPTX)


def remove_shapes():
    """Remove shapes by reference and by index."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape1 = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        shape2 = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        slide.shapes.add_auto_shape(ShapeType.TRIANGLE, 150, 200, 100, 100)
        print(f"Before removal: {len(slide.shapes)} shapes")

        # Remove by reference
        slide.shapes.remove(shape1)
        print(f"After remove(rect): {len(slide.shapes)} shapes")

        # Remove by index
        slide.shapes.remove_at(0)
        print(f"After remove_at(0): {len(slide.shapes)} shapes")

        pres.save(os.path.join(OUT, "remove_shapes.pptx"), SaveFormat.PPTX)


def clear_shapes():
    """Clear all shapes from a slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        print(f"Before clear: {len(slide.shapes)} shapes")

        slide.shapes.clear()
        print(f"After clear: {len(slide.shapes)} shapes")

        pres.save(os.path.join(OUT, "clear_shapes.pptx"), SaveFormat.PPTX)


def index_of_and_to_array():
    """Use index_of and to_array on ShapeCollection."""
    with Presentation() as pres:
        slide = pres.slides[0]
        rect = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)

        idx = slide.shapes.index_of(rect)
        print(f"index_of rectangle: {idx}")

        arr = slide.shapes.to_array()
        print(f"to_array length: {len(arr)}")


def reorder_shapes():
    """Reorder a shape to a different position."""
    with Presentation() as pres:
        slide = pres.slides[0]
        rect = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        ellipse = slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)

        print(f"Before reorder: shapes[0]={slide.shapes[0].shape_type}")
        slide.shapes.reorder(0, ellipse)
        print(f"After reorder:  shapes[0]={slide.shapes[0].shape_type}")

        pres.save(os.path.join(OUT, "reorder_shapes.pptx"), SaveFormat.PPTX)


def shape_frame_properties():
    """Access and modify shape frame: x, y, width, height, rotation."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 150)

        # Read frame properties
        print(f"x={shape.x}, y={shape.y}, width={shape.width}, height={shape.height}")
        print(f"rotation={shape.rotation}")

        # Modify frame properties
        shape.x = 200
        shape.y = 200
        shape.width = 300
        shape.height = 200
        shape.rotation = 45
        print(f"After change: x={shape.x}, y={shape.y}, w={shape.width}, h={shape.height}, rot={shape.rotation}")

        pres.save(os.path.join(OUT, "shape_frame.pptx"), SaveFormat.PPTX)


def iterate_shapes():
    """Iterate over all shapes on a slide."""
    with Presentation() as pres:
        slide = pres.slides[0]
        slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)
        slide.shapes.add_auto_shape(ShapeType.ELLIPSE, 300, 50, 150, 150)
        slide.shapes.add_auto_shape(ShapeType.TRIANGLE, 150, 200, 100, 100)

        for i, shape in enumerate(slide.shapes):
            print(f"  Shape {i}: type={shape.shape_type}, name='{shape.name}'")


if __name__ == "__main__":
    add_auto_shapes()
    insert_auto_shape()
    remove_shapes()
    clear_shapes()
    index_of_and_to_array()
    reorder_shapes()
    shape_frame_properties()
    iterate_shapes()
    print("\n=== test_shapes.py completed ===")
