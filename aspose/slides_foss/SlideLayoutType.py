from __future__ import annotations
from enum import Enum

class SlideLayoutType(Enum):
    """Represents the slide layout type."""
    CUSTOM = 'Custom'  # Custom
    TITLE = 'Title'  # Title
    TEXT = 'Text'  # Text
    TWO_COLUMN_TEXT = 'TwoColumnText'  # Two Column Text
    TABLE = 'Table'  # Table
    TEXT_AND_CHART = 'TextAndChart'  # Text and Chart
    CHART_AND_TEXT = 'ChartAndText'  # Chart and Text
    DIAGRAM = 'Diagram'  # Diagram
    CHART = 'Chart'  # Chart
    TEXT_AND_CLIP_ART = 'TextAndClipArt'  # Text and Clip Art
    CLIP_ART_AND_TEXT = 'ClipArtAndText'  # Clip Art and Text
    TITLE_ONLY = 'TitleOnly'  # Title Only
    BLANK = 'Blank'  # Blank
    TEXT_AND_OBJECT = 'TextAndObject'  # Text and Object
    OBJECT_AND_TEXT = 'ObjectAndText'  # Object and Text
    OBJECT = 'Object'  # Object
    TITLE_AND_OBJECT = 'TitleAndObject'  # Title and Object
    TEXT_AND_MEDIA = 'TextAndMedia'  # Text and Media
    MEDIA_AND_TEXT = 'MediaAndText'  # Media and Text
    OBJECT_OVER_TEXT = 'ObjectOverText'  # Object over Text
    TEXT_OVER_OBJECT = 'TextOverObject'  # Text over Object
    TEXT_AND_TWO_OBJECTS = 'TextAndTwoObjects'  # Text and Two Objects
    TWO_OBJECTS_AND_TEXT = 'TwoObjectsAndText'  # Two Objects and Text
    TWO_OBJECTS_OVER_TEXT = 'TwoObjectsOverText'  # Two Objects over Text
    FOUR_OBJECTS = 'FourObjects'  # Four Objects
    VERTICAL_TEXT = 'VerticalText'  # Vertical Text
    CLIP_ART_AND_VERTICAL_TEXT = 'ClipArtAndVerticalText'  # Clip Art and Vertical Text
    VERTICAL_TITLE_AND_TEXT = 'VerticalTitleAndText'  # Vertical Title and Text
    VERTICAL_TITLE_AND_TEXT_OVER_CHART = 'VerticalTitleAndTextOverChart'  # Vertical Title and Text Over Chart
    TWO_OBJECTS = 'TwoObjects'  # Two Objects
    OBJECT_AND_TWO_OBJECT = 'ObjectAndTwoObject'  # Object and Two Object
    TWO_OBJECTS_AND_OBJECT = 'TwoObjectsAndObject'  # Two Objects and Object
    SECTION_HEADER = 'SectionHeader'  # Section Header
    TWO_TEXT_AND_TWO_OBJECTS = 'TwoTextAndTwoObjects'  # Two Text and Two Objects
    TITLE_OBJECT_AND_CAPTION = 'TitleObjectAndCaption'  # Title, Object, and Caption
    PICTURE_AND_CAPTION = 'PictureAndCaption'  # Picture and Caption
