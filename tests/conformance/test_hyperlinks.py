"""Setting a hyperlink must either work or say it does not.

`portion_format.hyperlink_click = "https://example.com"` returns successfully,
saves successfully, and writes nothing at all.  The README lists hyperlinks
under *Limitations* and promises `NotImplementedError`; what happens instead is
silence, which is the dangerous direction of wrong — the call looks like it
worked and the link is simply absent from the file.

The mechanism is general and worth naming: no formatting class defines
`__slots__`, so *any* assignment to a property that does not exist is accepted
and discarded.  A typo in a property name behaves exactly like a working call.
"""

from __future__ import annotations

import pytest

from .harness import REL_TYPE, qname

SLIDE = "ppt/slides/slide1.xml"
URL = "https://example.com/report"


def test_setting_a_hyperlink_is_not_silently_discarded(produced, shape_on_blank_slide):
    """A hyperlink must reach the package, or the caller must be told it cannot."""
    pres, shape = shape_on_blank_slide(with_text="Click me")
    portion_format = shape.text_frame.paragraphs[0].portions[0].portion_format

    raised = None
    try:
        portion_format.hyperlink_click = URL
    except Exception as exc:  # noqa: BLE001 - the type is asserted below
        raised = exc

    pkg = produced(pres)
    links = pkg.findall(SLIDE, "//a:hlinkClick")

    assert raised is not None or links, (
        "assigning a hyperlink was accepted and nothing was written: the saved "
        "slide contains no <a:hlinkClick>, so the link is lost with no error"
    )

    if raised is not None:
        assert isinstance(raised, (NotImplementedError, AttributeError)), (
            "refusing is fine, but the exception must say so; got %r" % (raised,)
        )
        return

    element = links[0]
    rel_id = element.get(qname("r:id"))
    assert rel_id, "<a:hlinkClick> carries no r:id: %r" % dict(element.attrib)

    relationship = pkg.relationship(SLIDE, rel_id)
    assert relationship["type"] == REL_TYPE["hyperlink"]
    assert relationship["mode"] == "External"
    assert relationship["target"] == URL


def test_a_shape_level_hyperlink_reaches_the_package(produced, shape_on_blank_slide):
    """A link on the whole shape lives in `p:cNvPr`, not in the run properties.

    `CT_NonVisualDrawingProps` (ECMA-376 §20.1.2.2.8) is `hlinkClick?`,
    `hlinkHover?`, `extLst?` — and the mouse-over element is named
    `a:hlinkHover` there, not `a:hlinkMouseOver` as it is on a text run. The
    two names are easy to write interchangeably and only one of them is the
    element PowerPoint reads.
    """
    pres, shape = shape_on_blank_slide()
    shape.hyperlink_click = URL
    shape.hyperlink_mouse_over = URL + "/over"
    pkg = produced(pres)

    for tag, expected in (("a:hlinkClick", URL), ("a:hlinkHover", URL + "/over")):
        element = pkg.find_one(SLIDE, "//p:sp/p:nvSpPr/p:cNvPr/" + tag)
        rel_id = element.get(qname("r:id"))
        assert rel_id, "<%s> carries no r:id: %r" % (tag, dict(element.attrib))
        relationship = pkg.relationship(SLIDE, rel_id)
        assert relationship["type"] == REL_TYPE["hyperlink"]
        assert relationship["mode"] == "External"
        assert relationship["target"] == expected

    assert not pkg.findall(SLIDE, "//p:cNvPr/a:hlinkMouseOver"), (
        "a:hlinkMouseOver is the run-properties name; CT_NonVisualDrawingProps "
        "has no such child and PowerPoint ignores it"
    )
    pkg.assert_element(
        SLIDE,
        "//p:sp/p:nvSpPr/p:cNvPr",
        child_order=[["a:hlinkClick"], ["a:hlinkHover"], ["a:extLst"]],
    )
    pkg.assert_package_is_consistent()


def test_clearing_a_shape_hyperlink_removes_its_relationship(produced, shape_on_blank_slide):
    """Setting the link back to None must take the .rels entry with it."""
    pres, shape = shape_on_blank_slide()
    shape.hyperlink_click = URL
    shape.hyperlink_click = None
    pkg = produced(pres)

    assert not pkg.findall(SLIDE, "//p:cNvPr/a:hlinkClick"), (
        "the hyperlink element survived being cleared"
    )
    external = [
        rel for rel in pkg.relationships(SLIDE).values()
        if rel["type"] == REL_TYPE["hyperlink"]
    ]
    assert not external, (
        "the element is gone but its external relationship is still declared: "
        "%r" % external
    )
    pkg.assert_package_is_consistent()


def test_an_unknown_formatting_property_is_rejected(shape_on_blank_slide):
    """A misspelt or unimplemented property must raise, not vanish.

    Without this, every unimplemented feature in the library fails the same
    silent way, and a user's typo is indistinguishable from a working call.
    """
    pres, shape = shape_on_blank_slide(with_text="Click me")
    try:
        portion_format = shape.text_frame.paragraphs[0].portions[0].portion_format
        with pytest.raises(AttributeError):
            portion_format.definitely_not_a_formatting_property = 1
    finally:
        pres.dispose()
