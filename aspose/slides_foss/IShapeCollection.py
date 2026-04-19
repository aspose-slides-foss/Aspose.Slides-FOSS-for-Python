from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IAutoShape import IAutoShape
    from .IConnector import IConnector
    from .IGroupShape import IGroupShape
    from .IPictureFrame import IPictureFrame
    from .IShape import IShape
    from .ITable import ITable

class IShapeCollection(ABC):
    """Represents a collection of shapes."""
    @property
    def parent_group(self) -> IGroupShape:
        """Gets the parent group shape object for the shapes collection. Read-only ."""
        ...

    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...


































    @overload
    def to_array(self) -> list[IShape]:
        ...

    @overload
    def to_array(self, start_index, count) -> list[IShape]:
        ...


    @overload
    def reorder(self, index, shape) -> None:
        ...

    @overload
    def reorder(self, index, shapes) -> None:
        ...


    @overload
    def add_auto_shape(self, shape_type, x, y, width, height) -> IAutoShape:
        ...

    @overload
    def add_auto_shape(self, shape_type, x, y, width, height, create_from_template) -> IAutoShape:
        ...


    @overload
    def insert_auto_shape(self, index, shape_type, x, y, width, height) -> IAutoShape:
        ...

    @overload
    def insert_auto_shape(self, index, shape_type, x, y, width, height, create_from_template) -> IAutoShape:
        ...





    @overload
    def add_connector(self, shape_type, x, y, width, height) -> IConnector:
        ...

    @overload
    def add_connector(self, shape_type, x, y, width, height, create_from_template) -> IConnector:
        ...


    @overload
    def insert_connector(self, index, shape_type, x, y, width, height) -> IConnector:
        ...

    @overload
    def insert_connector(self, index, shape_type, x, y, width, height, create_from_template) -> IConnector:
        ...

    @overload
    def add_group_shape(self) -> IGroupShape:
        ...

    @overload
    def add_group_shape(self, svg_image, x, y, width, height) -> IGroupShape:
        ...

    def add_group_shape(self, *args, **kwargs) -> IGroupShape:
        ...

    def index_of(self, shape) -> int:
        ...
    def add_picture_frame(self, shape_type, x, y, width, height, image) -> IPictureFrame:
        ...
    def insert_picture_frame(self, index, shape_type, x, y, width, height, image) -> IPictureFrame:
        ...
    def add_table(self, x, y, column_widths, row_heights) -> ITable:
        ...
    def insert_table(self, index, x, y, column_widths, row_heights) -> ITable:
        ...
    def remove_at(self, index) -> None:
        ...
    def remove(self, shape) -> None:
        ...
    def clear(self) -> None:
        ...
    def __getitem__(self, index: int) -> IShape:
        ...

