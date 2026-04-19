from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IRotation3D import IRotation3D

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart

# OOXML schema order for <c:view3D> children
_VIEW3D_ORDER = ['rotX', 'hPercent', 'rotY', 'depthPercent', 'rAngAx', 'perspective']

# OOXML schema order for <c:chart> children — used to place <c:view3D>
# after title/autoTitleDeleted/pivotFmts but before floor/walls/plotArea.
_CHART_CHILD_ORDER = [
    'title', 'autoTitleDeleted', 'pivotFmts', 'view3D',
    'floor', 'sideWall', 'backWall', 'plotArea',
    'legend', 'plotVisOnly', 'dispBlanksAs', 'showDLblsOverMax', 'extLst',
]


class Rotation3D(IRotation3D):
    """Represents 3D rotation of a chart."""

    @property
    def rotation_x(self) -> int:
        elem = self._view3d.find(f'{self._C}rotX')
        return int(elem.get('val', '0')) if elem is not None else 0

    @rotation_x.setter
    def rotation_x(self, value: int):
        self._set_child('rotX', None if value == 0 else str(value))

    @property
    def rotation_y(self) -> int:
        elem = self._view3d.find(f'{self._C}rotY')
        return int(elem.get('val', '0')) if elem is not None else 0

    @rotation_y.setter
    def rotation_y(self, value: int):
        self._set_child('rotY', None if value == 0 else str(value))

    @property
    def perspective(self) -> int:
        elem = self._view3d.find(f'{self._C}perspective')
        return int(elem.get('val', '30')) if elem is not None else 30

    @perspective.setter
    def perspective(self, value: int):
        tag = f'{self._C}perspective'
        elem = self._view3d.find(tag)
        if value == 30:
            # 30 is the OOXML default — remove element if present
            if elem is not None:
                self._view3d.remove(elem)
        else:
            if elem is None:
                elem = ET.Element(tag)
                target_idx = _VIEW3D_ORDER.index('perspective')
                insert_pos = 0
                for child in self._view3d:
                    child_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if child_local in _VIEW3D_ORDER:
                        if _VIEW3D_ORDER.index(child_local) < target_idx:
                            insert_pos += 1
                        else:
                            break
                    else:
                        insert_pos += 1
                self._view3d.insert(insert_pos, elem)
            elem.set('val', str(value))

    @property
    def right_angle_axes(self) -> bool:
        elem = self._view3d.find(f'{self._C}rAngAx')
        if elem is not None:
            return elem.get('val', '1') in ('1', 'true')
        return True

    @right_angle_axes.setter
    def right_angle_axes(self, value: bool):
        self._set_child('rAngAx', '1' if value else '0')

    @property
    def depth_percents(self) -> int:
        elem = self._view3d.find(f'{self._C}depthPercent')
        return int(elem.get('val', '100')) if elem is not None else 100

    @depth_percents.setter
    def depth_percents(self, value: int):
        self._remove_or_set('depthPercent', value, default=100)

    @property
    def height_percents(self) -> int:
        elem = self._view3d.find(f'{self._C}hPercent')
        return int(elem.get('val', '100')) if elem is not None else 100

    @height_percents.setter
    def height_percents(self, value: int):
        self._remove_or_set('hPercent', value, default=100)

    def _set_child(self, local_name: str, val):
        """Ensure child element exists; set val attr, or strip it when val is None
        (matches OOXML convention of emitting a bare element for default zero)."""
        tag = f'{self._C}{local_name}'
        elem = self._view3d.find(tag)
        if elem is None:
            elem = ET.Element(tag)
            target_idx = _VIEW3D_ORDER.index(local_name)
            insert_pos = 0
            for child in self._view3d:
                child_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if child_local in _VIEW3D_ORDER:
                    child_idx = _VIEW3D_ORDER.index(child_local)
                    if child_idx < target_idx:
                        insert_pos += 1
                    else:
                        break
                else:
                    insert_pos += 1
            self._view3d.insert(insert_pos, elem)
        if val is None:
            if 'val' in elem.attrib:
                del elem.attrib['val']
        else:
            elem.set('val', val)

    def _remove_or_set(self, local_name: str, value: int, default: int):
        """Remove element if value equals OOXML default; else set val."""
        tag = f'{self._C}{local_name}'
        elem = self._view3d.find(tag)
        if value == default:
            if elem is not None:
                self._view3d.remove(elem)
        else:
            self._set_child(local_name, str(value))

    def _init_internal(self, chart_part: 'ChartPart'):
        from .._internal.pptx.constants import NS
        self._chart_part = chart_part
        self._C = NS.C
        chart_elem = chart_part.get_chart_element()
        self._view3d = chart_elem.find(f'{self._C}view3D')
        if self._view3d is None:
            self._view3d = ET.Element(f'{self._C}view3D')
            target_idx = _CHART_CHILD_ORDER.index('view3D')
            insert_pos = len(chart_elem)
            for i, child in enumerate(chart_elem):
                local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if local in _CHART_CHILD_ORDER and _CHART_CHILD_ORDER.index(local) >= target_idx:
                    insert_pos = i
                    break
            chart_elem.insert(insert_pos, self._view3d)
