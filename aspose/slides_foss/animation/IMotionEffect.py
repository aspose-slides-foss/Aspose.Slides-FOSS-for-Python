from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .IMotionPath import IMotionPath
    from .ITiming import ITiming
    from .MotionOriginType import MotionOriginType
    from .MotionPathEditMode import MotionPathEditMode
    from ..NullableBool import NullableBool

class IMotionEffect(IBehavior, ABC):
    """Represent motion effect behavior of effect."""
    @property
    @abstractmethod
    def from_address(self) -> Any:
        """Specifies an x/y co-ordinate to start the animation from (in percents). Read/write ."""
        ...
    @from_address.setter
    @abstractmethod
    def from_address(self, value: Any):
        ...
    @property
    @abstractmethod
    def to(self) -> Any:
        """Specifies the target location for an animation motion effect (in percents). Read/write ."""
        ...
    @to.setter
    @abstractmethod
    def to(self, value: Any):
        ...
    @property
    @abstractmethod
    def by(self) -> Any:
        """Describes the relative offset value for the animation (in percents). Read/write ."""
        ...
    @by.setter
    @abstractmethod
    def by(self, value: Any):
        ...
    @property
    @abstractmethod
    def rotation_center(self) -> Any:
        """Describes the center of the rotation used to rotate a motion path by X angle. Read/write ."""
        ...
    @rotation_center.setter
    @abstractmethod
    def rotation_center(self, value: Any):
        ...
    @property
    @abstractmethod
    def origin(self) -> MotionOriginType:
        """Specifies what the origin of the motion path is relative to such as the layout of the slide, or the parent. Read/write ."""
        ...
    @origin.setter
    @abstractmethod
    def origin(self, value: MotionOriginType):
        ...
    @property
    @abstractmethod
    def path(self) -> IMotionPath:
        """Specifies the path primitive followed by coordinates for the animation motion. Read/write ."""
        ...
    @path.setter
    @abstractmethod
    def path(self, value: IMotionPath):
        ...
    @property
    @abstractmethod
    def path_edit_mode(self) -> MotionPathEditMode:
        """Specifies how the motion path moves when shape is moved. Read/write ."""
        ...
    @path_edit_mode.setter
    @abstractmethod
    def path_edit_mode(self, value: MotionPathEditMode):
        ...
    @property
    @abstractmethod
    def angle(self) -> float:
        """Describes the relative angle of the motion path. Read/write ."""
        ...
    @angle.setter
    @abstractmethod
    def angle(self, value: float):
        ...
    @property
    @abstractmethod
    def as_i_behavior(self) -> IBehavior:
        """Allows to get base IBehavior interface. Read-only ."""
        ...
    @property
    @abstractmethod
    def accumulate(self) -> NullableBool:
        ...
    @accumulate.setter
    @abstractmethod
    def accumulate(self, value: NullableBool):
        ...
    @property
    @abstractmethod
    def additive(self) -> BehaviorAdditiveType:
        ...
    @additive.setter
    @abstractmethod
    def additive(self, value: BehaviorAdditiveType):
        ...
    @property
    @abstractmethod
    def properties(self) -> IBehaviorPropertyCollection:
        ...
    @property
    @abstractmethod
    def timing(self) -> ITiming:
        ...
    @timing.setter
    @abstractmethod
    def timing(self, value: ITiming):
        ...