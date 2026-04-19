"""Tests for Presentation create / load / save / properties."""
import io
import os

import pytest

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat


def test_create_empty():
    """A brand-new presentation has exactly 1 slide."""
    pres = Presentation()
    assert len(pres.slides) == 1
    pres.dispose()


def test_save_and_reload(tmp_pptx):
    """Round-trip: create → save → reload preserves slide count."""
    pres = Presentation()
    pres2 = tmp_pptx(pres)
    assert len(pres2.slides) == 1
    pres2.dispose()


def test_save_to_stream():
    """Saving to a BytesIO stream produces a non-empty buffer."""
    pres = Presentation()
    buf = io.BytesIO()
    pres.save(buf, SaveFormat.PPTX)
    assert buf.tell() > 0
    pres.dispose()


def test_context_manager():
    """Presentation can be used as a context manager."""
    with Presentation() as pres:
        assert len(pres.slides) >= 1


def test_first_slide_number(tmp_pptx):
    """first_slide_number persists across save/reload."""
    pres = Presentation()
    pres.first_slide_number = 5
    assert pres.first_slide_number == 5

    pres2 = tmp_pptx(pres)
    assert pres2.first_slide_number == 5
    pres2.dispose()


def test_load_existing(test_data_dir):
    """Load a known .pptx from test_data and verify it opens."""
    path = os.path.join(test_data_dir, "Presentation.pptx")
    if not os.path.exists(path):
        pytest.skip("Presentation.pptx not found in test_data")
    pres = Presentation(path)
    assert len(pres.slides) >= 1
    pres.dispose()


def test_dispose_is_idempotent():
    """Calling dispose() twice must not raise."""
    pres = Presentation()
    pres.dispose()
    pres.dispose()  # second call should be harmless


def test_slide_count_after_add():
    """Adding a slide increases slide count to 2."""
    pres = Presentation()
    layout = pres.layout_slides[0]
    pres.slides.add_empty_slide(layout)
    assert len(pres.slides) == 2
    pres.dispose()
