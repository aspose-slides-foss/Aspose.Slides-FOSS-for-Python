"""
PPTX-specific parsing and manipulation module.

Provides classes and constants for working with PowerPoint presentation XML.
"""

from .constants import *
from .presentation_part import PresentationPart, SlideReference, MasterReference
from .slide_part import SlidePart
from .layout_slide_part import LayoutSlidePart
from .master_slide_part import MasterSlidePart
from .notes_slide_part import NotesSlidePart
from .core_properties_part import CorePropertiesPart
from .app_properties_part import AppPropertiesPart
from .custom_properties_part import CustomPropertiesPart
from .comment_authors_part import CommentAuthorsPart
from .comments_part import CommentsPart

__all__ = [
    'PresentationPart', 'SlideReference', 'MasterReference',
    'SlidePart', 'LayoutSlidePart', 'MasterSlidePart', 'NotesSlidePart',
    'CorePropertiesPart', 'AppPropertiesPart', 'CustomPropertiesPart',
    'CommentAuthorsPart', 'CommentsPart',
    'NS', 'NAMESPACES',
]
