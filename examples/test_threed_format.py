"""
ThreeDFormat — bevel, camera, light rig, material, depth, contour.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aspose.slides_foss import (
    Presentation, ShapeType,
    BevelPresetType, CameraPresetType, LightRigPresetType,
    LightingDirection, MaterialPresetType,
)
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.export import SaveFormat

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


def bevel_top_bottom():
    """Set top and bottom bevel on a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Beveled"

        tdf = shape.three_d_format

        # Top bevel
        bevel_top = tdf.bevel_top
        bevel_top.bevel_type = BevelPresetType.CIRCLE
        bevel_top.width = 10
        bevel_top.height = 5

        # Bottom bevel
        bevel_bottom = tdf.bevel_bottom
        bevel_bottom.bevel_type = BevelPresetType.ANGLE
        bevel_bottom.width = 8
        bevel_bottom.height = 4

        print(f"Top bevel: type={bevel_top.bevel_type}, w={bevel_top.width}, h={bevel_top.height}")
        print(f"Bottom bevel: type={bevel_bottom.bevel_type}, w={bevel_bottom.width}, h={bevel_bottom.height}")
        pres.save(os.path.join(OUT, "bevel.pptx"), SaveFormat.PPTX)


def camera_settings():
    """Configure the 3D camera on a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "3D Camera"

        tdf = shape.three_d_format
        camera = tdf.camera
        camera.camera_type = CameraPresetType.PERSPECTIVE_ABOVE

        print(f"Camera type: {camera.camera_type}")
        pres.save(os.path.join(OUT, "camera.pptx"), SaveFormat.PPTX)


def light_rig_settings():
    """Configure the light rig on a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Lit Shape"

        tdf = shape.three_d_format
        light = tdf.light_rig
        light.light_type = LightRigPresetType.BALANCED
        light.direction = LightingDirection.TOP

        print(f"Light type: {light.light_type}, direction: {light.direction}")
        pres.save(os.path.join(OUT, "light_rig.pptx"), SaveFormat.PPTX)


def material_preset():
    """Set the material type on a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Metal"

        tdf = shape.three_d_format
        tdf.material = MaterialPresetType.METAL

        print(f"Material: {tdf.material}")
        pres.save(os.path.join(OUT, "material.pptx"), SaveFormat.PPTX)


def depth_and_contour():
    """Set extrusion depth and contour on a shape."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 200, 100)
        shape.text_frame.text = "Extruded"

        tdf = shape.three_d_format

        # Depth (extrusion) — a float in points
        tdf.depth = 20
        tdf.extrusion_color.color = Color.dark_blue

        # Contour
        tdf.contour_width = 3
        tdf.contour_color.color = Color.gold

        print(f"Depth: {tdf.depth}")
        print(f"Contour width: {tdf.contour_width}")
        pres.save(os.path.join(OUT, "depth_contour.pptx"), SaveFormat.PPTX)


def full_3d_shape():
    """Combine bevel, camera, light, and material for a full 3D look."""
    with Presentation() as pres:
        slide = pres.slides[0]
        shape = slide.shapes.add_auto_shape(ShapeType.RECTANGLE, 100, 100, 250, 120)
        shape.text_frame.text = "Full 3D"

        tdf = shape.three_d_format

        # Bevel
        tdf.bevel_top.bevel_type = BevelPresetType.COOL_SLANT
        tdf.bevel_top.width = 12
        tdf.bevel_top.height = 6

        # Camera
        tdf.camera.camera_type = CameraPresetType.PERSPECTIVE_ABOVE

        # Light
        tdf.light_rig.light_type = LightRigPresetType.BALANCED
        tdf.light_rig.direction = LightingDirection.TOP

        # Material
        tdf.material = MaterialPresetType.PLASTIC

        # Depth
        tdf.depth = 15

        print("Full 3D effect applied")
        pres.save(os.path.join(OUT, "full_3d.pptx"), SaveFormat.PPTX)


if __name__ == "__main__":
    bevel_top_bottom()
    camera_settings()
    light_rig_settings()
    material_preset()
    depth_and_contour()
    full_3d_shape()
    print("\n=== test_threed_format.py completed ===")
