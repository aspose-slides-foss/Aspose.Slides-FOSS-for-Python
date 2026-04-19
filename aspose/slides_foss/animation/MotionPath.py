from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IMotionPath import IMotionPath

if TYPE_CHECKING:
    from .IMotionCmdPath import IMotionCmdPath


class MotionPath(IMotionPath):
    """Represent motion path."""

    def __init__(self):
        self._commands: list = []
        self._owner = None  # MotionEffect that owns this path

    def _init_internal(self, owner=None):
        self._owner = owner

    @property
    def count(self) -> int:
        return len(self._commands)

    @property
    def as_i_enumerable(self) -> Any:
        return iter(self._commands)

    def add(self, type, pts, pts_type, b_relative_coord) -> IMotionCmdPath:
        from .MotionCmdPath import MotionCmdPath
        cmd = MotionCmdPath()
        cmd._init_internal(type, pts, pts_type, b_relative_coord)
        self._commands.append(cmd)
        if self._owner is not None:
            self._owner._sync_path_to_xml()
        return cmd

    def insert(self, index, type, pts, pts_type, b_relative_coord) -> None:
        from .MotionCmdPath import MotionCmdPath
        cmd = MotionCmdPath()
        cmd._init_internal(type, pts, pts_type, b_relative_coord)
        self._commands.insert(index, cmd)
        if self._owner is not None:
            self._owner._sync_path_to_xml()

    def clear(self) -> None:
        self._commands.clear()
        if self._owner is not None:
            self._owner._sync_path_to_xml()

    def remove(self, item) -> None:
        self._commands.remove(item)
        if self._owner is not None:
            self._owner._sync_path_to_xml()

    def remove_at(self, index) -> None:
        del self._commands[index]
        if self._owner is not None:
            self._owner._sync_path_to_xml()

    def __getitem__(self, index: int) -> IMotionCmdPath:
        return self._commands[index]

    def __len__(self):
        return len(self._commands)

    def __iter__(self):
        return iter(self._commands)
