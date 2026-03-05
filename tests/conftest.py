"""Shared fixtures for the aspose-slides-foss test suite."""
import os
import struct
import sys
import zlib

import pytest

# When ASPOSE_TEST_PKG_DIR is set (e.g. by build_production.py), use that
# directory instead of src/ so tests run against the production package.
_pkg_dir = os.environ.get("ASPOSE_TEST_PKG_DIR")
if _pkg_dir:
    sys.path.insert(0, _pkg_dir)
else:
    # Ensure the src directory is on the path so `import aspose` works.
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if SRC_DIR not in sys.path:
        sys.path.insert(0, SRC_DIR)

from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat


@pytest.fixture()
def tmp_pptx(tmp_path):
    """Return a helper that saves a Presentation to a temp file and reopens it.

    Usage::

        def test_something(tmp_pptx):
            pres = Presentation()
            # ... modify pres ...
            pres2 = tmp_pptx(pres)
            # ... assert on pres2 ...
            pres2.dispose()
    """

    def _save_and_reopen(pres: Presentation) -> Presentation:
        path = str(tmp_path / "roundtrip.pptx")
        pres.save(path, SaveFormat.PPTX)
        pres.dispose()
        return Presentation(path)

    return _save_and_reopen


@pytest.fixture()
def test_data_dir():
    """Return the path to the tests/test_data/ directory."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")


def create_test_png(r: int = 255, g: int = 0, b: int = 0) -> bytes:
    """Generate a minimal valid 1x1 PNG with the given RGB colour."""

    def _chunk(ct: bytes, data: bytes) -> bytes:
        c = ct + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw = bytes([0, r, g, b])
    idat = zlib.compress(raw)
    return header + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")
