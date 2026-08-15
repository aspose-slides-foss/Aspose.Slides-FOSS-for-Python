"""Tables and charts must use the OOXML lock element, not an invented one.

`<p:cNvGraphicFramePr>` accepts exactly one child, `<a:graphicFrameLocks>`.  The
name written here is `<a:graphicFrameLocking>` — the *type* is
`CT_GraphicalObjectFrameLocking`, which is presumably where it came from, but
the element name is not in the schema.

PowerPoint tolerates it and silently drops the element, so every table and every
chart this library writes is schema-invalid without anything visible saying so.
That silence is exactly why it survived: only a validator, or an assertion on
the package, can see it.
"""

from __future__ import annotations

from aspose.slides_foss import Presentation
from aspose.slides_foss.charts import ChartType

from .harness import child_names

SLIDE = "ppt/slides/slide1.xml"
INVENTED = "a:graphicFrameLocking"
CORRECT = "a:graphicFrameLocks"


def _lock_children(pkg):
    element = pkg.find_one(SLIDE, "//p:graphicFrame/p:nvGraphicFramePr/p:cNvGraphicFramePr")
    return child_names(element)


def test_a_table_uses_the_schema_name_for_its_frame_locks(produced):
    """A table's frame locks must be `<a:graphicFrameLocks>`."""
    pres = Presentation()
    pres.slides[0].shapes.add_table(50.0, 50.0, [100.0, 100.0], [40.0, 40.0])
    pkg = produced(pres)

    children = _lock_children(pkg)
    assert INVENTED not in children, (
        "<%s> is not an OOXML element; PowerPoint discards it silently. "
        "children of <p:cNvGraphicFramePr>: %r" % (INVENTED, children)
    )
    assert CORRECT in children, (
        "expected <%s>, found %r" % (CORRECT, children)
    )
    pkg.assert_element(SLIDE, "//a:graphicFrameLocks", attrs={"noGrp": "1"})


def test_a_chart_uses_the_schema_name_for_its_frame_locks(produced):
    """A chart's frame locks must be `<a:graphicFrameLocks>`."""
    pres = Presentation()
    pres.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 50.0, 50.0, 300.0, 200.0)
    pkg = produced(pres)

    children = _lock_children(pkg)
    assert INVENTED not in children, (
        "<%s> is not an OOXML element; PowerPoint discards it silently. "
        "children of <p:cNvGraphicFramePr>: %r" % (INVENTED, children)
    )
    assert CORRECT in children, (
        "expected <%s>, found %r" % (CORRECT, children)
    )
    pkg.assert_element(SLIDE, "//a:graphicFrameLocks", attrs={"noGrp": "1"})


def test_a_table_leaves_the_package_consistent(produced):
    """Relationships and content types stay resolvable when a table is added."""
    pres = Presentation()
    pres.slides[0].shapes.add_table(50.0, 50.0, [100.0, 100.0], [40.0, 40.0])
    pkg = produced(pres)

    pkg.assert_package_is_consistent()
