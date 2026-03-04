from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IHyperlinkContainer import IHyperlinkContainer

if TYPE_CHECKING:
    from .BlackWhiteMode import BlackWhiteMode
    from .IBaseShapeLock import IBaseShapeLock
    from .ICustomData import ICustomData
    from .IEffectFormat import IEffectFormat
    from .IFillFormat import IFillFormat
    from .IGroupShape import IGroupShape
    from .IImage import IImage
    from .ILineFormat import ILineFormat
    from .IPlaceholder import IPlaceholder
    from .IShapeFrame import IShapeFrame
    from .IThreeDFormat import IThreeDFormat

class IShape(ISlideComponent, IPresentationComponent, IHyperlinkContainer, ABC):
    """Represents a shape on a slide."""
    @property
    def is_text_holder(self) -> bool:
        """Determines whether the shape is TextHolder. Read-only ."""
        ...

    @property
    def placeholder(self) -> IPlaceholder:
        """Returns the placeholder for a shape. Read-only ."""
        ...

    @property
    def custom_data(self) -> ICustomData:
        """Returns the shape's custom data. Read-only ."""
        ...

    @property
    def raw_frame(self) -> IShapeFrame:
        """Returns or sets the raw shape frame's properties. Read/write ."""
        ...

    @raw_frame.setter
    def raw_frame(self, value: IShapeFrame):
        ...

    @property
    def frame(self) -> IShapeFrame:
        """Returns or sets the shape frame's properties. Read/write ."""
        ...

    @frame.setter
    def frame(self, value: IShapeFrame):
        ...

    @property
    def line_format(self) -> ILineFormat:
        """Returns the LineFormat object that contains line formatting properties for a shape. Read-only ."""
        ...

    @property
    def three_d_format(self) -> IThreeDFormat:
        """Returns the ThreeDFormat object that contains line formatting properties for a shape. Read-only ."""
        ...

    @property
    def effect_format(self) -> IEffectFormat:
        """Returns the EffectFormat object which contains pixel effects applied to a shape. Read-only ."""
        ...

    @property
    def fill_format(self) -> IFillFormat:
        """Returns the FillFormat object that contains fill formatting properties for a shape. Read-only ."""
        ...

    @property
    def hidden(self) -> bool:
        """Determines whether the shape is hidden. Read/write ."""
        ...

    @hidden.setter
    def hidden(self, value: bool):
        ...

    @property
    def z_order_position(self) -> int:
        """Returns the position of a shape in the z-order. Shapes[0] returns the shape at the back of the z-order, and Shapes[Shapes.Count - 1] returns the shape at the front of the z-order. Read-only ."""
        ...

    @property
    def connection_site_count(self) -> int:
        """Returns the number of connection sites on the shape. Read-only ."""
        ...

    @property
    def rotation(self) -> float:
        """Returns or sets the number of degrees the specified shape is rotated around the z-axis. A positive value indicates clockwise rotation; a negative value indicates counterclockwise rotation. Read/write ."""
        ...

    @rotation.setter
    def rotation(self, value: float):
        ...

    @property
    def x(self) -> float:
        """Gets or sets the x-coordinate of the shape's upper-left corner, measured in points. Read/write ."""
        ...

    @x.setter
    def x(self, value: float):
        ...

    @property
    def y(self) -> float:
        """Gets or sets the y-coordinate of the shape's upper-left corner, measured in points. Read/write ."""
        ...

    @y.setter
    def y(self, value: float):
        ...

    @property
    def width(self) -> float:
        """Gets or sets the width of the shape, measured in points. Read/write ."""
        ...

    @width.setter
    def width(self, value: float):
        ...

    @property
    def height(self) -> float:
        """Gets or sets the height of the shape, measured in points. Read/write ."""
        ...

    @height.setter
    def height(self, value: float):
        ...

    @property
    def alternative_text(self) -> str:
        """Returns or sets the alternative text associated with a shape. Read/write ."""
        ...

    @alternative_text.setter
    def alternative_text(self, value: str):
        ...

    @property
    def alternative_text_title(self) -> str:
        """Returns or sets the title of alternative text associated with a shape. Read/write ."""
        ...

    @alternative_text_title.setter
    def alternative_text_title(self, value: str):
        ...

    @property
    def name(self) -> str:
        """Returns or sets the name of a shape. Read/write ."""
        ...

    @name.setter
    def name(self, value: str):
        ...

    @property
    def is_decorative(self) -> bool:
        """Gets or sets 'Mark as decorative' option Reed/write ."""
        ...

    @is_decorative.setter
    def is_decorative(self, value: bool):
        ...


    @property
    def unique_id(self) -> int:
        """Returns an internal, presentation-scoped identifier intended for use by add-ins or other code. Because this value can be reassigned by the user or programmatically, it must not be treated as a persistent unique key. Read-only . See also ."""
        ...

    @property
    def office_interop_shape_id(self) -> int:
        """Returns a slide-scoped unique identifier that remains constant for the lifetime of the shape and lets PowerPoint or interop code reliably reference the shape from anywhere in the document. Read-only . See also ."""
        ...

    @property
    def is_grouped(self) -> bool:
        """Determines whether the shape is grouped. Read-only ."""
        ...





    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...










