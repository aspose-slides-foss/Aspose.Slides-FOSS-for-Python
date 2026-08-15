"""What a produced file says about itself must be true.

Three separate small defects, one decision:

* the bundled template carries `lang="ru-RU"` on 84 runs and every produced file
  inherits them, so a deck written by an English-speaking user is marked as
  Russian text throughout;
* `docProps/app.xml` is copied from the template and never regenerated, so a
  three-slide deck reports `<Slides>1</Slides>`;
* the template's placeholder `docProps/thumbnail.jpeg` ships in every output,
  showing a preview of a document that does not exist.

None of these stops a file opening.  All of them are the file lying about
itself, which is the kind of defect nobody finds until it is embarrassing.
"""

from __future__ import annotations

import os
import re
import zipfile

from aspose.slides_foss import Presentation

TEMPLATE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "aspose", "slides_foss", "_internal", "pptx", "Template.pptx",
)


def _lang_counts(zip_file) -> dict:
    counts = {}
    for name in zip_file.namelist():
        if not name.endswith(".xml"):
            continue
        text = zip_file.read(name).decode("utf-8", errors="replace")
        for value in re.findall(r'lang="([^"]+)"', text):
            counts[value] = counts.get(value, 0) + 1
    return counts


def test_the_bundled_template_carries_no_foreign_editing_language():
    """The template must not stamp a language the user did not choose."""
    with zipfile.ZipFile(TEMPLATE) as template:
        counts = _lang_counts(template)

    assert "ru-RU" not in counts, (
        "the bundled template marks %d runs as ru-RU; every produced file "
        "inherits them. languages in the template: %r" % (counts.get("ru-RU"), counts)
    )


def test_a_produced_file_carries_no_foreign_editing_language(produced):
    """Nothing the user writes should come out marked in another language."""
    pres = Presentation()
    pkg = produced(pres)

    with zipfile.ZipFile(pkg.path) as written:
        counts = _lang_counts(written)

    assert "ru-RU" not in counts, (
        "the saved file marks %d runs as ru-RU; languages present: %r"
        % (counts.get("ru-RU"), counts)
    )


def test_the_document_summary_reports_the_real_slide_count(produced):
    """`docProps/app.xml` must be regenerated on save, not copied."""
    pres = Presentation()
    pres.slides.add_empty_slide(pres.layout_slides[0])
    pres.slides.add_empty_slide(pres.layout_slides[0])
    expected = len(pres.slides)
    pkg = produced(pres)

    declared = int(pkg.find_one("docProps/app.xml", "//*[local-name()='Slides']").text)
    in_package = len(pkg.findall("ppt/presentation.xml", "//p:sldIdLst/p:sldId"))

    assert in_package == expected, (
        "the package itself has %d slides, expected %d" % (in_package, expected)
    )
    assert declared == expected, (
        "docProps/app.xml reports <Slides>%d</Slides> for a %d-slide deck"
        % (declared, expected)
    )


def test_the_document_summary_follows_a_removal(produced):
    """Removing a slide must be reflected in the summary too."""
    pres = Presentation()
    pres.slides.add_empty_slide(pres.layout_slides[0])
    pres.slides.add_empty_slide(pres.layout_slides[0])
    pres.slides.remove_at(1)
    expected = len(pres.slides)
    pkg = produced(pres)

    declared = int(pkg.find_one("docProps/app.xml", "//*[local-name()='Slides']").text)
    assert declared == expected, (
        "docProps/app.xml reports <Slides>%d</Slides> for a %d-slide deck"
        % (declared, expected)
    )


def test_a_produced_file_carries_no_placeholder_thumbnail(produced):
    """Shipping the template's preview as the document's own is a false claim."""
    pres = Presentation()
    pres.slides[0].shapes  # touch the deck so it is not a bare copy
    pkg = produced(pres)

    thumbnails = [n for n in pkg.namelist if n.startswith("docProps/thumbnail")]
    assert not thumbnails, (
        "the template's placeholder thumbnail is shipped in the output: %r"
        % thumbnails
    )
