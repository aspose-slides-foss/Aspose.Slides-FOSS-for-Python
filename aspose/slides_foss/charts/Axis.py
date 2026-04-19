from __future__ import annotations
from typing import TYPE_CHECKING
from .IAxis import IAxis

if TYPE_CHECKING:
    from .AxisPositionType import AxisPositionType
    from .CategoryAxisType import CategoryAxisType
    from .CrossesType import CrossesType
    from .DisplayUnitType import DisplayUnitType
    from .TickLabelPositionType import TickLabelPositionType
    from .TickMarkType import TickMarkType
    from .TimeUnitType import TimeUnitType
    from .._internal.pptx.chart_part import ChartPart


class Axis(IAxis):
    """Encapsulates the object that represents a chart's axis."""

    # ------------------------------------------------------------------ #
    #  axis_between_categories
    # ------------------------------------------------------------------ #

    @property
    def axis_between_categories(self) -> bool:
        return self._read_bool('crossBetween', True, default_missing=True)

    @axis_between_categories.setter
    def axis_between_categories(self, value: bool):
        self._write_val('crossBetween', 'between' if value else 'midCat')

    # ------------------------------------------------------------------ #
    #  category_axis_type
    # ------------------------------------------------------------------ #

    @property
    def category_axis_type(self) -> CategoryAxisType:
        from .CategoryAxisType import CategoryAxisType
        tag = self._ax_elem.tag.split('}')[-1] if '}' in self._ax_elem.tag else self._ax_elem.tag
        if tag == 'dateAx':
            return CategoryAxisType.DATE
        return CategoryAxisType.TEXT

    @category_axis_type.setter
    def category_axis_type(self, value: CategoryAxisType):
        # Category axis type is determined by the XML element tag (catAx vs dateAx).
        # Changing it would require replacing the element — not supported as a simple setter.
        pass

    def set_category_axis_type_automatically(self) -> None:
        pass

    # ------------------------------------------------------------------ #
    #  cross_type / cross_at
    # ------------------------------------------------------------------ #

    @property
    def cross_type(self) -> CrossesType:
        from .CrossesType import CrossesType
        perp = self._get_perpendicular_ax_elem()
        if perp is None:
            return CrossesType.AXIS_CROSSES_AT_ZERO
        from .._internal.pptx.constants import NS
        crosses = perp.find(f'{NS.C}crosses')
        if crosses is not None:
            val = crosses.get('val', 'autoZero')
            if val == 'max':
                return CrossesType.MAXIMUM
            if val == 'autoZero':
                return CrossesType.AXIS_CROSSES_AT_ZERO
        crosses_at = perp.find(f'{NS.C}crossesAt')
        if crosses_at is not None:
            return CrossesType.CUSTOM
        return CrossesType.AXIS_CROSSES_AT_ZERO

    @cross_type.setter
    def cross_type(self, value: CrossesType):
        from .CrossesType import CrossesType
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        perp = self._get_perpendicular_ax_elem()
        if perp is None:
            return
        # Remove both <c:crosses> and <c:crossesAt> on the perpendicular axis
        for tag in ('crosses', 'crossesAt'):
            el = perp.find(f'{NS.C}{tag}')
            if el is not None:
                perp.remove(el)
        if value == CrossesType.MAXIMUM:
            el = ET.SubElement(perp, f'{NS.C}crosses')
            el.set('val', 'max')
        elif value == CrossesType.CUSTOM:
            el = ET.SubElement(perp, f'{NS.C}crossesAt')
            el.set('val', '0')
        else:
            el = ET.SubElement(perp, f'{NS.C}crosses')
            el.set('val', 'autoZero')

    @property
    def cross_at(self) -> float:
        from .._internal.pptx.constants import NS
        perp = self._get_perpendicular_ax_elem()
        if perp is not None:
            el = perp.find(f'{NS.C}crossesAt')
            if el is not None:
                try:
                    return float(el.get('val', '0'))
                except (ValueError, TypeError):
                    pass
        return 0.0

    @cross_at.setter
    def cross_at(self, value: float):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        perp = self._get_perpendicular_ax_elem()
        if perp is None:
            return
        # Remove <c:crosses> and set <c:crossesAt> on perpendicular axis
        crosses = perp.find(f'{NS.C}crosses')
        if crosses is not None:
            perp.remove(crosses)
        el = perp.find(f'{NS.C}crossesAt')
        if el is None:
            el = ET.SubElement(perp, f'{NS.C}crossesAt')
        el.set('val', _format_num(value))

    # ------------------------------------------------------------------ #
    #  display_unit
    # ------------------------------------------------------------------ #

    _DISPLAY_UNIT_MAP = {
        'hundreds': 'Hundreds',
        'thousands': 'Thousands',
        'tenThousands': 'TenThousands',
        'hundredThousands': 'HundredThousands',
        'millions': 'Millions',
        'tenMillions': 'TenMillions',
        'hundredMillions': 'HundredMillions',
        'billions': 'Billions',
        'trillions': 'Trillions',
    }

    _DISPLAY_UNIT_MAP_REV = {v: k for k, v in _DISPLAY_UNIT_MAP.items()}

    @property
    def display_unit(self) -> DisplayUnitType:
        from .DisplayUnitType import DisplayUnitType
        from .._internal.pptx.constants import NS
        disp = self._ax_elem.find(f'{NS.C}dispUnits')
        if disp is not None:
            bu = disp.find(f'{NS.C}builtInUnit')
            if bu is not None:
                val = bu.get('val', '')
                enum_val = self._DISPLAY_UNIT_MAP.get(val)
                if enum_val:
                    return DisplayUnitType(enum_val)
            cu = disp.find(f'{NS.C}custUnit')
            if cu is not None:
                return DisplayUnitType.CUSTOM_VALUE
        return DisplayUnitType.NONE

    @display_unit.setter
    def display_unit(self, value: DisplayUnitType):
        from .DisplayUnitType import DisplayUnitType
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        existing = self._ax_elem.find(f'{NS.C}dispUnits')
        if value == DisplayUnitType.NONE:
            if existing is not None:
                self._ax_elem.remove(existing)
            return
        if existing is None:
            existing = ET.SubElement(self._ax_elem, f'{NS.C}dispUnits')
        # Clear children
        for child in list(existing):
            existing.remove(child)
        xml_val = self._DISPLAY_UNIT_MAP_REV.get(value.value)
        if xml_val:
            bu = ET.SubElement(existing, f'{NS.C}builtInUnit')
            bu.set('val', xml_val)

    # ------------------------------------------------------------------ #
    #  max_value / min_value (and is_automatic variants)
    # ------------------------------------------------------------------ #

    @property
    def max_value(self) -> float:
        return self._read_scaling_val('max', 10.0)

    @max_value.setter
    def max_value(self, value: float):
        self._write_scaling_val('max', value)
        self._set_auto_scaling('max', False)

    @property
    def is_automatic_max_value(self) -> bool:
        return self._is_auto_scaling('max')

    @is_automatic_max_value.setter
    def is_automatic_max_value(self, value: bool):
        self._set_auto_scaling('max', value)

    @property
    def min_value(self) -> float:
        return self._read_scaling_val('min', 0.0)

    @min_value.setter
    def min_value(self, value: float):
        self._write_scaling_val('min', value)
        self._set_auto_scaling('min', False)

    @property
    def is_automatic_min_value(self) -> bool:
        return self._is_auto_scaling('min')

    @is_automatic_min_value.setter
    def is_automatic_min_value(self, value: bool):
        self._set_auto_scaling('min', value)

    # ------------------------------------------------------------------ #
    #  major_unit / minor_unit (and is_automatic variants)
    # ------------------------------------------------------------------ #

    @property
    def major_unit(self) -> float:
        return self._read_simple_float('majorUnit', 1.0)

    @major_unit.setter
    def major_unit(self, value: float):
        self._write_simple_val('majorUnit', _format_num(value))

    @property
    def is_automatic_major_unit(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}majorUnit') is None

    @is_automatic_major_unit.setter
    def is_automatic_major_unit(self, value: bool):
        if value:
            self._remove_elem('majorUnit')

    @property
    def minor_unit(self) -> float:
        return self._read_simple_float('minorUnit', 0.2)

    @minor_unit.setter
    def minor_unit(self, value: float):
        self._write_simple_val('minorUnit', _format_num(value))

    @property
    def is_automatic_minor_unit(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}minorUnit') is None

    @is_automatic_minor_unit.setter
    def is_automatic_minor_unit(self, value: bool):
        if value:
            self._remove_elem('minorUnit')

    # ------------------------------------------------------------------ #
    #  is_logarithmic / log_base  (lives inside <c:scaling>)
    # ------------------------------------------------------------------ #

    @property
    def is_logarithmic(self) -> bool:
        from .._internal.pptx.constants import NS
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is not None:
            return scaling.find(f'{NS.C}logBase') is not None
        return False

    @is_logarithmic.setter
    def is_logarithmic(self, value: bool):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is None:
            scaling = ET.SubElement(self._ax_elem, f'{NS.C}scaling')
        if value:
            if scaling.find(f'{NS.C}logBase') is None:
                # Insert logBase before orientation to match OOXML element order
                orient = scaling.find(f'{NS.C}orientation')
                lb = ET.Element(f'{NS.C}logBase')
                lb.set('val', '10')
                if orient is not None:
                    scaling.insert(list(scaling).index(orient), lb)
                else:
                    scaling.append(lb)
        else:
            lb = scaling.find(f'{NS.C}logBase')
            if lb is not None:
                scaling.remove(lb)

    @property
    def log_base(self) -> float:
        from .._internal.pptx.constants import NS
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is not None:
            el = scaling.find(f'{NS.C}logBase')
            if el is not None:
                try:
                    return float(el.get('val', '10'))
                except (ValueError, TypeError):
                    pass
        return 10.0

    @log_base.setter
    def log_base(self, value: float):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is None:
            scaling = ET.SubElement(self._ax_elem, f'{NS.C}scaling')
        el = scaling.find(f'{NS.C}logBase')
        if el is None:
            orient = scaling.find(f'{NS.C}orientation')
            el = ET.Element(f'{NS.C}logBase')
            if orient is not None:
                scaling.insert(list(scaling).index(orient), el)
            else:
                scaling.append(el)
        el.set('val', _format_num(value))

    # ------------------------------------------------------------------ #
    #  is_plot_order_reversed
    # ------------------------------------------------------------------ #

    @property
    def is_plot_order_reversed(self) -> bool:
        from .._internal.pptx.constants import NS
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is not None:
            orient = scaling.find(f'{NS.C}orientation')
            if orient is not None:
                return orient.get('val', 'minMax') == 'maxMin'
        return False

    @is_plot_order_reversed.setter
    def is_plot_order_reversed(self, value: bool):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is None:
            scaling = ET.SubElement(self._ax_elem, f'{NS.C}scaling')
        orient = scaling.find(f'{NS.C}orientation')
        if orient is None:
            orient = ET.SubElement(scaling, f'{NS.C}orientation')
        orient.set('val', 'maxMin' if value else 'minMax')

    # ------------------------------------------------------------------ #
    #  is_visible
    # ------------------------------------------------------------------ #

    @property
    def is_visible(self) -> bool:
        from .._internal.pptx.constants import NS
        delete = self._ax_elem.find(f'{NS.C}delete')
        if delete is not None:
            return delete.get('val', '0') in ('0', 'false')
        return True

    @is_visible.setter
    def is_visible(self, value: bool):
        self._write_simple_val('delete', '0' if value else '1')

    # ------------------------------------------------------------------ #
    #  position
    # ------------------------------------------------------------------ #

    @property
    def position(self) -> AxisPositionType:
        from .AxisPositionType import AxisPositionType
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}axPos')
        if el is not None:
            val = el.get('val', 'b')
            _map = {'b': AxisPositionType.BOTTOM, 'l': AxisPositionType.LEFT,
                     'r': AxisPositionType.RIGHT, 't': AxisPositionType.TOP}
            return _map.get(val, AxisPositionType.BOTTOM)
        return AxisPositionType.BOTTOM

    @position.setter
    def position(self, value: AxisPositionType):
        from .AxisPositionType import AxisPositionType
        _map = {AxisPositionType.BOTTOM: 'b', AxisPositionType.LEFT: 'l',
                AxisPositionType.RIGHT: 'r', AxisPositionType.TOP: 't'}
        self._write_simple_val('axPos', _map.get(value, 'b'))

    # ------------------------------------------------------------------ #
    #  tick marks
    # ------------------------------------------------------------------ #

    @property
    def major_tick_mark(self) -> TickMarkType:
        return self._read_tick_mark('majorTickMark')

    @major_tick_mark.setter
    def major_tick_mark(self, value: TickMarkType):
        self._write_tick_mark('majorTickMark', value)

    @property
    def minor_tick_mark(self) -> TickMarkType:
        return self._read_tick_mark('minorTickMark')

    @minor_tick_mark.setter
    def minor_tick_mark(self, value: TickMarkType):
        self._write_tick_mark('minorTickMark', value)

    def _read_tick_mark(self, local_name: str) -> TickMarkType:
        from .TickMarkType import TickMarkType
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            val = el.get('val', 'cross')
            _map = {'cross': TickMarkType.CROSS, 'in': TickMarkType.INSIDE,
                     'none': TickMarkType.NONE, 'out': TickMarkType.OUTSIDE}
            return _map.get(val, TickMarkType.CROSS)
        return TickMarkType.CROSS

    def _write_tick_mark(self, local_name: str, value: TickMarkType):
        from .TickMarkType import TickMarkType
        _map = {TickMarkType.CROSS: 'cross', TickMarkType.INSIDE: 'in',
                TickMarkType.NONE: 'none', TickMarkType.OUTSIDE: 'out'}
        self._write_simple_val(local_name, _map.get(value, 'cross'))

    # ------------------------------------------------------------------ #
    #  tick_label_position
    # ------------------------------------------------------------------ #

    @property
    def tick_label_position(self) -> TickLabelPositionType:
        from .TickLabelPositionType import TickLabelPositionType
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}tickLblPos')
        if el is not None:
            val = el.get('val', 'nextTo')
            _map = {'high': TickLabelPositionType.HIGH,
                     'low': TickLabelPositionType.LOW,
                     'nextTo': TickLabelPositionType.NEXT_TO,
                     'none': TickLabelPositionType.NONE}
            return _map.get(val, TickLabelPositionType.NEXT_TO)
        return TickLabelPositionType.NEXT_TO

    @tick_label_position.setter
    def tick_label_position(self, value: TickLabelPositionType):
        from .TickLabelPositionType import TickLabelPositionType
        _map = {TickLabelPositionType.HIGH: 'high',
                TickLabelPositionType.LOW: 'low',
                TickLabelPositionType.NEXT_TO: 'nextTo',
                TickLabelPositionType.NONE: 'none'}
        self._write_simple_val('tickLblPos', _map.get(value, 'nextTo'))

    # ------------------------------------------------------------------ #
    #  tick_label_spacing / tick_marks_spacing (and auto flags)
    # ------------------------------------------------------------------ #

    @property
    def tick_label_spacing(self) -> int:
        return self._read_simple_int('tickLblSkip', 1)

    @tick_label_spacing.setter
    def tick_label_spacing(self, value: int):
        self._write_simple_val('tickLblSkip', str(value))

    @property
    def is_automatic_tick_label_spacing(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}tickLblSkip') is None

    @is_automatic_tick_label_spacing.setter
    def is_automatic_tick_label_spacing(self, value: bool):
        if value:
            self._remove_elem('tickLblSkip')

    @property
    def tick_marks_spacing(self) -> int:
        return self._read_simple_int('tickMarkSkip', 1)

    @tick_marks_spacing.setter
    def tick_marks_spacing(self, value: int):
        self._write_simple_val('tickMarkSkip', str(value))

    @property
    def is_automatic_tick_marks_spacing(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}tickMarkSkip') is None

    @is_automatic_tick_marks_spacing.setter
    def is_automatic_tick_marks_spacing(self, value: bool):
        if value:
            self._remove_elem('tickMarkSkip')

    # ------------------------------------------------------------------ #
    #  tick_label_rotation_angle
    # ------------------------------------------------------------------ #

    @property
    def tick_label_rotation_angle(self) -> float:
        from .._internal.pptx.constants import NS
        txPr = self._ax_elem.find(f'{NS.C}txPr')
        if txPr is not None:
            bodyPr = txPr.find(f'{NS.A}bodyPr')
            if bodyPr is not None:
                rot = bodyPr.get('rot')
                if rot is not None:
                    try:
                        return int(rot) / 60000.0
                    except (ValueError, TypeError):
                        pass
        return 0.0

    @tick_label_rotation_angle.setter
    def tick_label_rotation_angle(self, value: float):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        txPr = self._ax_elem.find(f'{NS.C}txPr')
        if txPr is None:
            txPr = ET.SubElement(self._ax_elem, f'{NS.C}txPr')
        bodyPr = txPr.find(f'{NS.A}bodyPr')
        if bodyPr is None:
            bodyPr = ET.SubElement(txPr, f'{NS.A}bodyPr')
        bodyPr.set('rot', str(int(value * 60000)))
        # Ensure minimal valid txPr structure (required by readers)
        if txPr.find(f'{NS.A}p') is None:
            p = ET.SubElement(txPr, f'{NS.A}p')
            pPr = ET.SubElement(p, f'{NS.A}pPr')
            ET.SubElement(pPr, f'{NS.A}defRPr')

    # ------------------------------------------------------------------ #
    #  label_offset
    # ------------------------------------------------------------------ #

    @property
    def label_offset(self) -> int:
        return self._read_simple_int('lblOffset', 100)

    @label_offset.setter
    def label_offset(self, value: int):
        self._write_simple_val('lblOffset', str(value))

    # ------------------------------------------------------------------ #
    #  number_format / is_number_format_linked_to_source
    # ------------------------------------------------------------------ #

    @property
    def number_format(self) -> str:
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}numFmt')
        if el is not None:
            return el.get('formatCode', 'General')
        return 'General'

    @number_format.setter
    def number_format(self, value: str):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        el = self._ax_elem.find(f'{NS.C}numFmt')
        if el is None:
            el = ET.SubElement(self._ax_elem, f'{NS.C}numFmt')
        el.set('formatCode', value)

    @property
    def is_number_format_linked_to_source(self) -> bool:
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}numFmt')
        if el is not None:
            return el.get('sourceLinked', '1') in ('1', 'true')
        return True

    @is_number_format_linked_to_source.setter
    def is_number_format_linked_to_source(self, value: bool):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        el = self._ax_elem.find(f'{NS.C}numFmt')
        if el is None:
            el = ET.SubElement(self._ax_elem, f'{NS.C}numFmt')
            el.set('formatCode', 'General')
        el.set('sourceLinked', '1' if value else '0')

    # ------------------------------------------------------------------ #
    #  has_title
    # ------------------------------------------------------------------ #

    @property
    def has_title(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}title') is not None

    @has_title.setter
    def has_title(self, value: bool):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        existing = self._ax_elem.find(f'{NS.C}title')
        if value and existing is None:
            # Insert <c:title> after <c:axPos> to match standard element order
            title = ET.Element(f'{NS.C}title')
            ax_pos = self._ax_elem.find(f'{NS.C}axPos')
            if ax_pos is not None:
                idx = list(self._ax_elem).index(ax_pos)
                self._ax_elem.insert(idx + 1, title)
            else:
                self._ax_elem.append(title)
        elif not value and existing is not None:
            self._ax_elem.remove(existing)

    # ------------------------------------------------------------------ #
    #  show_major_grid_lines / show_minor_grid_lines
    # ------------------------------------------------------------------ #

    @property
    def show_major_grid_lines(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}majorGridlines') is not None

    @property
    def show_minor_grid_lines(self) -> bool:
        from .._internal.pptx.constants import NS
        return self._ax_elem.find(f'{NS.C}minorGridlines') is not None

    # ------------------------------------------------------------------ #
    #  date axis: major_unit_scale / minor_unit_scale / base_unit_scale
    # ------------------------------------------------------------------ #

    @property
    def major_unit_scale(self) -> TimeUnitType:
        return self._read_time_unit('majorTimeUnit')

    @major_unit_scale.setter
    def major_unit_scale(self, value: TimeUnitType):
        self._write_time_unit('majorTimeUnit', value)

    @property
    def minor_unit_scale(self) -> TimeUnitType:
        return self._read_time_unit('minorTimeUnit')

    @minor_unit_scale.setter
    def minor_unit_scale(self, value: TimeUnitType):
        self._write_time_unit('minorTimeUnit', value)

    @property
    def base_unit_scale(self) -> TimeUnitType:
        return self._read_time_unit('baseTimeUnit')

    @base_unit_scale.setter
    def base_unit_scale(self, value: TimeUnitType):
        self._write_time_unit('baseTimeUnit', value)

    def _read_time_unit(self, local_name: str) -> TimeUnitType:
        from .TimeUnitType import TimeUnitType
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            val = el.get('val', '')
            _map = {'days': TimeUnitType.DAYS, 'months': TimeUnitType.MONTHS,
                     'years': TimeUnitType.YEARS}
            return _map.get(val, TimeUnitType.NONE)
        return TimeUnitType.NONE

    def _write_time_unit(self, local_name: str, value: TimeUnitType):
        from .TimeUnitType import TimeUnitType
        if value == TimeUnitType.NONE:
            self._remove_elem(local_name)
            return
        _map = {TimeUnitType.DAYS: 'days', TimeUnitType.MONTHS: 'months',
                TimeUnitType.YEARS: 'years'}
        xml_val = _map.get(value)
        if xml_val:
            self._write_simple_val(local_name, xml_val)

    # ------------------------------------------------------------------ #
    #  actual_* properties (read-only, return current XML values)
    # ------------------------------------------------------------------ #

    @property
    def actual_max_value(self) -> float:
        return self.max_value

    @property
    def actual_min_value(self) -> float:
        return self.min_value

    @property
    def actual_major_unit(self) -> float:
        return self.major_unit

    @property
    def actual_minor_unit(self) -> float:
        return self.minor_unit

    @property
    def actual_major_unit_scale(self) -> TimeUnitType:
        return self.major_unit_scale

    @property
    def actual_minor_unit_scale(self) -> TimeUnitType:
        return self.minor_unit_scale

    # ------------------------------------------------------------------ #
    #  Formatting properties
    # ------------------------------------------------------------------ #

    @property
    def format(self):
        """Returns the format of the axis. Read-only."""
        from .Format import Format
        fmt = Format()
        fmt._init_internal(self._ax_elem, self._chart_part)
        return fmt

    @property
    def text_format(self):
        """Returns the chart text format for axis labels. Read-only."""
        from .ChartTextFormat import ChartTextFormat
        ctf = ChartTextFormat()
        ctf._init_internal(self._ax_elem, self._chart_part)
        return ctf

    @property
    def title(self):
        """Gets the axis' title. Read-only."""
        from .._internal.pptx.constants import NS
        from .ChartTitle import ChartTitle
        title_elem = self._ax_elem.find(f'{NS.C}title')
        ct = ChartTitle()
        ct._init_internal(title_elem, self._chart_part, self._ax_elem)
        return ct

    @property
    def major_grid_lines_format(self):
        """Returns the format of major gridlines. Read-only."""
        from .ChartLinesFormat import ChartLinesFormat
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        gl = self._ax_elem.find(f'{NS.C}majorGridlines')
        if gl is None:
            gl = ET.SubElement(self._ax_elem, f'{NS.C}majorGridlines')
        clf = ChartLinesFormat()
        clf._init_internal(gl, self._chart_part)
        return clf

    @property
    def minor_grid_lines_format(self):
        """Returns the format of minor gridlines. Read-only."""
        from .ChartLinesFormat import ChartLinesFormat
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        gl = self._ax_elem.find(f'{NS.C}minorGridlines')
        if gl is None:
            gl = ET.SubElement(self._ax_elem, f'{NS.C}minorGridlines')
        clf = ChartLinesFormat()
        clf._init_internal(gl, self._chart_part)
        return clf

    # ------------------------------------------------------------------ #
    #  _init_internal
    # ------------------------------------------------------------------ #

    def _init_internal(self, ax_elem, chart_part: 'ChartPart'):
        """
        Initialize from an axis XML element (<c:catAx>, <c:valAx>, <c:dateAx>, <c:serAx>).

        Args:
            ax_elem: The lxml axis element.
            chart_part: Parent ChartPart for save coordination.
        """
        self._ax_elem = ax_elem
        self._chart_part = chart_part

    # ------------------------------------------------------------------ #
    #  Axis ID helpers
    # ------------------------------------------------------------------ #

    @property
    def _axis_id(self) -> str:
        """The axis ID from <c:axId val="...">."""
        from .._internal.pptx.constants import NS
        ax_id = self._ax_elem.find(f'{NS.C}axId')
        return ax_id.get('val', '') if ax_id is not None else ''

    @property
    def _cross_axis_id(self) -> str:
        """The crossing axis ID from <c:crossAx val="...">."""
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}crossAx')
        return el.get('val', '') if el is not None else ''

    def _get_perpendicular_ax_elem(self):
        """Find the perpendicular axis XML element via crossAx ID."""
        from .._internal.pptx.constants import NS
        cross_id = self._cross_axis_id
        if not cross_id:
            return None
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return None
        C = NS.C
        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local in ('catAx', 'valAx', 'dateAx', 'serAx'):
                ax_id_elem = child.find(f'{C}axId')
                if ax_id_elem is not None and ax_id_elem.get('val') == cross_id:
                    return child
        return None

    # ------------------------------------------------------------------ #
    #  XML helper methods
    # ------------------------------------------------------------------ #

    def _read_simple_float(self, local_name: str, default: float) -> float:
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            try:
                return float(el.get('val', str(default)))
            except (ValueError, TypeError):
                return default
        return default

    def _read_simple_int(self, local_name: str, default: int) -> int:
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            try:
                return int(el.get('val', str(default)))
            except (ValueError, TypeError):
                return default
        return default

    def _read_bool(self, local_name: str, true_val: bool, default_missing: bool = True) -> bool:
        """Read a bool from a child element.

        For <c:crossBetween>, val='between' → True, val='midCat' → False.
        For standard bools, val='1'/'true' → True.
        """
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            val = el.get('val', '')
            if local_name == 'crossBetween':
                return val == 'between'
            return val in ('1', 'true')
        return default_missing

    def _write_simple_val(self, local_name: str, value: str):
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is None:
            el = ET.SubElement(self._ax_elem, f'{NS.C}{local_name}')
        el.set('val', value)

    def _remove_elem(self, local_name: str):
        from .._internal.pptx.constants import NS
        el = self._ax_elem.find(f'{NS.C}{local_name}')
        if el is not None:
            self._ax_elem.remove(el)

    def _read_scaling_val(self, which: str, default: float) -> float:
        """Read max or min from <c:scaling>/<c:max|min val="...">."""
        from .._internal.pptx.constants import NS
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is not None:
            el = scaling.find(f'{NS.C}{which}')
            if el is not None:
                try:
                    return float(el.get('val', str(default)))
                except (ValueError, TypeError):
                    pass
        return default

    def _write_scaling_val(self, which: str, value: float):
        """Write max or min to <c:scaling>/<c:max|min val="...">."""
        from .._internal.pptx.constants import NS
        import lxml.etree as ET
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is None:
            scaling = ET.SubElement(self._ax_elem, f'{NS.C}scaling')
        el = scaling.find(f'{NS.C}{which}')
        if el is None:
            el = ET.SubElement(scaling, f'{NS.C}{which}')
        el.set('val', _format_num(value))

    def _is_auto_scaling(self, which: str) -> bool:
        """Check if max/min is automatic (no element present in scaling)."""
        from .._internal.pptx.constants import NS
        scaling = self._ax_elem.find(f'{NS.C}scaling')
        if scaling is not None:
            return scaling.find(f'{NS.C}{which}') is None
        return True

    def _set_auto_scaling(self, which: str, auto: bool):
        """Set automatic scaling by removing or keeping the element."""
        if auto:
            from .._internal.pptx.constants import NS
            scaling = self._ax_elem.find(f'{NS.C}scaling')
            if scaling is not None:
                el = scaling.find(f'{NS.C}{which}')
                if el is not None:
                    scaling.remove(el)


def _format_num(value: float) -> str:
    """Format a number: integers without .0, floats as-is."""
    if value == int(value):
        return str(int(value))
    return str(value)
