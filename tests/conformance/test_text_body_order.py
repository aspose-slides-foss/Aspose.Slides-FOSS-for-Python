"""Text frame formatting must be valid whatever order the caller set it in.

`<a:bodyPr>` gets a child for the autofit mode, one for a text warp, and a
scene and extrusion for 3-D text, each created when the caller first sets the
property.  `CT_TextBodyProperties` (ECMA-376 §21.1.2.1.1) is the sequence

    prstTxWarp, noAutofit|normAutofit|spAutoFit, scene3d, sp3d|flatTx, extLst

so appending them made the file's order the caller's order.  Setting the
autofit before the warp wrote the warp after the autofit, and PowerPoint then
kept the autofit and showed the text unwarped.
"""

from __future__ import annotations

import itertools

import pytest

from aspose.slides_foss import TextAutofitType, TextShapeType

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"
BODY_PR = "//p:sp/p:txBody/a:bodyPr"


def _apply(text_frame_format, operation):
    if operation == "autofit":
        text_frame_format.autofit_type = TextAutofitType.NORMAL
    elif operation == "warp":
        text_frame_format.transform = TextShapeType.ARCH_UP
    elif operation == "keep_text_flat":
        text_frame_format.keep_text_flat = True
    elif operation == "text_3d":
        text_frame_format.three_d_format.depth = 3.0
    else:  # pragma: no cover - guards a typo in the parametrisation
        raise AssertionError("unknown operation %r" % operation)


OPERATIONS = ("autofit", "warp", "keep_text_flat", "text_3d")


@pytest.mark.parametrize(
    "order", list(itertools.permutations(OPERATIONS)), ids=lambda o: "-".join(o)
)
def test_text_body_properties_keep_their_schema_order_however_they_were_set(
    produced, shape_on_blank_slide, order
):
    """`<a:bodyPr>` children follow `CT_TextBodyProperties` for every permutation."""
    pres, shape = shape_on_blank_slide(with_text="Warped")
    text_frame_format = shape.text_frame.text_frame_format
    for operation in order:
        _apply(text_frame_format, operation)
    pkg = produced(pres)

    body_pr = pkg.find_one(SLIDE, BODY_PR)
    assert child_names(body_pr) == ["a:prstTxWarp", "a:normAutofit", "a:scene3d", "a:sp3d"], (
        "<a:bodyPr> children are not the CT_TextBodyProperties sequence "
        "prstTxWarp, normAutofit, scene3d, sp3d; found %r" % child_names(body_pr)
    )
    pkg.assert_element(SLIDE, BODY_PR, child_order=True)


@pytest.mark.parametrize("autofit", [TextAutofitType.NONE, TextAutofitType.SHAPE])
def test_every_autofit_mode_goes_after_the_warp(produced, shape_on_blank_slide, autofit):
    """The other two autofit elements take the same position as `normAutofit`."""
    pres, shape = shape_on_blank_slide(with_text="Warped")
    text_frame_format = shape.text_frame.text_frame_format
    text_frame_format.autofit_type = autofit
    text_frame_format.transform = TextShapeType.ARCH_UP
    pkg = produced(pres)

    pkg.assert_element(SLIDE, BODY_PR, children=("a:prstTxWarp",), child_order=True)
