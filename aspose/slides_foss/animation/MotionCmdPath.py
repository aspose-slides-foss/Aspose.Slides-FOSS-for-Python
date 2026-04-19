from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IMotionCmdPath import IMotionCmdPath

if TYPE_CHECKING:
    from .MotionCommandPathType import MotionCommandPathType
    from .MotionPathPointsType import MotionPathPointsType


class MotionCmdPath(IMotionCmdPath):
    """Represent one command of a path."""

    def _init_internal(self, command_type, points, points_type, is_relative):
        from .MotionCommandPathType import MotionCommandPathType
        from .MotionPathPointsType import MotionPathPointsType
        self._command_type = command_type
        self._points = points if points is not None else []
        self._points_type = points_type
        self._is_relative = is_relative

    @property
    def points(self) -> list[Any]:
        return self._points

    @points.setter
    def points(self, value: list[Any]):
        self._points = value

    @property
    def command_type(self) -> MotionCommandPathType:
        return self._command_type

    @command_type.setter
    def command_type(self, value: MotionCommandPathType):
        self._command_type = value

    @property
    def is_relative(self) -> bool:
        return self._is_relative

    @is_relative.setter
    def is_relative(self, value: bool):
        self._is_relative = value

    @property
    def points_type(self) -> MotionPathPointsType:
        return self._points_type

    @points_type.setter
    def points_type(self, value: MotionPathPointsType):
        self._points_type = value
