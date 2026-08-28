"""A slide transition must be written where `CT_Slide` puts it.

`<p:transition>` is inserted directly after `<p:cSld>`, which lands it *before*
`<p:clrMapOvr>`.  `CT_Slide` (ECMA-376 §19.3.1.38) is the sequence
`cSld, clrMapOvr?, transition?, timing?, extLst?`, so every file with a
transition is schema-invalid — all transition types, not a subset.

PowerPoint tolerates the inversion, which is why it survived: nothing that reads
the file complains, and the library's own reader finds the element wherever it
put it.
"""

from __future__ import annotations

import pytest

from aspose.slides_foss import Presentation
from aspose.slides_foss.slideshow import TransitionType

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"

# A spread across the transition families rather than all 57: the insertion
# point is shared, so one case per family is enough to show it is not
# type-specific.
SAMPLE_TRANSITIONS = [
    TransitionType.FADE,
    TransitionType.PUSH,
    TransitionType.WIPE,
    TransitionType.SPLIT,
    TransitionType.CIRCLE,
    TransitionType.RANDOM,
]


@pytest.mark.parametrize("transition", SAMPLE_TRANSITIONS, ids=lambda t: t.name)
def test_a_transition_is_written_after_the_colour_map_override(produced, transition):
    """`<p:transition>` must follow `<p:clrMapOvr>`, not precede it."""
    pres = Presentation()
    pres.slides[0].slide_show_transition.type = transition
    pkg = produced(pres)

    root = pkg.xml(SLIDE)
    order = child_names(root)
    assert "p:transition" in order, "no <p:transition> was written: %r" % order

    pkg.assert_element(SLIDE, "/p:sld", child_order=True)


def test_a_transition_leaves_the_package_consistent(produced):
    """Adding a transition must not break relationships or content types."""
    pres = Presentation()
    pres.slides[0].slide_show_transition.type = TransitionType.FADE
    pkg = produced(pres)

    pkg.assert_package_is_consistent()
