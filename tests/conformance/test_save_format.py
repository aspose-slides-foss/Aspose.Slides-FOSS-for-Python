"""Asking for a template, a slideshow or a macro-enabled deck must produce one.

`save(path, SaveFormat.POTX)` writes a package whose main part is still declared
`...presentationml.presentation.main+xml`, so the file claims to be an ordinary
presentation whatever extension it was given.  PowerPoint refuses several of the
mislabelled names outright — *"PowerPoint can't open this file because its file
extension has changed"* — and a consumer that trusts the content type is simply
told the wrong thing.

The six PPTX-family formats are the same OPC shape and differ only in the
content type of `/ppt/presentation.xml`, so getting them right is a lookup, not
a conversion.
"""

from __future__ import annotations

import pytest

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat

#: ECMA-376 Part 1 §15.2.11 plus the Microsoft macro-enabled types PowerPoint
#: writes.  One row per format that is the OPC shape this library produces.
MAIN_PART_CONTENT_TYPE = {
    SaveFormat.PPTX: "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
    SaveFormat.PPSX: "application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml",
    SaveFormat.POTX: "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml",
    SaveFormat.PPTM: "application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml",
    SaveFormat.PPSM: "application/vnd.ms-powerpoint.slideshow.macroEnabled.main+xml",
    SaveFormat.POTM: "application/vnd.ms-powerpoint.template.macroEnabled.main+xml",
}

EXTENSION = {
    SaveFormat.PPTX: "pptx",
    SaveFormat.PPSX: "ppsx",
    SaveFormat.POTX: "potx",
    SaveFormat.PPTM: "pptm",
    SaveFormat.PPSM: "ppsm",
    SaveFormat.POTM: "potm",
}


@pytest.mark.parametrize(
    "save_format", list(MAIN_PART_CONTENT_TYPE), ids=lambda f: f.value
)
def test_the_saved_file_declares_the_format_that_was_asked_for(produced, save_format):
    """The main part's content type must match the requested format."""
    pkg = produced(
        Presentation(), save_format, "deck." + EXTENSION[save_format]
    )

    assert pkg.content_type_of("ppt/presentation.xml") == MAIN_PART_CONTENT_TYPE[save_format]


def test_the_six_office_formats_do_not_all_produce_the_same_file(produced, tmp_path):
    """Six requested formats must not collapse into one content type."""
    written = {}
    for save_format, extension in EXTENSION.items():
        pkg = produced(Presentation(), save_format, "distinct." + extension)
        written[save_format] = pkg.content_type_of("ppt/presentation.xml")

    assert len(set(written.values())) == len(written), (
        "the six formats produced %d distinct main content types, not %d: %r"
        % (len(set(written.values())), len(written),
           {f.value: t for f, t in written.items()})
    )


UNSUPPORTED_FORMATS = [
    f
    for f in SaveFormat
    if f not in MAIN_PART_CONTENT_TYPE and f is not SaveFormat.MD
]


@pytest.mark.parametrize("save_format", UNSUPPORTED_FORMATS, ids=lambda f: f.value)
def test_an_unimplemented_format_refuses_rather_than_writing_a_pptx(
    tmp_path, save_format
):
    """A format with no exporter must raise, never write a mislabelled package.

    This is the half of the behaviour that is already correct; it is asserted
    so a future change that adds a content type cannot quietly start writing
    presentation packages under a `.pdf` name instead.
    """
    pres = Presentation()
    try:
        with pytest.raises(ValueError):
            pres.save(str(tmp_path / ("out." + save_format.value.lower())), save_format)
    finally:
        pres.dispose()
