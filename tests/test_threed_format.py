"""Tests for ThreeDFormat: bevel, camera, light rig, depth."""
from aspose.slides_foss import (
    Presentation, ShapeType,
    BevelPresetType, CameraPresetType, LightRigPresetType,
    LightingDirection, MaterialPresetType,
)
from aspose.slides_foss.drawing import Color


def _clear(pres):
    pres.slides[0].shapes.clear()
    return pres.slides[0]


def test_bevel_top(tmp_pptx):
    """Bevel top type/width/height persist."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    tdf = shape.three_d_format
    tdf.bevel_top.bevel_type = BevelPresetType.CIRCLE
    tdf.bevel_top.width = 10
    tdf.bevel_top.height = 5

    pres2 = tmp_pptx(pres)
    bt = pres2.slides[0].shapes[0].three_d_format.bevel_top
    assert bt.bevel_type == BevelPresetType.CIRCLE
    assert bt.width == 10
    assert bt.height == 5
    pres2.dispose()


def test_camera(tmp_pptx):
    """Camera preset persists."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    shape.three_d_format.camera.camera_type = CameraPresetType.PERSPECTIVE_ABOVE

    pres2 = tmp_pptx(pres)
    cam = pres2.slides[0].shapes[0].three_d_format.camera
    assert cam.camera_type == CameraPresetType.PERSPECTIVE_ABOVE
    pres2.dispose()


def test_light_rig(tmp_pptx):
    """Light rig preset and direction persist."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    lr = shape.three_d_format.light_rig
    lr.light_type = LightRigPresetType.BALANCED
    lr.direction = LightingDirection.TOP

    pres2 = tmp_pptx(pres)
    lr2 = pres2.slides[0].shapes[0].three_d_format.light_rig
    assert lr2.light_type == LightRigPresetType.BALANCED
    assert lr2.direction == LightingDirection.TOP
    pres2.dispose()


def test_depth_and_material(tmp_pptx):
    """Extrusion depth and material persist."""
    pres = Presentation()
    slide = _clear(pres)
    shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
    tdf = shape.three_d_format
    tdf.depth = 20
    tdf.material = MaterialPresetType.METAL

    pres2 = tmp_pptx(pres)
    tdf2 = pres2.slides[0].shapes[0].three_d_format
    assert tdf2.depth == 20
    assert tdf2.material == MaterialPresetType.METAL
    pres2.dispose()
