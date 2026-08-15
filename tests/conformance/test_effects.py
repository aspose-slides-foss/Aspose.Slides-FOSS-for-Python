"""A one-line `enable_*_effect()` must produce an effect PowerPoint can open.

Each enabler inserts its element into `<a:effectLst>` in the right place and
then stops: `<a:outerShdw/>` carries no colour, `<a:softEdge/>` no radius,
`<a:prstShdw/>` no preset.  ECMA-376 §20.1.8 makes those children and
attributes mandatory, and PowerPoint refuses the whole file rather than
ignoring the incomplete element.

Setting the missing value afterwards through the public API repairs every one
of them, so what is missing is the default, not the feature.
"""

from __future__ import annotations

import pytest

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"

#: tag -> (required attributes, one-of required children)
#: ECMA-376 Part 1, §20.1.8.  `blur` and `reflection` are complete when empty
#: and are deliberately absent from this table.
REQUIRED = {
    "outer_shadow": ("a:outerShdw", (), ("a:srgbClr", "a:schemeClr", "a:prstClr",
                                        "a:hslClr", "a:sysClr", "a:scrgbClr")),
    "inner_shadow": ("a:innerShdw", (), ("a:srgbClr", "a:schemeClr", "a:prstClr",
                                         "a:hslClr", "a:sysClr", "a:scrgbClr")),
    "glow": ("a:glow", (), ("a:srgbClr", "a:schemeClr", "a:prstClr",
                            "a:hslClr", "a:sysClr", "a:scrgbClr")),
    "preset_shadow": ("a:prstShdw", ("prst",), ("a:srgbClr", "a:schemeClr", "a:prstClr",
                                                "a:hslClr", "a:sysClr", "a:scrgbClr")),
    "soft_edge": ("a:softEdge", ("rad",), ()),
    "fill_overlay": ("a:fillOverlay", ("blend",), ("a:noFill", "a:solidFill", "a:gradFill",
                                                   "a:blipFill", "a:pattFill", "a:grpFill")),
}


@pytest.mark.parametrize("effect", sorted(REQUIRED))
def test_enabling_an_effect_writes_an_element_powerpoint_can_open(
    produced, shape_on_blank_slide, effect
):
    """The enabled effect must carry the attributes and children its type requires."""
    tag, required_attrs, one_of_children = REQUIRED[effect]

    pres, shape = shape_on_blank_slide()
    getattr(shape.effect_format, "enable_%s_effect" % effect)()
    pkg = produced(pres)

    element = pkg.find_one(SLIDE, "//a:effectLst/%s" % tag)

    for attribute in required_attrs:
        assert element.get(attribute) is not None, (
            "<%s> was written without its required @%s; ECMA-376 makes it "
            "mandatory and PowerPoint refuses the file. attributes: %r"
            % (tag, attribute, dict(element.attrib))
        )

    if one_of_children:
        present = child_names(element)
        assert any(name in present for name in one_of_children), (
            "<%s> was written with no %s child; ECMA-376 requires one and "
            "PowerPoint refuses the file. children: %r"
            % (tag, " / ".join(one_of_children), present)
        )


@pytest.mark.parametrize("effect", sorted(REQUIRED))
def test_an_enabled_effect_does_not_disturb_the_effect_sequence(
    produced, shape_on_blank_slide, effect
):
    """`<a:effectLst>` children stay in their ECMA-376 sequence."""
    pres, shape = shape_on_blank_slide()
    shape.effect_format.set_blur_effect(4.0, False)
    getattr(shape.effect_format, "enable_%s_effect" % effect)()
    getattr(shape.effect_format, "enable_soft_edge_effect")()
    pkg = produced(pres)

    pkg.assert_element(SLIDE, "//a:effectLst", child_order=True)


def test_an_enabled_effect_leaves_the_package_consistent(produced, shape_on_blank_slide):
    """Enabling every effect must not break relationships or content types."""
    pres, shape = shape_on_blank_slide()
    for effect in sorted(REQUIRED):
        getattr(shape.effect_format, "enable_%s_effect" % effect)()
    pkg = produced(pres)

    pkg.assert_package_is_consistent()
