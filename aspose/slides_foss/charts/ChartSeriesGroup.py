from __future__ import annotations
from typing import TYPE_CHECKING
from .IChartSeriesGroup import IChartSeriesGroup

if TYPE_CHECKING:
    from .CombinableSeriesTypesGroup import CombinableSeriesTypesGroup
    from .IChartSeriesReadonlyCollection import IChartSeriesReadonlyCollection
    from .._internal.pptx.chart_part import ChartPart

# ---- XML element local names for series-group properties ----
_PROP_MAP = {
    'gapWidth': int,
    'overlap': int,
    'gapDepth': int,
    'firstSliceAng': int,
    'holeSize': int,
    'varyColors': bool,
    'secondPieSize': int,
    'splitType': str,
    'splitPos': float,
    'bubbleScale': int,
    'bubble3D': bool,
}


class ChartSeriesGroup(IChartSeriesGroup):
    """Represents group of series.

    In OOXML, a series group corresponds to a chart-type element inside
    ``<c:plotArea>`` (e.g. ``<c:barChart>``).  All ``<c:ser>`` children
    share the group-level properties like *gapWidth*, *overlap*, etc.
    """

    # -- public read-only properties --

    @property
    def type(self) -> CombinableSeriesTypesGroup:
        return self._combinable_type

    @property
    def plot_on_second_axis(self) -> bool:
        return self._plot_on_second_axis

    @property
    def series(self) -> IChartSeriesReadonlyCollection:
        return self._series_readonly

    # -- gap_width --

    @property
    def gap_width(self) -> int:
        return self._read_int('gapWidth', 150)

    @gap_width.setter
    def gap_width(self, value: int):
        self._write_val('gapWidth', str(value))

    # -- overlap --

    @property
    def overlap(self) -> int:
        return self._read_int('overlap', 0)

    @overlap.setter
    def overlap(self, value: int):
        self._write_val('overlap', str(value))

    # -- gap_depth --

    @property
    def gap_depth(self) -> int:
        return self._read_int('gapDepth', 150)

    @gap_depth.setter
    def gap_depth(self, value: int):
        self._write_val('gapDepth', str(value))

    # -- first_slice_angle --

    @property
    def first_slice_angle(self) -> int:
        return self._read_int('firstSliceAng', 0)

    @first_slice_angle.setter
    def first_slice_angle(self, value: int):
        self._write_val('firstSliceAng', str(value))

    # -- doughnut_hole_size --

    @property
    def doughnut_hole_size(self) -> int:
        return self._read_int('holeSize', 50)

    @doughnut_hole_size.setter
    def doughnut_hole_size(self, value: int):
        self._write_val('holeSize', str(value))

    # -- is_color_varied --

    @property
    def is_color_varied(self) -> bool:
        return self._read_bool('varyColors', False)

    @is_color_varied.setter
    def is_color_varied(self, value: bool):
        self._write_val('varyColors', '1' if value else '0')

    # -- has_series_lines --

    @property
    def has_series_lines(self) -> bool:
        from .._internal.pptx.constants import NS
        el = self._ct_elem.find(f'{NS.C}serLines')
        return el is not None

    @has_series_lines.setter
    def has_series_lines(self, value: bool):
        import lxml.etree as ET
        from .._internal.pptx.constants import NS
        existing = self._ct_elem.find(f'{NS.C}serLines')
        if value and existing is None:
            ET.SubElement(self._ct_elem, f'{NS.C}serLines')
        elif not value and existing is not None:
            self._ct_elem.remove(existing)

    # -- overlap --
    # (already defined above)

    # -- second_pie_size --

    @property
    def second_pie_size(self) -> int:
        return self._read_int('secondPieSize', 75)

    @second_pie_size.setter
    def second_pie_size(self, value: int):
        self._write_val('secondPieSize', str(value))

    # -- pie_split_position --

    @property
    def pie_split_position(self) -> float:
        return self._read_float('splitPos', 0.0)

    @pie_split_position.setter
    def pie_split_position(self, value: float):
        self._write_val('splitPos', str(value))

    # -- pie_split_by --

    @property
    def pie_split_by(self):
        from .PieSplitType import PieSplitType
        raw = self._read_str('splitType', 'auto')
        _map = {
            'auto': PieSplitType.DEFAULT,
            'pos': PieSplitType.BY_POS,
            'val': PieSplitType.BY_VALUE,
            'percent': PieSplitType.BY_PERCENTAGE,
            'cust': PieSplitType.CUSTOM,
        }
        return _map.get(raw, PieSplitType.DEFAULT)

    @pie_split_by.setter
    def pie_split_by(self, value):
        from .PieSplitType import PieSplitType
        _map = {
            PieSplitType.DEFAULT: 'auto',
            PieSplitType.BY_POS: 'pos',
            PieSplitType.BY_VALUE: 'val',
            PieSplitType.BY_PERCENTAGE: 'percent',
            PieSplitType.CUSTOM: 'cust',
        }
        self._write_val('splitType', _map.get(value, 'auto'))

    # -- bubble_size_scale --

    @property
    def bubble_size_scale(self) -> int:
        return self._read_int('bubbleScale', 100)

    @bubble_size_scale.setter
    def bubble_size_scale(self, value: int):
        self._write_val('bubbleScale', str(value))

    # -- bubble_size_representation --

    @property
    def bubble_size_representation(self):
        from .BubbleSizeRepresentationType import BubbleSizeRepresentationType
        raw = self._read_str('sizeRepresents', 'area')
        if raw == 'w':
            return BubbleSizeRepresentationType.WIDTH
        return BubbleSizeRepresentationType.AREA

    @bubble_size_representation.setter
    def bubble_size_representation(self, value):
        from .BubbleSizeRepresentationType import BubbleSizeRepresentationType
        xml_val = 'w' if value == BubbleSizeRepresentationType.WIDTH else 'area'
        self._write_val('sizeRepresents', xml_val)

    # ---- internal init ----

    def _init_internal(self, ct_elem, chart_part: 'ChartPart',
                       combinable_type: 'CombinableSeriesTypesGroup',
                       series_list: list,
                       plot_on_second_axis: bool = False):
        """
        Args:
            ct_elem: The chart-type XML element (e.g. <c:barChart>).
            chart_part: Parent ChartPart for save coordination.
            combinable_type: The CombinableSeriesTypesGroup enum value.
            series_list: List of ChartSeries objects belonging to this group.
            plot_on_second_axis: Whether this group plots on secondary axis.
        """
        self._ct_elem = ct_elem
        self._chart_part = chart_part
        self._combinable_type = combinable_type
        self._plot_on_second_axis = plot_on_second_axis

        # Build readonly series view
        from .ChartSeriesReadonlyCollection import ChartSeriesReadonlyCollection
        self._series_readonly = ChartSeriesReadonlyCollection()
        self._series_readonly._init_internal(series_list)

        # Back-link each series to this group
        for s in series_list:
            s._parent_series_group = self

    def _update_series(self, series_list: list):
        """Replace the series list without recreating the group object.

        Called during rebuild to refresh membership while preserving the
        group identity and all XML-backed properties.
        """
        self._series_readonly._series = list(series_list)
        for s in series_list:
            s._parent_series_group = self

    # ---- XML helpers ----

    def _read_int(self, local_name: str, default: int) -> int:
        from .._internal.pptx.constants import NS
        el = self._ct_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            try:
                return int(el.get('val', str(default)))
            except (ValueError, TypeError):
                return default
        return default

    def _read_float(self, local_name: str, default: float) -> float:
        from .._internal.pptx.constants import NS
        el = self._ct_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            try:
                return float(el.get('val', str(default)))
            except (ValueError, TypeError):
                return default
        return default

    def _read_bool(self, local_name: str, default: bool) -> bool:
        from .._internal.pptx.constants import NS
        el = self._ct_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            val = el.get('val', '1' if default else '0')
            return val in ('1', 'true')
        return default

    def _read_str(self, local_name: str, default: str) -> str:
        from .._internal.pptx.constants import NS
        el = self._ct_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            return el.get('val', default)
        return default

    def _write_val(self, local_name: str, value: str):
        import lxml.etree as ET
        from .._internal.pptx.constants import NS
        el = self._ct_elem.find(f'{NS.C}{local_name}')
        if el is None:
            el = ET.SubElement(self._ct_elem, f'{NS.C}{local_name}')
        el.set('val', value)
