from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .Shape import Shape
from .IGroupShape import IGroupShape
from ._internal.pptx.constants import NS

if TYPE_CHECKING:
    from .ICustomData import ICustomData
    from .IGroupShapeLock import IGroupShapeLock
    from .IPlaceholder import IPlaceholder
    from .IShapeCollection import IShapeCollection
    from .IShape import IShape
    from ._internal.pptx.slide_part import SlidePart


class GroupShape(Shape, IGroupShape):
    """Represents a group of shapes on a slide."""

    def __init__(self):
        super().__init__()
        self._child_shapes: Optional[IShapeCollection] = None

    @property
    def is_text_holder(self) -> bool:
        return False

    @property
    def placeholder(self) -> IPlaceholder:
        return None

    @property
    def custom_data(self) -> ICustomData:
        return None

    @property
    def group_shape_lock(self) -> IGroupShapeLock:
        """Returns shape's locks. Read-only ."""
        from .GroupShapeLock import GroupShapeLock
        lock = GroupShapeLock()
        if self._xml_element is not None:
            nv_grp_sp_pr = self._xml_element.find(f"{NS.P}nvGrpSpPr")
            if nv_grp_sp_pr is not None:
                cnv_grp_sp_pr = nv_grp_sp_pr.find(f"{NS.P}cNvGrpSpPr")
                if cnv_grp_sp_pr is not None:
                    lock._init_internal(cnv_grp_sp_pr, self._slide_part)
        return lock

    @property
    def shapes(self) -> IShapeCollection:
        """Returns the collection of shapes inside the group. Read-only ."""
        if self._child_shapes is None:
            from .ShapeCollection import ShapeCollection
            coll = ShapeCollection()
            coll._init_internal_group(self._xml_element, self._slide_part, self._parent_slide, self)
            self._child_shapes = coll
        return self._child_shapes

    @property
    def as_i_shape(self) -> IShape:
        """Allows to get base IShape interface. Read-only ."""
        return self
