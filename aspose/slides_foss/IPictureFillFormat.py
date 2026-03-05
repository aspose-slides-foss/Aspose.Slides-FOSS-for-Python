from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .IPPImage import IPPImage
    from .ISlidesPicture import ISlidesPicture
    from .PictureFillMode import PictureFillMode
    from .RectangleAlignment import RectangleAlignment
    from .TileFlip import TileFlip

class IPictureFillFormat(IFillParamSource, ABC):
    """Represents a picture fill style."""
    @property
    def dpi(self) -> int:
        """Returns or sets the dpi which is used to fill a picture. Read/write ."""
        ...

    @dpi.setter
    def dpi(self, value: int):
        ...

    @property
    def picture_fill_mode(self) -> PictureFillMode:
        """Returns or sets the picture fill mode. Read/write ."""
        ...

    @picture_fill_mode.setter
    def picture_fill_mode(self, value: PictureFillMode):
        ...

    @property
    def picture(self) -> ISlidesPicture:
        """Returns the picture. Read-only ."""
        ...

    @property
    def crop_left(self) -> float:
        """Returns or sets the number of percents of real image width that are cropped off the left of the picture. Read/write ."""
        ...

    @crop_left.setter
    def crop_left(self, value: float):
        ...

    @property
    def crop_top(self) -> float:
        """Returns or sets the number of percents of real image height that are cropped off the top of the picture. Read/write ."""
        ...

    @crop_top.setter
    def crop_top(self, value: float):
        ...

    @property
    def crop_right(self) -> float:
        """Returns or sets the number of percents of real image width that are cropped off the right of the picture. Read/write ."""
        ...

    @crop_right.setter
    def crop_right(self, value: float):
        ...

    @property
    def crop_bottom(self) -> float:
        """Returns or sets the number of percents of real image height that are cropped off the bottom of the picture. Read/write ."""
        ...

    @crop_bottom.setter
    def crop_bottom(self, value: float):
        ...

    @property
    def stretch_offset_left(self) -> float:
        """Returns or sets left edge of the fill rectangle that is defined by a percentage offset from the left edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        ...

    @stretch_offset_left.setter
    def stretch_offset_left(self, value: float):
        ...

    @property
    def stretch_offset_top(self) -> float:
        """Returns or sets top edge of the fill rectangle that is defined by a percentage offset from the top edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        ...

    @stretch_offset_top.setter
    def stretch_offset_top(self, value: float):
        ...

    @property
    def stretch_offset_right(self) -> float:
        """Returns or sets right edge of the fill rectangle that is defined by a percentage offset from the right edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        ...

    @stretch_offset_right.setter
    def stretch_offset_right(self, value: float):
        ...

    @property
    def stretch_offset_bottom(self) -> float:
        """Returns or sets bottom edge of the fill rectangle that is defined by a percentage offset from the bottom edge of the shape's bounding box. A positive percentage specifies an inset, while a negative percentage specifies an outset. Read/write ."""
        ...

    @stretch_offset_bottom.setter
    def stretch_offset_bottom(self, value: float):
        ...

    @property
    def tile_offset_x(self) -> float:
        """Returns or sets the horizontal offset of the texture from the shape's origin in points. A positive value moves the texture to the right, while a negative value moves it to the left. Read/write ."""
        ...

    @tile_offset_x.setter
    def tile_offset_x(self, value: float):
        ...

    @property
    def tile_offset_y(self) -> float:
        """Returns or sets the vertical offset of the texture from the shape's origin in points. A positive value moves the texture down, while a negative value moves it up. Read/write ."""
        ...

    @tile_offset_y.setter
    def tile_offset_y(self, value: float):
        ...

    @property
    def tile_scale_x(self) -> float:
        """Returns or sets the horizontal scale for the texture fill as a percentage. Read/write ."""
        ...

    @tile_scale_x.setter
    def tile_scale_x(self, value: float):
        ...

    @property
    def tile_scale_y(self) -> float:
        """Returns or sets the vertical scale for the texture fill as a percentage. Read/write ."""
        ...

    @tile_scale_y.setter
    def tile_scale_y(self, value: float):
        ...

    @property
    def tile_alignment(self) -> RectangleAlignment:
        """Returns or sets how the texture is aligned within the shape. This setting controls the starting point of the texture pattern and how it repeats across the shape. Read/write ."""
        ...

    @tile_alignment.setter
    def tile_alignment(self, value: RectangleAlignment):
        ...

    @property
    def tile_flip(self) -> TileFlip:
        """Flips the texture tile around its horizontal, vertical or both axis. Read/write ."""
        ...

    @tile_flip.setter
    def tile_flip(self, value: TileFlip):
        ...






