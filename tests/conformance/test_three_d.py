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

The children of `<a:sp3d>` are a sequence too.  `CT_Shape3D` (§20.1.5.12) is
`bevelT, bevelB, extrusionClr, contourClr, extLst`, and each child is created
when the caller first touches the property that needs it.  Appending them made
the file's order the caller's order: setting the contour colour before the top
bevel wrote an `<a:sp3d>` PowerPoint reads as having no bevels and a white
extrusion.
"""

from __future__ import annotations

import itertools

import pytest

from aspose.slides_foss import BevelPresetType, CameraPresetType, LightRigPresetType
from aspose.slides_foss.drawing import Color

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


def _apply_3d(three_d, operation):
    if operation == "bevel_top":
        three_d.bevel_top.bevel_type = BevelPresetType.CIRCLE
    elif operation == "bevel_bottom":
        three_d.bevel_bottom.bevel_type = BevelPresetType.ANGLE
    elif operation == "extrusion_color":
        three_d.extrusion_height = 12.0
        three_d.extrusion_color.color = Color.from_argb(255, 0, 0, 255)
    elif operation == "contour_color":
        three_d.contour_width = 3.0
        three_d.contour_color.color = Color.from_argb(255, 255, 0, 0)
    else:  # pragma: no cover - guards a typo in the parametrisation
        raise AssertionError("unknown operation %r" % operation)


SHAPE_3D_OPERATIONS = ("bevel_top", "bevel_bottom", "extrusion_color", "contour_color")


@pytest.mark.parametrize(
    "order",
    list(itertools.permutations(SHAPE_3D_OPERATIONS)),
    ids=lambda o: "-".join(o),
)
def test_bevels_and_3d_colours_keep_their_schema_order_however_they_were_set(
    produced, shape_on_blank_slide, order
):
    """`<a:sp3d>` children follow `CT_Shape3D` for every order of the four setters."""
    pres, shape = shape_on_blank_slide()
    for operation in order:
        _apply_3d(shape.three_d_format, operation)
    pkg = produced(pres)

    sp3d = pkg.find_one(SLIDE, "//p:sp/p:spPr/a:sp3d")
    assert child_names(sp3d) == ["a:bevelT", "a:bevelB", "a:extrusionClr", "a:contourClr"], (
        "<a:sp3d> children are not the CT_Shape3D sequence "
        "bevelT, bevelB, extrusionClr, contourClr; found %r" % child_names(sp3d)
    )
    pkg.assert_element(SLIDE, "//p:sp/p:spPr/a:sp3d", child_order=True)
    pkg.assert_element(SLIDE, "//p:sp/p:spPr", child_order=True)
