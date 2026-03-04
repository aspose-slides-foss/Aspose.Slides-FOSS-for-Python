from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ITextFrameFormatEffectiveData import ITextFrameFormatEffectiveData
    from .ITextStyle import ITextStyle
    from .IThreeDFormat import IThreeDFormat
    from .NullableBool import NullableBool
    from .TextAnchorType import TextAnchorType
    from .TextAutofitType import TextAutofitType
    from .TextShapeType import TextShapeType
    from .TextVerticalType import TextVerticalType

class ITextFrameFormat(ABC):
    """Contains the TextFrame's formatting properties."""

    @property
    def margin_left(self) -> float:
        """Returns or sets the left margin (points) in a TextFrame. Read/write ."""
        ...

    @margin_left.setter
    def margin_left(self, value: float):
        ...

    @property
    def margin_right(self) -> float:
        """Returns or sets the right margin (points) in a TextFrame. Read/write ."""
        ...

    @margin_right.setter
    def margin_right(self, value: float):
        ...

    @property
    def margin_top(self) -> float:
        """Returns or sets the top margin (points) in a TextFrame. Read/write ."""
        ...

    @margin_top.setter
    def margin_top(self, value: float):
        ...

    @property
    def margin_bottom(self) -> float:
        """Returns or sets the bottom margin (points) in a TextFrame. Read/write ."""
        ...

    @margin_bottom.setter
    def margin_bottom(self, value: float):
        ...

    @property
    def wrap_text(self) -> NullableBool:
        """True if text is wrapped at TextFrame's margins. Read/write ."""
        ...

    @wrap_text.setter
    def wrap_text(self, value: NullableBool):
        ...

    @property
    def anchoring_type(self) -> TextAnchorType:
        """Returns or sets vertical anchor text in a TextFrame. Read/write ."""
        ...

    @anchoring_type.setter
    def anchoring_type(self, value: TextAnchorType):
        ...

    @property
    def center_text(self) -> NullableBool:
        """If NullableBool.True then text should be centered in box horizontally. Read/write ."""
        ...

    @center_text.setter
    def center_text(self, value: NullableBool):
        ...

    @property
    def text_vertical_type(self) -> TextVerticalType:
        """Determines text orientation. The resulted value of visual text rotation summarized from this property and custom angle in property RotationAngle. Read/write ."""
        ...

    @text_vertical_type.setter
    def text_vertical_type(self, value: TextVerticalType):
        ...

    @property
    def autofit_type(self) -> TextAutofitType:
        """Returns or sets text's autofit mode. Read/write ."""
        ...

    @autofit_type.setter
    def autofit_type(self, value: TextAutofitType):
        ...

    @property
    def column_count(self) -> int:
        """Returns or sets number of columns in the text area. This value must be a positive number. Otherwise, the value will be set to zero. Value 0 means undefined value. Read/write ."""
        ...

    @column_count.setter
    def column_count(self, value: int):
        ...

    @property
    def column_spacing(self) -> float:
        """Returns or sets the space between text columns in the text area (in points). This should only apply when there is more than 1 column present. This value must be a positive number. Otherwise, the value will be set to zero. Read/write ."""
        ...

    @column_spacing.setter
    def column_spacing(self, value: float):
        ...

    @property
    def three_d_format(self) -> IThreeDFormat:
        """Returns the ThreeDFormat object that represents 3d effect properties for a text. Read-only ."""
        ...

    @property
    def keep_text_flat(self) -> bool:
        """Returns or set keeping text out of 3D scene entirely. Read/write ."""
        ...

    @keep_text_flat.setter
    def keep_text_flat(self, value: bool):
        ...

    @property
    def rotation_angle(self) -> float:
        """Specifies the custom rotation that is being applied to the text within the bounding box. If it not specified, the rotation of the accompanying shape is used. If it is specified, then this is applied independently from the shape. That is the shape can have a rotation applied in addition to the text itself having a rotation applied to it. The resulted value of visual text rotation summarized from this property and predefined vertical type in property TextVerticalType. Read/write ."""
        ...

    @rotation_angle.setter
    def rotation_angle(self, value: float):
        ...

    @property
    def transform(self) -> TextShapeType:
        """Gets or sets text wrapping shape. Read/write ."""
        ...

    @transform.setter
    def transform(self, value: TextShapeType):
        ...

