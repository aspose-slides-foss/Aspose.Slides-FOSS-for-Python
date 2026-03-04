"""
Image utility functions for parsing image headers and detecting content types.

Supports JPEG, PNG, GIF, BMP, TIFF, EMF, and WMF formats without external dependencies.
"""

from __future__ import annotations
import struct


# Magic byte signatures for image format detection
_PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
_JPEG_SIGNATURE = b'\xff\xd8\xff'
_GIF87_SIGNATURE = b'GIF87a'
_GIF89_SIGNATURE = b'GIF89a'
_BMP_SIGNATURE = b'BM'
_TIFF_LE_SIGNATURE = b'II\x2a\x00'
_TIFF_BE_SIGNATURE = b'MM\x00\x2a'
_EMF_SIGNATURE = b'\x01\x00\x00\x00'  # EMF record type 1 (EMR_HEADER)
_WMF_SIGNATURE = b'\xd7\xcd\xc6\x9a'  # WMF placeable header


# Extension to MIME type mapping
EXTENSION_CONTENT_TYPES: dict[str, str] = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'tiff': 'image/tiff',
    'tif': 'image/tiff',
    'emf': 'image/x-emf',
    'wmf': 'image/x-wmf',
    'svg': 'image/svg+xml',
}

# MIME type to default extension mapping
CONTENT_TYPE_EXTENSIONS: dict[str, str] = {
    'image/png': 'png',
    'image/jpeg': 'jpeg',
    'image/gif': 'gif',
    'image/bmp': 'bmp',
    'image/tiff': 'tiff',
    'image/x-emf': 'emf',
    'image/x-wmf': 'wmf',
    'image/svg+xml': 'svg',
}


def guess_content_type(data: bytes) -> str:
    """
    Detect the MIME content type of an image from its binary data.

    Args:
        data: Raw image bytes (at least first 12 bytes needed).

    Returns:
        MIME type string (e.g., 'image/jpeg'). Returns 'application/octet-stream' if unknown.
    """
    if len(data) < 4:
        return 'application/octet-stream'

    if data[:8] == _PNG_SIGNATURE:
        return 'image/png'
    if data[:3] == _JPEG_SIGNATURE:
        return 'image/jpeg'
    if data[:6] in (_GIF87_SIGNATURE, _GIF89_SIGNATURE):
        return 'image/gif'
    if data[:2] == _BMP_SIGNATURE:
        return 'image/bmp'
    if data[:4] in (_TIFF_LE_SIGNATURE, _TIFF_BE_SIGNATURE):
        return 'image/tiff'
    if data[:4] == _WMF_SIGNATURE:
        return 'image/x-wmf'
    # EMF: check for EMR_HEADER record type (1) and reasonable size
    if len(data) >= 44 and data[:4] == _EMF_SIGNATURE:
        record_size = struct.unpack_from('<I', data, 4)[0]
        if record_size >= 88:
            return 'image/x-emf'

    return 'application/octet-stream'


def guess_extension(data: bytes) -> str:
    """
    Guess the file extension for image data based on its content.

    Args:
        data: Raw image bytes.

    Returns:
        Extension string without dot (e.g., 'jpeg', 'png').
    """
    content_type = guess_content_type(data)
    return CONTENT_TYPE_EXTENSIONS.get(content_type, 'bin')


def get_image_dimensions(data: bytes) -> tuple[int, int]:
    """
    Parse image dimensions from binary header data.

    Args:
        data: Raw image bytes.

    Returns:
        Tuple of (width, height) in pixels. Returns (0, 0) if format is unrecognized.
    """
    if len(data) < 4:
        return (0, 0)

    if data[:8] == _PNG_SIGNATURE:
        return _get_png_dimensions(data)
    if data[:3] == _JPEG_SIGNATURE:
        return _get_jpeg_dimensions(data)
    if data[:6] in (_GIF87_SIGNATURE, _GIF89_SIGNATURE):
        return _get_gif_dimensions(data)
    if data[:2] == _BMP_SIGNATURE:
        return _get_bmp_dimensions(data)
    if data[:4] in (_TIFF_LE_SIGNATURE, _TIFF_BE_SIGNATURE):
        return _get_tiff_dimensions(data)

    return (0, 0)


def _get_png_dimensions(data: bytes) -> tuple[int, int]:
    """Parse PNG IHDR chunk for width and height."""
    if len(data) < 24:
        return (0, 0)
    # IHDR chunk starts at byte 8: length(4) + 'IHDR'(4) + width(4) + height(4)
    width = struct.unpack_from('>I', data, 16)[0]
    height = struct.unpack_from('>I', data, 20)[0]
    return (width, height)


def _get_jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Parse JPEG SOF marker for width and height."""
    offset = 2  # Skip SOI marker
    length = len(data)

    while offset < length - 1:
        if data[offset] != 0xFF:
            offset += 1
            continue

        marker = data[offset + 1]

        # Skip padding bytes
        if marker == 0xFF:
            offset += 1
            continue

        # SOF markers (0xC0 through 0xCF, excluding 0xC4 DHT and 0xC8 JPG and 0xCC DAC)
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                       0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if offset + 9 < length:
                height = struct.unpack_from('>H', data, offset + 5)[0]
                width = struct.unpack_from('>H', data, offset + 7)[0]
                return (width, height)
            return (0, 0)

        # Skip other markers (read segment length)
        if offset + 3 < length:
            segment_length = struct.unpack_from('>H', data, offset + 2)[0]
            offset += 2 + segment_length
        else:
            break

    return (0, 0)


def _get_gif_dimensions(data: bytes) -> tuple[int, int]:
    """Parse GIF logical screen descriptor for width and height."""
    if len(data) < 10:
        return (0, 0)
    width = struct.unpack_from('<H', data, 6)[0]
    height = struct.unpack_from('<H', data, 8)[0]
    return (width, height)


def _get_bmp_dimensions(data: bytes) -> tuple[int, int]:
    """Parse BMP info header for width and height."""
    if len(data) < 26:
        return (0, 0)
    width = struct.unpack_from('<i', data, 18)[0]
    height = abs(struct.unpack_from('<i', data, 22)[0])  # Height can be negative (top-down)
    return (width, height)


def _get_tiff_dimensions(data: bytes) -> tuple[int, int]:
    """Parse TIFF IFD for ImageWidth and ImageLength tags."""
    if len(data) < 8:
        return (0, 0)

    # Determine byte order
    if data[:2] == b'II':
        endian = '<'
    else:
        endian = '>'

    # Get offset to first IFD
    ifd_offset = struct.unpack_from(f'{endian}I', data, 4)[0]
    if ifd_offset + 2 > len(data):
        return (0, 0)

    # Read number of IFD entries
    num_entries = struct.unpack_from(f'{endian}H', data, ifd_offset)[0]

    width = 0
    height = 0
    offset = ifd_offset + 2

    for _ in range(num_entries):
        if offset + 12 > len(data):
            break
        tag = struct.unpack_from(f'{endian}H', data, offset)[0]
        field_type = struct.unpack_from(f'{endian}H', data, offset + 2)[0]
        value_offset = offset + 8

        # Read value based on type (SHORT=3, LONG=4)
        if field_type == 3:  # SHORT
            value = struct.unpack_from(f'{endian}H', data, value_offset)[0]
        elif field_type == 4:  # LONG
            value = struct.unpack_from(f'{endian}I', data, value_offset)[0]
        else:
            value = 0

        if tag == 256:  # ImageWidth
            width = value
        elif tag == 257:  # ImageLength (height)
            height = value

        if width and height:
            break

        offset += 12

    return (width, height)
