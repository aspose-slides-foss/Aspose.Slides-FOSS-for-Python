"""
FillFormat — solid fill, gradient fill, pattern fill, picture fill, and no fill.
"""
import os
import sys
import struct
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import (
    Presentation, ShapeType, FillType,
    GradientDirection, GradientShape, PatternStyle, PictureFillMode,
)
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def _create_test_png():
    """Create a minimal 2x2 PNG for testing."""
    def _chunk(ct, data):
        c = ct + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 2, 2, 8, 2, 0, 0, 0)
    raw = b"\x00\xff\x00\x00\x00\xff\x00" + b"\x00\x00\x00\xff\x00\x00\xff"
    idat = zlib.compress(raw)
    return header + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")


def solid_fill_rgb():
    """Apply a solid fill with an RGB color."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        shape.fill_format.fill_type = FillType.SOLID
        shape.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 128, 255)

        print("Solid fill with RGB(0, 128, 255)")
        pres.save(os.path.join(OUT, "solid_fill_rgb.pptx"), SaveFormat.PPTX)


def solid_fill_preset_color():
    """Apply a solid fill using a preset (named) color."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        shape.fill_format.fill_type = FillType.SOLID
        shape.fill_format.solid_fill_color.color = Color.coral

        print("Solid fill with Color.coral")
        pres.save(os.path.join(OUT, "solid_fill_preset.pptx"), SaveFormat.PPTX)


def gradient_fill():
    """Apply a gradient fill with multiple stops."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 300, 150)

        shape.fill_format.fill_type = FillType.GRADIENT
        gf = shape.fill_format.gradient_format

        # Set gradient shape and direction
        gf.gradient_shape = GradientShape.LINEAR
        gf.linear_gradient_angle = 45

        # Add gradient stops
        gf.gradient_stops.add(0.0, Color.blue)
        gf.gradient_stops.add(0.5, Color.white)
        gf.gradient_stops.add(1.0, Color.red)

        print(f"Gradient with {len(gf.gradient_stops)} stops, angle=45")
        pres.save(os.path.join(OUT, "gradient_fill.pptx"), SaveFormat.PPTX)


def pattern_fill():
    """Apply a pattern fill with foreground and background colors."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        shape.fill_format.fill_type = FillType.PATTERN
        pf = shape.fill_format.pattern_format
        pf.pattern_style = PatternStyle.PERCENT50
        pf.fore_color.color = Color.dark_blue
        pf.back_color.color = Color.light_yellow

        print(f"Pattern fill: style={pf.pattern_style}")
        pres.save(os.path.join(OUT, "pattern_fill.pptx"), SaveFormat.PPTX)


def picture_fill():
    """Apply a picture fill to a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 200)

        shape.fill_format.fill_type = FillType.PICTURE
        pff = shape.fill_format.picture_fill_format
        pff.picture_fill_mode = PictureFillMode.STRETCH

        # Add an image and assign it
        img = pres.images.add_image(_create_test_png())
        pff.picture.image = img

        print("Picture fill applied (stretch mode)")
        pres.save(os.path.join(OUT, "picture_fill.pptx"), SaveFormat.PPTX)


def no_fill():
    """Set a shape to have no fill (transparent)."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 50, 50, 200, 100)

        shape.fill_format.fill_type = FillType.NO_FILL

        print(f"Fill type: {shape.fill_format.fill_type}")
        pres.save(os.path.join(OUT, "no_fill.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    solid_fill_rgb()
    solid_fill_preset_color()
    gradient_fill()
    pattern_fill()
    picture_fill()
    no_fill()
    print("\n=== test_fill_format.py completed ===")
