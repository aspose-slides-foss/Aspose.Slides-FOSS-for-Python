from __future__ import annotations
from enum import Enum

class SchemeColor(Enum):
    """Represents colors in a color scheme."""
    NOT_DEFINED = 'NotDefined'  # Color scheme is not defined.
    BACKGROUND1 = 'Background1'
    TEXT1 = 'Text1'
    BACKGROUND2 = 'Background2'
    TEXT2 = 'Text2'
    ACCENT1 = 'Accent1'
    ACCENT2 = 'Accent2'
    ACCENT3 = 'Accent3'
    ACCENT4 = 'Accent4'
    ACCENT5 = 'Accent5'
    ACCENT6 = 'Accent6'
    HYPERLINK = 'Hyperlink'
    FOLLOWED_HYPERLINK = 'FollowedHyperlink'
    STYLE_COLOR = 'StyleColor'
    DARK1 = 'Dark1'
    LIGHT1 = 'Light1'
    DARK2 = 'Dark2'
    LIGHT2 = 'Light2'
