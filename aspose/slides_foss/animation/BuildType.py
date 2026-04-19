from __future__ import annotations
from enum import Enum

class BuildType(Enum):
    """Determines how text will appear on a shape during animation."""
    AS_ONE_OBJECT = 'AsOneObject'  # With containing shape.
    ALL_PARAGRAPHS_AT_ONCE = 'AllParagraphsAtOnce'  # All paragraph.
    BY_LEVEL_PARAGRAPHS1 = 'ByLevelParagraphs1'  # By groups of paragraphs of depth 1.
    BY_LEVEL_PARAGRAPHS2 = 'ByLevelParagraphs2'  # By groups of paragraphs of depth 2.
    BY_LEVEL_PARAGRAPHS3 = 'ByLevelParagraphs3'  # By groups of paragraphs of depth 3.
    BY_LEVEL_PARAGRAPHS4 = 'ByLevelParagraphs4'  # By groups of paragraphs of depth 4.
    BY_LEVEL_PARAGRAPHS5 = 'ByLevelParagraphs5'  # By groups of paragraphs of depth 5.
