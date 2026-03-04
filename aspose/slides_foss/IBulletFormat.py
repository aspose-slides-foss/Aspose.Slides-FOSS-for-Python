from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BulletType import BulletType
    from .IBulletFormatEffectiveData import IBulletFormatEffectiveData
    from .IColorFormat import IColorFormat
    from .IFontData import IFontData
    from .ISlidesPicture import ISlidesPicture
    from .NullableBool import NullableBool
    from .NumberedBulletStyle import NumberedBulletStyle

class IBulletFormat(ABC):
    """Represents paragraph bullet formatting properties."""
    @property
    def type(self) -> BulletType:
        """Returns or sets the bullet type of a paragraph with no inheritance. Read/write ."""
        ...

    @type.setter
    def type(self, value: BulletType):
        ...

    @property
    def char(self) -> str:
        """Returns or sets the bullet char of a paragraph with no inheritance. Read/write ."""
        ...

    @char.setter
    def char(self, value: str):
        ...

    @property
    def font(self) -> IFontData:
        """Returns or sets the bullet font of a paragraph with no inheritance. Read/write ."""
        ...

    @font.setter
    def font(self, value: IFontData):
        ...

    @property
    def height(self) -> float:
        """Returns or sets the bullet height of a paragraph with no inheritance. Value float.NaN determines that bullet inherits height from the first portion in the paragraph. Read/write ."""
        ...

    @height.setter
    def height(self, value: float):
        ...

    @property
    def color(self) -> IColorFormat:
        """Returns the color format of a bullet of a paragraph with no inheritance. Read-only ."""
        ...

    @property
    def picture(self) -> ISlidesPicture:
        """Returns the picture used as a bullet in a paragraph with no inheritance. Read-only ."""
        ...

    @property
    def numbered_bullet_start_with(self) -> int:
        """Returns or sets the first number which is used for group of numbered bullets with no inheritance. Read/write ."""
        ...

    @numbered_bullet_start_with.setter
    def numbered_bullet_start_with(self, value: int):
        ...

    @property
    def numbered_bullet_style(self) -> NumberedBulletStyle:
        """Returns or sets the style of a numbered bullet with no inheritance. Read/write ."""
        ...

    @numbered_bullet_style.setter
    def numbered_bullet_style(self, value: NumberedBulletStyle):
        ...

    @property
    def is_bullet_hard_color(self) -> NullableBool:
        """Determines whether the bullet has own color or inherits it from the first portion in the paragraph. NullableBool.True if bullet has own color and NullableBool.False if bullet inherits color from the first portion in the paragraph. Read/write ."""
        ...

    @is_bullet_hard_color.setter
    def is_bullet_hard_color(self, value: NullableBool):
        ...

    @property
    def is_bullet_hard_font(self) -> NullableBool:
        """Determines whether the bullet has own font or inherits it from the first portion in the paragraph. NullableBool.True if bullet has own font and NullableBool.False if bullet inherits font from the first portion in the paragraph. Read/write ."""
        ...

    @is_bullet_hard_font.setter
    def is_bullet_hard_font(self, value: NullableBool):
        ...


