"""
PictureFrame — add images to slides using ImageCollection and PictureFrame.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def _create_test_png():
    """Create a minimal valid PNG image (1x1 red pixel) for testing."""
    import struct
    import zlib

    def _chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw_row = b"\x00\xff\x00\x00"  # filter=none, R=255, G=0, B=0
    idat_data = zlib.compress(raw_row)
    return header + _chunk(b"IHDR", ihdr_data) + _chunk(b"IDAT", idat_data) + _chunk(b"IEND", b"")


def add_picture_from_bytes():
    """Add an image from raw bytes and create a PictureFrame."""
    with Presentation() as pres:
        slide = pres.slides[0]
        image_data = _create_test_png()

        # Add image to the presentation image collection
        pp_image = pres.images.add_image(image_data)
        print(f"Image added, collection size: {len(pres.images)}")

        # Create a picture frame on the slide
        pic_frame = slide.shapes.add_picture_frame(
            ShapeType.RECTANGLE, 100, 100, 200, 200, pp_image
        )
        print(f"PictureFrame shape_type: {pic_frame.shape_type}")
        print(f"PictureFrame position: x={pic_frame.x}, y={pic_frame.y}")

        pres.save(os.path.join(OUT, "picture_from_bytes.pptx"), SaveFormat.PPTX)
        print("Saved picture_from_bytes.pptx")


def add_picture_from_file():
    """Add an image from a file path."""
    # First save a test image to disk
    image_path = os.path.join(OUT, "test_image.png")
    with open(image_path, "wb") as f:
        f.write(_create_test_png())

    with Presentation() as pres:
        slide = pres.slides[0]

        # Read the file and add to collection
        with open(image_path, "rb") as f:
            pp_image = pres.images.add_image(f.read())

        # Create picture frame
        pic_frame = slide.shapes.add_picture_frame(
            ShapeType.RECTANGLE, 50, 50, 300, 300, pp_image
        )
        print(f"Picture from file: shape_type={pic_frame.shape_type}")

        pres.save(os.path.join(OUT, "picture_from_file.pptx"), SaveFormat.PPTX)
        print("Saved picture_from_file.pptx")


def multiple_images():
    """Add multiple images to the same presentation."""
    with Presentation() as pres:
        slide = pres.slides[0]
        image_data = _create_test_png()

        # Add two images
        img1 = pres.images.add_image(image_data)
        img2 = pres.images.add_image(image_data)

        slide.shapes.add_picture_frame(ShapeType.RECTANGLE, 50, 50, 150, 150, img1)
        slide.shapes.add_picture_frame(ShapeType.RECTANGLE, 250, 50, 150, 150, img2)

        print(f"Image collection size: {len(pres.images)}")
        print(f"Shapes on slide: {len(slide.shapes)}")

        pres.save(os.path.join(OUT, "multiple_images.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    add_picture_from_bytes()
    add_picture_from_file()
    multiple_images()
    print("\n=== test_picture_frame.py completed ===")
