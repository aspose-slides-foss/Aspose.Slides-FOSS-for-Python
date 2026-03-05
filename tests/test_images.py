"""Tests for ImageCollection and PictureFrame."""
import os

from aspose.slides_foss import Presentation, ShapeType

from conftest import create_test_png


def test_add_image():
    """Adding an image increases collection count."""
    with Presentation() as pres:
        pres.images.add_image(create_test_png(255, 0, 0))
        assert len(pres.images) >= 1


def test_multiple_images():
    """Multiple images can be added and iterated."""
    with Presentation() as pres:
        for r, g, b in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
            pres.images.add_image(create_test_png(r, g, b))
        assert len(pres.images) >= 3
        imgs = list(pres.images)
        assert len(imgs) >= 3


def test_picture_frame(tmp_pptx):
    """Picture frame with image persists after save/reload."""
    pres = Presentation()
    img = pres.images.add_image(create_test_png(0, 0, 255))
    pres.slides[0].shapes.add_picture_frame(ShapeType.RECTANGLE, 50, 50, 100, 100, img)
    assert len(pres.slides[0].shapes) >= 1

    pres2 = tmp_pptx(pres)
    assert len(pres2.slides[0].shapes) >= 1
    pres2.dispose()


def test_image_from_file(test_data_dir):
    """Load an image from the test_data directory."""
    img_path = os.path.join(test_data_dir, "lotus.png")
    if not os.path.exists(img_path):
        import pytest
        pytest.skip("lotus.png not in test_data")

    with Presentation() as pres:
        with open(img_path, "rb") as f:
            pp_img = pres.images.add_image(f.read())
        pres.slides[0].shapes.add_picture_frame(ShapeType.RECTANGLE, 50, 50, 200, 200, pp_img)
        assert len(pres.slides[0].shapes) >= 1
