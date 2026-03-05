from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IGeometryShape import IGeometryShape

if TYPE_CHECKING:
    from .IPictureFillFormat import IPictureFillFormat
    from .IPictureFrameLock import IPictureFrameLock

class IPictureFrame(IGeometryShape, ABC):
    """Represents a frame with a picture inside."""
    @property
    def picture_frame_lock(self) -> IPictureFrameLock:
        """Returns PictureFrame's locks. Read-only ."""
        ...

    @property
    def picture_format(self) -> IPictureFillFormat:
        """Returns the PictureFillFormat object for a picture frame. Read-only ."""
        ...

    @property
    def relative_scale_height(self) -> float:
        """Returns or sets the scale of height(relative to original picture size) of the picture frame. Value 1.0 corresponds to 100%. Read/write ."""
        ...

    @relative_scale_height.setter
    def relative_scale_height(self, value: float):
        ...

    @property
    def relative_scale_width(self) -> float:
        """Returns or sets the scale of width (relative to original picture size) of the picture frame. Value 1.0 corresponds to 100%. Read/write ."""
        ...

    @relative_scale_width.setter
    def relative_scale_width(self, value: float):
        ...

