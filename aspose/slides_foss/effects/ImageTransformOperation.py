from __future__ import annotations
from typing import TYPE_CHECKING
from ..PVIObject import PVIObject
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent
from .IImageTransformOperation import IImageTransformOperation
if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..IPresentation import IPresentation

class ImageTransformOperation(PVIObject, ISlideComponent, IPresentationComponent, IImageTransformOperation):
    pass
