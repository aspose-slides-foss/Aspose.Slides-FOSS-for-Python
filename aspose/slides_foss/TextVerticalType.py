from __future__ import annotations
from enum import Enum

class TextVerticalType(Enum):
    """Determines vertical writing mode for a text."""
    NOT_DEFINED = 'NotDefined'  # Not defined.
    HORIZONTAL = 'Horizontal'  # Horizontal text.
    VERTICAL = 'Vertical'  # Vertical text.
    VERTICAL270 = 'Vertical270'  # Vertical 270 degrees text.
    WORD_ART_VERTICAL = 'WordArtVertical'  # WordArt vertical text.
    EAST_ASIAN_VERTICAL = 'EastAsianVertical'  # East asian vertical text.
    MONGOLIAN_VERTICAL = 'MongolianVertical'  # Mongolian vertical text.
    WORD_ART_VERTICAL_RIGHT_TO_LEFT = 'WordArtVerticalRightToLeft'  # WordArt vertical right to left text.
