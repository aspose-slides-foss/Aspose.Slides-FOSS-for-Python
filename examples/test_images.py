"""
ImageCollection — add images from bytes and file, iterate, access by index.
"""
import os
import sys
import struct
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import Presentation, ShapeType
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def _create_png(r, g, b):
    """Create a minimal 1x1 PNG with the given RGB color."""
    def _chunk(ct, data):
        c = ct + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw = bytes([0, r, g, b])  # filter=none + RGB
    idat = zlib.compress(raw)
    return header + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")


def add_image_from_bytes():
    """Add an image to the collection from raw bytes."""
    with Presentation() as pres:
        image_data = _create_png(255, 0, 0)
        pp_image = pres.images.add_image(image_data)

        print(f"Image added, collection count: {len(pres.images)}")
        print(f"Image type: {type(pp_image).__name__}")

        pres.save(os.path.join(OUT, "image_from_bytes.pptx"), SaveFormat.PPTX)


def add_image_from_file():
    """Add an image from a file on disk."""
    # Write a test PNG
    img_path = os.path.join(OUT, "blue.png")
    with open(img_path, "wb") as f:
        f.write(_create_png(0, 0, 255))

    with Presentation() as pres:
        with open(img_path, "rb") as f:
            pp_image = pres.images.add_image(f.read())

        print(f"Image from file added, count: {len(pres.images)}")

        # Use it in a picture frame
        slide = pres.slides[0]
        slide.shapes.add_picture_frame(ShapeType.RECTANGLE, 50, 50, 100, 100, pp_image)

        pres.save(os.path.join(OUT, "image_from_file.pptx"), SaveFormat.PPTX)


def multiple_images():
    """Add multiple images and iterate over the collection."""
    with Presentation() as pres:
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for r, g, b in colors:
            pres.images.add_image(_create_png(r, g, b))

        print(f"Total images: {len(pres.images)}")

        # Iterate
        for i, img in enumerate(pres.images):
            print(f"  Image {i}: {type(img).__name__}")

        # Access by index
        first_img = pres.images[0]
        print(f"First image: {type(first_img).__name__}")

        pres.save(os.path.join(OUT, "multiple_images_coll.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    add_image_from_bytes()
    add_image_from_file()
    multiple_images()
    print("\n=== test_images.py completed ===")
