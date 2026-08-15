"""Behaviour that is already correct, asserted so a repair cannot quietly undo it.

These are not defect reports.  They pin down the parts of the package this
library already gets right — slide registration, relationship resolution,
content types, embedded media — and they exercise the harness itself against a
file that should pass every rule it has.
"""

from __future__ import annotations

import os

from aspose.slides_foss import Presentation, ShapeType

from .harness import REL_TYPE, qname

SLIDE = "ppt/slides/slide1.xml"


def test_a_plain_deck_satisfies_every_package_rule(produced):
    """Relationships resolve, targets exist, every part is content-typed."""
    pkg = produced(Presentation())

    pkg.assert_package_is_consistent()


def test_added_and_removed_slides_stay_registered(produced):
    """A slide is a slide in all four places, and removal cleans up all four."""
    pres = Presentation()
    pres.slides.add_empty_slide(pres.layout_slides[0])
    pres.slides.add_empty_slide(pres.layout_slides[0])
    pres.slides.remove_at(1)
    pkg = produced(pres)

    parts = pkg.parts_matching(r"^ppt/slides/slide\d+\.xml$")
    sld_ids = pkg.findall("ppt/presentation.xml", "//p:sldIdLst/p:sldId")
    slide_rels = [
        r for r in pkg.relationships("ppt/presentation.xml").values()
        if r["type"] == REL_TYPE["slide"]
    ]
    overrides = [
        n for n in pkg.content_types()[1]
        if n.startswith("/ppt/slides/slide")
    ]

    assert len(parts) == 2, parts
    assert len(sld_ids) == 2
    assert len(slide_rels) == 2
    assert len(overrides) == 2
    pkg.assert_package_is_consistent()


def test_an_embedded_image_resolves_from_the_slide(produced, test_data_dir):
    """`<a:blip r:embed>` must name a relationship that names a part that exists."""
    pres = Presentation()
    image = pres.images.add_image(open(os.path.join(test_data_dir, "lotus.png"), "rb").read())
    pres.slides[0].shapes.add_picture_frame(
        ShapeType.RECTANGLE, 50.0, 50.0, 200.0, 150.0, image
    )
    pkg = produced(pres)

    blip = pkg.find_one(SLIDE, "//a:blip")
    rel_id = blip.get(qname("r:embed"))
    assert rel_id, dict(blip.attrib)
    assert pkg.relationship(SLIDE, rel_id)["type"] == REL_TYPE["image"]
    pkg.assert_package_is_consistent()


def test_a_produced_file_opens_in_an_independent_reader(
    produced, shape_on_blank_slide, python_pptx
):
    """A third-party reader must see the shape and its text.

    python-pptx is deliberately not the library under test: when it and the
    library disagree about what is in the file, the file decides.
    """
    pres, shape = shape_on_blank_slide(with_text="Independent read-back")
    pkg = produced(pres)

    deck = pkg.open_with_python_pptx()
    texts = [
        s.text_frame.text
        for s in deck.slides[0].shapes
        if s.has_text_frame and s.text_frame.text
    ]
    assert "Independent read-back" in texts, texts
