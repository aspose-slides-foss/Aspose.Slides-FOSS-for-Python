from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IGradientStopCollection import IGradientStopCollection
from ._internal.pptx.constants import Elements

if TYPE_CHECKING:
    from .GradientStop import GradientStop
    from .IGradientStop import IGradientStop
    from ._internal.pptx.slide_part import SlidePart


from ._internal.base_collection import BaseCollection
class GradientStopCollection(PVIObject, ISlideComponent, IPresentationComponent, IGradientStopCollection):
    """Represnts a collection of gradient stops."""

    def _init_internal(self, gs_lst_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._gs_lst = gs_lst_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def as_i_collection(self) -> list:
        if not hasattr(self, '_gs_lst'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return [self[i] for i in range(len(self))]

    @property
    def as_i_enumerable(self) -> Any:
        return self.as_i_collection

    def __len__(self) -> int:
        if not hasattr(self, '_gs_lst'):
            return 0
        return len(self._gs_lst.findall(Elements.A_GS))

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]




    def add(self, *args, **kwargs) -> IGradientStop:
        if not hasattr(self, '_gs_lst'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .GradientStop import GradientStop as GradientStopClass
        from .ColorFormat import ColorFormat

        position = args[0]
        color_arg = args[1]

        pos_val = str(int(round(position * 100000)))
        gs_elem = ET.SubElement(self._gs_lst, Elements.A_GS, pos=pos_val)

        # Determine color type and set accordingly
        cf = ColorFormat()
        cf._init_internal(gs_elem, self._slide_part, self._parent_slide)
        self._set_color_from_arg(cf, color_arg)

        self._save()

        stop = GradientStopClass()
        stop._init_internal(gs_elem, self._slide_part, self._parent_slide)
        return stop

    def _set_color_from_arg(self, cf, color_arg) -> None:
        """Set color on ColorFormat from various argument types."""
        from .PresetColor import PresetColor
        from .SchemeColor import SchemeColor
        from .drawing import Color
        if isinstance(color_arg, Color):
            cf.color = color_arg
        elif isinstance(color_arg, PresetColor):
            cf.preset_color = color_arg
        elif isinstance(color_arg, SchemeColor):
            cf.scheme_color = color_arg




    def insert(self, *args, **kwargs) -> None:
        if not hasattr(self, '_gs_lst'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColorFormat import ColorFormat

        index = args[0]
        position = args[1]
        color_arg = args[2]

        pos_val = str(int(round(position * 100000)))
        gs_elem = ET.Element(Elements.A_GS, pos=pos_val)

        cf = ColorFormat()
        cf._init_internal(gs_elem, self._slide_part, self._parent_slide)
        self._set_color_from_arg(cf, color_arg)

        gs_elements = self._gs_lst.findall(Elements.A_GS)
        if index >= len(gs_elements):
            self._gs_lst.append(gs_elem)
        else:
            self._gs_lst.insert(list(self._gs_lst).index(gs_elements[index]), gs_elem)
        self._save()

    def remove_at(self, index) -> None:
        if not hasattr(self, '_gs_lst'):
            raise NotImplementedError("This feature is not yet available in this version.")
        gs_elements = self._gs_lst.findall(Elements.A_GS)
        if 0 <= index < len(gs_elements):
            self._gs_lst.remove(gs_elements[index])
            self._save()

    def clear(self) -> None:
        if not hasattr(self, '_gs_lst'):
            raise NotImplementedError("This feature is not yet available in this version.")
        for gs in list(self._gs_lst.findall(Elements.A_GS)):
            self._gs_lst.remove(gs)
        self._save()

    def __getitem__(self, index: int) -> GradientStop:
        if not hasattr(self, '_gs_lst'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .GradientStop import GradientStop as GradientStopClass
        gs_elements = self._gs_lst.findall(Elements.A_GS)
        if index < 0 or index >= len(gs_elements):
            raise IndexError(f"Index {index} out of range")
        stop = GradientStopClass()
        stop._init_internal(gs_elements[index], self._slide_part, self._parent_slide)
        return stop
