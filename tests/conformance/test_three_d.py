"""A shape given 3-D properties must actually render in 3-D.

`three_d_format.depth`, `.extrusion_height` and `.contour_width` write
`<a:sp3d>` and stop there.  Without a sibling `<a:scene3d>` there is no camera
and no lighting, so PowerPoint has nothing to render the extrusion with and
reports the shape as flat.

The related failure is `<a:scene3d>` written half-populated: `CT_Scene3D`
(ECMA-376 §20.1.4.1.26) is a sequence of a *required* `<a:camera>` and a
*required* `<a:lightRig>`, and touching only the camera leaves the light rig
out, which makes the element schema-invalid.  `CT_LightRig` in turn requires
both `@rig` and `@dir`.
"""

from __future__ import annotations

from aspose.slides_foss import CameraPresetType, LightRigPresetType

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"


def test_a_shape_with_depth_gets_the_scene_that_makes_it_render(
    produced, shape_on_blank_slide
):
    """Extrusion without a scene is invisible; `<a:scene3d>` must be written too."""
    pres, shape = shape_on_blank_slide()
    shape.three_d_format.depth = 6.0
    shape.three_d_format.extrusion_height = 8.0
    shape.three_d_format.contour_width = 2.0
    pkg = produced(pres)

    sp_pr = pkg.find_one(SLIDE, "//p:sp/p:spPr")
    present = child_names(sp_pr)
    assert "a:sp3d" in present, "no <a:sp3d> was written at all: %r" % present
    assert "a:scene3d" in present, (
        "<a:sp3d> was written with no <a:scene3d> sibling, so the shape has no "
        "camera and no lighting and PowerPoint renders it flat. "
        "children of <p:spPr>: %r" % present
    )

    pkg.assert_element(
        SLIDE,
        "//a:scene3d",
        children=("a:camera", "a:lightRig"),
        child_order=True,
    )
    pkg.assert_element(SLIDE, "//a:scene3d/a:camera", attrs={"prst": ...})
    pkg.assert_element(SLIDE, "//a:scene3d/a:lightRig", attrs={"rig": ..., "dir": ...})
    pkg.assert_element(SLIDE, "//p:sp/p:spPr", child_order=True)


def test_a_scene_is_never_written_half_populated(produced, shape_on_blank_slide):
    """Setting only the camera must still produce a complete `<a:scene3d>`."""
    pres, shape = shape_on_blank_slide()
    shape.three_d_format.camera.camera_type = CameraPresetType.ORTHOGRAPHIC_FRONT
    pkg = produced(pres)

    scene = pkg.find_one(SLIDE, "//a:scene3d")
    present = child_names(scene)
    assert "a:lightRig" in present, (
        "<a:scene3d> requires both <a:camera> and <a:lightRig>; only %r was "
        "written, which no strict consumer will accept" % present
    )


def test_a_light_rig_carries_its_required_direction(produced, shape_on_blank_slide):
    """`CT_LightRig` requires `@dir` as well as `@rig`."""
    pres, shape = shape_on_blank_slide()
    shape.three_d_format.light_rig.light_type = LightRigPresetType.THREE_PT
    pkg = produced(pres)

    pkg.assert_element(SLIDE, "//a:lightRig", attrs={"rig": ..., "dir": ...})
