from __future__ import annotations
from abc import ABC, abstractmethod
from .IBaseShapeLock import IBaseShapeLock

class IGroupShapeLock(IBaseShapeLock, ABC):
    """Determines which operations are disabled on the parent GroupShape."""
    @property
    @abstractmethod
    def grouping_locked(self) -> bool:
        """Determines whether adding this shape to a group is forbidden. Read/write ."""
        ...

    @grouping_locked.setter
    @abstractmethod
    def grouping_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def ungrouping_locked(self) -> bool:
        """Determines whether splitting this groupshape is forbidden. Read/write ."""
        ...

    @ungrouping_locked.setter
    @abstractmethod
    def ungrouping_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def select_locked(self) -> bool:
        """Determines whether selecting this shape is forbidden. Read/write ."""
        ...

    @select_locked.setter
    @abstractmethod
    def select_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def rotation_locked(self) -> bool:
        """Determines whether changing rotation angle of this shape is forbidden. Read/write ."""
        ...

    @rotation_locked.setter
    @abstractmethod
    def rotation_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def aspect_ratio_locked(self) -> bool:
        """Determines whether shape have to preserve aspect ratio on resizing. Read/write ."""
        ...

    @aspect_ratio_locked.setter
    @abstractmethod
    def aspect_ratio_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def position_locked(self) -> bool:
        """Determines whether moving this shape is forbidden. Read/write ."""
        ...

    @position_locked.setter
    @abstractmethod
    def position_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def size_locked(self) -> bool:
        """Determines whether resizing this shape is forbidden. Read/write ."""
        ...

    @size_locked.setter
    @abstractmethod
    def size_locked(self, value: bool):
        ...

    @property
    @abstractmethod
    def as_i_base_shape_lock(self) -> IBaseShapeLock:
        """Allows to get base IBaseShapeLock interface. Read-only ."""
        ...
