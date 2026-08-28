"""A group shape's properties element has its own, shorter, schema.

`p:grpSpPr` is `CT_GroupShapeProperties`, not `CT_ShapeProperties`
(ECMA-376 §19.3.1.23), and the difference is not cosmetic:

    xfrm?, <fill>?, effectLst|effectDag?, scene3d?, extLst?

There is no `a:ln` and no `a:sp3d` in it at all.  A group is a container; it
has no outline of its own and no extrusion of its own, and the Open XML SDK
rejects both elements outright rather than merely objecting to their position.

So two things have to hold.  Whatever *is* allowed there must come out in
sequence however the caller ordered the assignments — the same order-dependent
correctness the shape properties table exists to remove, one container over.
And the two properties the type does not have must not be written: an outline
or a depth set on a group used to produce a package PowerPoint and the SDK
both refuse, from a call that reported success.
"""

from __future__ import annotations

import itertools

import pytest

from aspose.slides_foss import FillType

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"
GRP_SP_PR = "//p:grpSp/p:grpSpPr"


def _apply(group, operation):
    if operation == "fill":
        group.fill_format.fill_type = FillType.SOLID
    elif operation == "effect":
        group.effect_format.enable_outer_shadow_effect()
    else:  # pragma: no cover - guards a typo in the parametrisation
        raise AssertionError("unknown operation %r" % operation)


OPERATIONS = ("fill", "effect")
PERMUTATIONS = list(itertools.permutations(OPERATIONS))


@pytest.mark.parametrize("order", PERMUTATIONS, ids=lambda o: "-".join(o))
def test_group_properties_keep_their_schema_order_however_they_were_set(
    produced, blank_presentation, order
):
    """`<p:grpSpPr>` children follow `CT_GroupShapeProperties` for every permutation."""
    pres = blank_presentation
    group = pres.slides[0].shapes.add_group_shape()
    for operation in order:
        _apply(group, operation)
    pkg = produced(pres)

    grp_sp_pr = pkg.find_one(SLIDE, GRP_SP_PR)
    assert set(child_names(grp_sp_pr)) >= {"a:solidFill", "a:effectLst"}, (
        "the formatting children were not all written: %r" % child_names(grp_sp_pr)
    )
    pkg.assert_element(SLIDE, GRP_SP_PR, child_order=True)


def test_a_fill_set_after_a_scene_still_precedes_it(produced, blank_presentation):
    """A fill added to a group that already has a scene must go in before it.

    A loaded deck can arrive with `<a:scene3d>` already in place; appending the
    fill after it is the inversion the sequence forbids.
    """
    import lxml.etree as ET

    pres = blank_presentation
    group = pres.slides[0].shapes.add_group_shape()
    grp_sp_pr = group._get_sp_pr()
    ET.SubElement(grp_sp_pr, "{http://schemas.openxmlformats.org/drawingml/2006/main}scene3d")
    group.fill_format.fill_type = FillType.SOLID
    pkg = produced(pres)

    pkg.assert_element(SLIDE, GRP_SP_PR, child_order=True)


def test_a_group_shape_has_no_outline_to_set(produced, blank_presentation):
    """`CT_GroupShapeProperties` has no `a:ln`, so none may be written."""
    pres = blank_presentation
    group = pres.slides[0].shapes.add_group_shape()

    assert group.line_format is None, (
        "line_format on a group shape returned %r; there is nowhere valid to "
        "put the result, so the documented None is the only honest answer"
        % (group.line_format,)
    )

    pkg = produced(pres)
    assert not pkg.findall(SLIDE, GRP_SP_PR + "/a:ln"), (
        "<a:ln> was written inside <p:grpSpPr>, which the schema does not "
        "allow: %r" % child_names(pkg.find_one(SLIDE, GRP_SP_PR))
    )


def test_a_group_shape_has_no_extrusion_to_set(produced, blank_presentation):
    """`CT_GroupShapeProperties` has no `a:sp3d`, so none may be written."""
    pres = blank_presentation
    group = pres.slides[0].shapes.add_group_shape()

    assert group.three_d_format is None, (
        "three_d_format on a group shape returned %r; a:sp3d is not a child "
        "the type has" % (group.three_d_format,)
    )

    pkg = produced(pres)
    assert not pkg.findall(SLIDE, GRP_SP_PR + "/a:sp3d"), (
        "<a:sp3d> was written inside <p:grpSpPr>, which the schema does not "
        "allow: %r" % child_names(pkg.find_one(SLIDE, GRP_SP_PR))
    )


def test_a_child_of_a_group_still_has_both(produced, blank_presentation):
    """The restriction is the group's own properties, not the shapes inside it."""
    from aspose.slides_foss import ShapeType

    pres = blank_presentation
    group = pres.slides[0].shapes.add_group_shape()
    child = group.shapes.add_auto_shape(ShapeType.RECTANGLE, 10.0, 10.0, 100.0, 50.0)
    child.line_format.width = 3.0
    child.three_d_format.depth = 6.0
    pkg = produced(pres)

    sp_pr = pkg.find_one(SLIDE, "//p:grpSp/p:sp/p:spPr")
    present = child_names(sp_pr)
    assert "a:ln" in present and "a:sp3d" in present, (
        "a shape inside a group lost its outline or its extrusion: %r" % present
    )
    pkg.assert_element(SLIDE, "//p:grpSp/p:sp/p:spPr", child_order=True)
