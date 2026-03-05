from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .FontAlignment import FontAlignment
    from .IBulletFormat import IBulletFormat
    from .IPortionFormat import IPortionFormat
    from .NullableBool import NullableBool
    from .TextAlignment import TextAlignment

class IParagraphFormat(ABC):
    """This class contains the paragraph formatting properties. Unlike , all properties of this class are writeable."""
    @property
    def bullet(self) -> IBulletFormat:
        """Returns bullet format of the paragraph. Read-only ."""
        ...

    @property
    def depth(self) -> int:
        """Returns or sets depth of the paragraph. Value 0 means undefined value. Read/write ."""
        ...

    @depth.setter
    def depth(self, value: int):
        ...

    @property
    def alignment(self) -> TextAlignment:
        """Returns or sets the text alignment in a paragraph with no inheritance. Read/write ."""
        ...

    @alignment.setter
    def alignment(self, value: TextAlignment):
        ...

    @property
    def space_within(self) -> float:
        """Returns or sets the amount of space between base lines in a paragraph. Positive value means percentage, negative - size in points. No inheritance applied. Read/write ."""
        ...

    @space_within.setter
    def space_within(self, value: float):
        ...

    @property
    def space_before(self) -> float:
        """Returns or sets the amount of space before the first line in a paragraph with no inheritance. A positive value specifies the percentage of the font size that the white space should be. A negative value specifies the size of the white space in point size. Read/write ."""
        ...

    @space_before.setter
    def space_before(self, value: float):
        ...

    @property
    def space_after(self) -> float:
        """Returns or sets the amount of space after the last line in a paragraph with no inheritance. A positive value specifies the percentage of the font size that the white space should be. A negative value specifies the size of the white space in point size. Read/write ."""
        ...

    @space_after.setter
    def space_after(self, value: float):
        ...

    @property
    def east_asian_line_break(self) -> NullableBool:
        """Determines whether the East Asian line break is used in a paragraph. No inheritance applied. Read/write ."""
        ...

    @east_asian_line_break.setter
    def east_asian_line_break(self, value: NullableBool):
        ...

    @property
    def right_to_left(self) -> NullableBool:
        """Determines whether the Right to Left writing is used in a paragraph. No inheritance applied. Read/write ."""
        ...

    @right_to_left.setter
    def right_to_left(self, value: NullableBool):
        ...

    @property
    def latin_line_break(self) -> NullableBool:
        """Determines whether the Latin line break is used in a paragraph. No inheritance applied. Read/write ."""
        ...

    @latin_line_break.setter
    def latin_line_break(self, value: NullableBool):
        ...

    @property
    def hanging_punctuation(self) -> NullableBool:
        """Determines whether the hanging punctuation is used in a paragraph. No inheritance applied. Read/write ."""
        ...

    @hanging_punctuation.setter
    def hanging_punctuation(self, value: NullableBool):
        ...

    @property
    def margin_left(self) -> float:
        """Returns or sets the left margin in a paragraph with no inheritance. Read/write ."""
        ...

    @margin_left.setter
    def margin_left(self, value: float):
        ...

    @property
    def margin_right(self) -> float:
        """Returns or sets the right margin in a paragraph with no inheritance. Read/write ."""
        ...

    @margin_right.setter
    def margin_right(self, value: float):
        ...

    @property
    def indent(self) -> float:
        """Returns or sets paragraph First Line Indent/Hanging Indent with no inheritance. Hanging Indent can be defined with negative values. Read/write ."""
        ...

    @indent.setter
    def indent(self, value: float):
        ...

    @property
    def default_tab_size(self) -> float:
        """Returns or sets default tabulation size with no inheritance. Read/write ."""
        ...

    @default_tab_size.setter
    def default_tab_size(self, value: float):
        ...


    @property
    def font_alignment(self) -> FontAlignment:
        """Returns or sets a font alignment in a paragraph with no inheritance. Read/write ."""
        ...

    @font_alignment.setter
    def font_alignment(self, value: FontAlignment):
        ...

    @property
    def default_portion_format(self) -> IPortionFormat:
        """Returns default portion format of a paragraph. No inheritance applied. Read-only ."""
        ...

