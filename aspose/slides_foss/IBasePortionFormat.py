from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IColorFormat import IColorFormat
    from .IEffectFormat import IEffectFormat
    from .IFillFormat import IFillFormat
    from .IFontData import IFontData
    from .ILineFormat import ILineFormat
    from .NullableBool import NullableBool
    from .TextCapType import TextCapType
    from .TextStrikethroughType import TextStrikethroughType
    from .TextUnderlineType import TextUnderlineType

class IBasePortionFormat(ABC):
    """This class contains the text portion formatting properties. Unlike , all properties of this class are writeable."""
    @property
    def line_format(self) -> ILineFormat:
        """Returns the LineFormat properties for text outlining. No inheritance applied. Read-only ."""
        ...

    @property
    def fill_format(self) -> IFillFormat:
        """Returns the text FillFormat properties. No inheritance applied. Read-only ."""
        ...

    @property
    def effect_format(self) -> IEffectFormat:
        """Returns the text EffectFormat properties. No inheritance applied. Read-only ."""
        ...

    @property
    def highlight_color(self) -> IColorFormat:
        """Returns the color used to highlight a text. No inheritance applied. Read-only ."""
        ...

    @property
    def underline_line_format(self) -> ILineFormat:
        """Returns the LineFormat properties used to outline underline line. No inheritance applied. Read-only ."""
        ...

    @property
    def underline_fill_format(self) -> IFillFormat:
        """Returns the underline line FillFormat properties. No inheritance applied. Read-only ."""
        ...

    @property
    def font_bold(self) -> NullableBool:
        """Determines whether the font is bold. No inheritance applied. Read/write ."""
        ...

    @font_bold.setter
    def font_bold(self, value: NullableBool):
        ...

    @property
    def font_italic(self) -> NullableBool:
        """Determines whether the font is itallic. No inheritance applied. Read/write ."""
        ...

    @font_italic.setter
    def font_italic(self, value: NullableBool):
        ...

    @property
    def kumimoji(self) -> NullableBool:
        """Determines whether the numbers should ignore text eastern language-specific vertical text layout. No inheritance applied. Read/write ."""
        ...

    @kumimoji.setter
    def kumimoji(self, value: NullableBool):
        ...

    @property
    def normalise_height(self) -> NullableBool:
        """Determines whether the height of a text should be normalized. No inheritance applied. Read/write ."""
        ...

    @normalise_height.setter
    def normalise_height(self, value: NullableBool):
        ...

    @property
    def proof_disabled(self) -> NullableBool:
        """Determines whether the text shouldn't be proofed. No inheritance applied. Read/write ."""
        ...

    @proof_disabled.setter
    def proof_disabled(self, value: NullableBool):
        ...

    @property
    def font_underline(self) -> TextUnderlineType:
        """Returns or sets the text underline type. No inheritance applied. Read/write ."""
        ...

    @font_underline.setter
    def font_underline(self, value: TextUnderlineType):
        ...

    @property
    def text_cap_type(self) -> TextCapType:
        """Returns or sets the type of text capitalization. No inheritance applied. Read/write ."""
        ...

    @text_cap_type.setter
    def text_cap_type(self, value: TextCapType):
        ...

    @property
    def strikethrough_type(self) -> TextStrikethroughType:
        """Returns or sets the strikethrough type of a text. No inheritance applied. Read/write ."""
        ...

    @strikethrough_type.setter
    def strikethrough_type(self, value: TextStrikethroughType):
        ...

    @property
    def is_hard_underline_line(self) -> NullableBool:
        """Determines whether the underline style has own LineFormat properties or inherits it from the LineFormat properties of the text. Read/write ."""
        ...

    @is_hard_underline_line.setter
    def is_hard_underline_line(self, value: NullableBool):
        ...

    @property
    def is_hard_underline_fill(self) -> NullableBool:
        """Determines whether the underline style has own FillFormat properties or inherits it from the FillFormat properties of the text. Read/write ."""
        ...

    @is_hard_underline_fill.setter
    def is_hard_underline_fill(self, value: NullableBool):
        ...

    @property
    def font_height(self) -> float:
        """Returns or sets the font height of a portion. float.NaN means height is undefined and should be inherited from the Master. Read/write ."""
        ...

    @font_height.setter
    def font_height(self, value: float):
        ...

    @property
    def latin_font(self) -> IFontData:
        """Returns or sets the Latin font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        ...

    @latin_font.setter
    def latin_font(self, value: IFontData):
        ...

    @property
    def east_asian_font(self) -> IFontData:
        """Returns or sets the East Asian font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        ...

    @east_asian_font.setter
    def east_asian_font(self, value: IFontData):
        ...

    @property
    def complex_script_font(self) -> IFontData:
        """Returns or sets the complex script font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        ...

    @complex_script_font.setter
    def complex_script_font(self, value: IFontData):
        ...

    @property
    def symbol_font(self) -> IFontData:
        """Returns or sets the symbolic font info. Null means font is undefined and should be inherited from the Master. Read/write ."""
        ...

    @symbol_font.setter
    def symbol_font(self, value: IFontData):
        ...

    @property
    def escapement(self) -> float:
        """Returns or sets the superscript or subscript text. Value from -100% (subscript) to 100% (superscript). float.NaN means value is undefined and should be inherited from the Master. Read/write ."""
        ...

    @escapement.setter
    def escapement(self, value: float):
        ...

    @property
    def kerning_minimal_size(self) -> float:
        """Returns or sets the minimal font size, for which kerning should be switched on. float.NaN means value is undefined and should be inherited from the Master. Read/write ."""
        ...

    @kerning_minimal_size.setter
    def kerning_minimal_size(self, value: float):
        ...

    @property
    def language_id(self) -> str:
        """Returns or sets the Id of a proofing language. Used for checking spelling and grammar. Read/write ."""
        ...

    @language_id.setter
    def language_id(self, value: str):
        ...

    @property
    def alternative_language_id(self) -> str:
        """Returns or sets the Id of an alternative language. Read/write ."""
        ...

    @alternative_language_id.setter
    def alternative_language_id(self, value: str):
        ...

    @property
    def spacing(self) -> float:
        """Returns or sets the intercharacter spacing increment. float.NaN means value is undefined and should be inherited from the Master. Read/write ."""
        ...

    @spacing.setter
    def spacing(self, value: float):
        ...

    @property
    def spell_check(self) -> bool:
        """Gets or sets a value indicating whether spell checking is enabled for the text portion. When this property is set to false, spelling checks for text elements are suppressed. When set to true, spell checking is allowed. Default value is false."""
        ...

    @spell_check.setter
    def spell_check(self, value: bool):
        ...
