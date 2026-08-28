"""Character formatting must be valid whatever order the caller set it in.

Every lazily created child of `<a:rPr>` is appended, so the element's child
order is the order the caller happened to make the assignments in.
`CT_TextCharacterProperties` (ECMA-376 §21.1.2.3.9) is a sequence:

    ln, <fill>, effectLst|effectDag, highlight, uLnTx|uLn, uFillTx|uFill,
    latin, ea, cs, sym, hlinkClick, hlinkMouseOver, rtl, extLst

so setting the font before the highlight produces a valid file and setting the
highlight before the font produces an invalid one, from the same formatting.

Order-dependent correctness is worse than consistent breakage: the same code
path works for one user and fails for another, and the bug will not reproduce
for whoever reports it.
"""

from __future__ import annotations

import itertools

import pytest

from aspose.slides_foss import FontData
from aspose.slides_foss.drawing import Color

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"


def _apply(portion_format, operation):
    if operation == "latin_font":
        portion_format.latin_font = FontData("Arial")
    elif operation == "highlight":
        portion_format.highlight_color.color = Color.from_argb(255, 255, 255, 0)
    elif operation == "fill":
        portion_format.fill_format.solid_fill_color.color = Color.from_argb(255, 0, 70, 127)
    else:  # pragma: no cover - guards a typo in the parametrisation
        raise AssertionError("unknown operation %r" % operation)


OPERATIONS = ("latin_font", "highlight", "fill")
PERMUTATIONS = list(itertools.permutations(OPERATIONS))


@pytest.mark.parametrize("order", PERMUTATIONS, ids=lambda o: "-".join(o))
def test_run_properties_keep_their_schema_order_however_they_were_set(
    produced, shape_on_blank_slide, order
):
    """`<a:rPr>` children follow `CT_TextCharacterProperties` for every permutation."""
    pres, shape = shape_on_blank_slide(with_text="Formatted")
    portion_format = shape.text_frame.paragraphs[0].portions[0].portion_format
    for operation in order:
        _apply(portion_format, operation)
    pkg = produced(pres)

    rpr = pkg.find_one(SLIDE, "//a:r/a:rPr")
    assert set(child_names(rpr)) >= {"a:latin", "a:highlight", "a:solidFill"}, (
        "the three formatting children were not all written: %r" % child_names(rpr)
    )
    pkg.assert_element(SLIDE, "//a:r/a:rPr", child_order=True)


def test_run_properties_come_before_the_run_text(produced, shape_on_blank_slide):
    """`CT_RegularTextRun` is `rPr?` then `t`; formatting after the text is discarded."""
    pres, shape = shape_on_blank_slide(with_text="Formatted")
    shape.text_frame.paragraphs[0].portions[0].portion_format.font_height = 24.0
    pkg = produced(pres)

    pkg.assert_element(SLIDE, "//a:p/a:r", child_order=True)
