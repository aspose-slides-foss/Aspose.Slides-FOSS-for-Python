from __future__ import annotations
from typing import TYPE_CHECKING, Any
import lxml.etree as ET
from .Behavior import Behavior
from .IBehavior import IBehavior
from .IMotionEffect import IMotionEffect
from .._internal.pptx.constants import Elements

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from .IMotionPath import IMotionPath
    from .ITiming import ITiming
    from .MotionOriginType import MotionOriginType
    from .MotionPathEditMode import MotionPathEditMode
    from ..NullableBool import NullableBool


class MotionEffect(Behavior, IMotionEffect):
    """Represent motion effect behavior of effect."""

    def __init__(self):
        self._path_cache = None

    def _init_internal(self, elem: ET._Element):
        super()._init_internal(elem)
        self._path_cache = None

    def _parse_path_string(self, path_str: str):
        """Parse SVG-like path string into MotionPath commands."""
        from .MotionPath import MotionPath
        from .MotionCmdPath import MotionCmdPath
        from .MotionCommandPathType import MotionCommandPathType
        from .MotionPathPointsType import MotionPathPointsType
        from ...slides_foss.drawing import PointF

        mp = MotionPath()
        mp._init_internal(self)

        if not path_str:
            return mp

        # Tokenize: split on whitespace, but also split comma-joined pairs
        raw_tokens = path_str.strip().split()
        tokens = []
        for rt in raw_tokens:
            if ',' in rt and rt[0] not in 'MmLlCcZzEe':
                # Split "0.076,0.59" into two tokens
                tokens.extend(rt.split(','))
            else:
                tokens.append(rt)

        def _is_number(s):
            try:
                float(s)
                return True
            except (ValueError, IndexError):
                return False

        def _read_points(idx):
            """Read consecutive number pairs as PointF list."""
            pts = []
            while idx < len(tokens) and _is_number(tokens[idx]):
                x = float(tokens[idx])
                if idx + 1 < len(tokens) and _is_number(tokens[idx + 1]):
                    y = float(tokens[idx + 1])
                    pts.append(PointF(x, y))
                    idx += 2
                else:
                    break
            return pts, idx

        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.upper() == 'M':
                i += 1
                pts, i = _read_points(i)
                cmd = MotionCmdPath()
                cmd._init_internal(MotionCommandPathType.MOVE_TO, pts, MotionPathPointsType.AUTO, t == 'm')
                mp._commands.append(cmd)
            elif t.upper() == 'L':
                i += 1
                pts, i = _read_points(i)
                cmd = MotionCmdPath()
                cmd._init_internal(MotionCommandPathType.LINE_TO, pts, MotionPathPointsType.AUTO, t == 'l')
                mp._commands.append(cmd)
            elif t.upper() == 'C':
                i += 1
                pts, i = _read_points(i)
                cmd = MotionCmdPath()
                cmd._init_internal(MotionCommandPathType.CURVE_TO, pts, MotionPathPointsType.AUTO, t == 'c')
                mp._commands.append(cmd)
            elif t.upper() == 'Z':
                cmd = MotionCmdPath()
                cmd._init_internal(MotionCommandPathType.CLOSE_LOOP, [], MotionPathPointsType.AUTO, False)
                mp._commands.append(cmd)
                i += 1
            elif t.upper() == 'E':
                cmd = MotionCmdPath()
                cmd._init_internal(MotionCommandPathType.END, [], MotionPathPointsType.AUTO, False)
                mp._commands.append(cmd)
                i += 1
            else:
                i += 1

        return mp

    def _path_to_string(self) -> str:
        """Serialize MotionPath commands to SVG-like path string."""
        from .MotionCommandPathType import MotionCommandPathType

        if self._path_cache is None:
            return ''

        parts = []
        for cmd in self._path_cache._commands:
            if cmd.command_type == MotionCommandPathType.MOVE_TO:
                letter = 'm' if cmd.is_relative else 'M'
                pts_str = ' '.join(f'{p.x} {p.y}' for p in cmd.points)
                parts.append(f'{letter} {pts_str}' if pts_str else letter)
            elif cmd.command_type == MotionCommandPathType.LINE_TO:
                letter = 'l' if cmd.is_relative else 'L'
                pts_str = ' '.join(f'{p.x} {p.y}' for p in cmd.points)
                parts.append(f'{letter} {pts_str}' if pts_str else letter)
            elif cmd.command_type == MotionCommandPathType.CURVE_TO:
                letter = 'c' if cmd.is_relative else 'C'
                pts_str = ' '.join(f'{p.x} {p.y}' for p in cmd.points)
                parts.append(f'{letter} {pts_str}' if pts_str else letter)
            elif cmd.command_type == MotionCommandPathType.CLOSE_LOOP:
                parts.append('Z')
            elif cmd.command_type == MotionCommandPathType.END:
                parts.append('E')
        return ' '.join(parts)

    def _sync_path_to_xml(self):
        """Write the current path back to the XML element."""
        self._elem.set('path', self._path_to_string())

    @property
    def from_address(self) -> Any:
        return self._elem.get('from')

    @from_address.setter
    def from_address(self, value: Any):
        if value is not None:
            self._elem.set('from', str(value))
        elif 'from' in self._elem.attrib:
            del self._elem.attrib['from']

    @property
    def to(self) -> Any:
        return self._elem.get('to')

    @to.setter
    def to(self, value: Any):
        if value is not None:
            self._elem.set('to', str(value))
        elif 'to' in self._elem.attrib:
            del self._elem.attrib['to']

    @property
    def by(self) -> Any:
        return self._elem.get('by')

    @by.setter
    def by(self, value: Any):
        if value is not None:
            self._elem.set('by', str(value))
        elif 'by' in self._elem.attrib:
            del self._elem.attrib['by']

    @property
    def rotation_center(self) -> Any:
        return self._elem.get('rCtr')

    @rotation_center.setter
    def rotation_center(self, value: Any):
        if value is not None:
            self._elem.set('rCtr', str(value))
        elif 'rCtr' in self._elem.attrib:
            del self._elem.attrib['rCtr']

    @property
    def origin(self) -> MotionOriginType:
        from .MotionOriginType import MotionOriginType
        val = self._elem.get('origin')
        _map = {'parent': MotionOriginType.PARENT, 'layout': MotionOriginType.LAYOUT}
        return _map.get(val, MotionOriginType.NOT_DEFINED)

    @origin.setter
    def origin(self, value: MotionOriginType):
        from .MotionOriginType import MotionOriginType
        _map = {MotionOriginType.PARENT: 'parent', MotionOriginType.LAYOUT: 'layout'}
        xml_val = _map.get(value)
        if xml_val:
            self._elem.set('origin', xml_val)
        elif 'origin' in self._elem.attrib:
            del self._elem.attrib['origin']

    @property
    def path(self) -> IMotionPath:
        if self._path_cache is None:
            path_str = self._elem.get('path', '')
            self._path_cache = self._parse_path_string(path_str)
        return self._path_cache

    @path.setter
    def path(self, value: IMotionPath):
        self._path_cache = value
        if hasattr(value, '_owner'):
            value._owner = self
        self._sync_path_to_xml()

    @property
    def path_edit_mode(self) -> MotionPathEditMode:
        from .MotionPathEditMode import MotionPathEditMode
        val = self._elem.get('pathEditMode')
        _map = {'relative': MotionPathEditMode.RELATIVE, 'fixed': MotionPathEditMode.FIXED}
        return _map.get(val, MotionPathEditMode.NOT_DEFINED)

    @path_edit_mode.setter
    def path_edit_mode(self, value: MotionPathEditMode):
        from .MotionPathEditMode import MotionPathEditMode
        _map = {MotionPathEditMode.RELATIVE: 'relative', MotionPathEditMode.FIXED: 'fixed'}
        xml_val = _map.get(value)
        if xml_val:
            self._elem.set('pathEditMode', xml_val)

    @property
    def angle(self) -> float:
        val = self._elem.get('ang')
        if val is not None:
            return int(val) / 60000.0
        return 0.0

    @angle.setter
    def angle(self, value: float):
        self._elem.set('ang', str(int(value * 60000)))

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
