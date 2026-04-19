from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .MotionCommandPathType import MotionCommandPathType
    from .MotionPathPointsType import MotionPathPointsType

class IMotionCmdPath(ABC):
    """Represent one command of a path."""
    @property
    @abstractmethod
    def points(self) -> list[Any]:
        """Specifies points of command. Read/write []."""
        ...
    @points.setter
    @abstractmethod
    def points(self, value: list[Any]):
        ...
    @property
    @abstractmethod
    def command_type(self) -> MotionCommandPathType:
        """Specifies command type. Read/write ."""
        ...
    @command_type.setter
    @abstractmethod
    def command_type(self, value: MotionCommandPathType):
        ...
    @property
    @abstractmethod
    def is_relative(self) -> bool:
        """Determine command coordinates relative or not. Read/write ."""
        ...
    @is_relative.setter
    @abstractmethod
    def is_relative(self, value: bool):
        ...
    @property
    @abstractmethod
    def points_type(self) -> MotionPathPointsType:
        """Specifies command points type Read/write ."""
        ...
    @points_type.setter
    @abstractmethod
    def points_type(self, value: MotionPathPointsType):
        ...