from __future__ import annotations
from enum import Enum

class TextShapeType(Enum):
    """Represents text wrapping shape."""
    NOT_DEFINED = 'NotDefined'  # Not defined
    NONE = 'None'  # No shape
    PLAIN = 'Plain'  # Plain
    STOP = 'Stop'  # Stop Sign
    TRIANGLE = 'Triangle'  # Triangle
    TRIANGLE_INVERTED = 'TriangleInverted'  # Inverted Triangle
    CHEVRON = 'Chevron'  # Chevron
    CHEVRON_INVERTED = 'ChevronInverted'  # Inverted Chevron
    RING_INSIDE = 'RingInside'  # Inside Ring
    RING_OUTSIDE = 'RingOutside'  # Outside Ring
    ARCH_UP = 'ArchUp'  # Upward Arch
    ARCH_DOWN = 'ArchDown'  # Downward Arch
    CIRCLE = 'Circle'  # Circle
    BUTTON = 'Button'  # Button
    ARCH_UP_POUR = 'ArchUpPour'  # Upward Pour Arch
    ARCH_DOWN_POUR = 'ArchDownPour'  # Downward Pour Arch
    CIRCLE_POUR = 'CirclePour'  # Circle Pour
    BUTTON_POUR = 'ButtonPour'  # Button Pour
    CURVE_UP = 'CurveUp'  # Upward Curve
    CURVE_DOWN = 'CurveDown'  # Downward Curve
    CAN_UP = 'CanUp'  # Upward Can
    CAN_DOWN = 'CanDown'  # Downward Can
    WAVE1 = 'Wave1'  # Wave 1
    WAVE2 = 'Wave2'  # Wave 2
    DOUBLE_WAVE1 = 'DoubleWave1'  # Double Wave 1
    WAVE4 = 'Wave4'  # Wave 4
    INFLATE = 'Inflate'  # Inflate
    DEFLATE = 'Deflate'  # Deflate
    INFLATE_BOTTOM = 'InflateBottom'  # Bottom Inflate
    DEFLATE_BOTTOM = 'DeflateBottom'  # Bottom Deflate
    INFLATE_TOP = 'InflateTop'  # Top Inflate
    DEFLATE_TOP = 'DeflateTop'  # Top Deflate
    DEFLATE_INFLATE = 'DeflateInflate'  # Deflate-Inflate
    DEFLATE_INFLATE_DEFLATE = 'DeflateInflateDeflate'  # Deflate-Inflate-Deflate
    FADE_RIGHT = 'FadeRight'  # Right Fade
    FADE_LEFT = 'FadeLeft'  # Left Fade
    FADE_UP = 'FadeUp'  # Upward Fade
    FADE_DOWN = 'FadeDown'  # Downward Fade
    SLANT_UP = 'SlantUp'  # Upward Slant
    SLANT_DOWN = 'SlantDown'  # Downward Slant
    CASCADE_UP = 'CascadeUp'  # Upward Cascade
    CASCADE_DOWN = 'CascadeDown'  # Downward Cascade
    CUSTOM = 'Custom'  # Custom
