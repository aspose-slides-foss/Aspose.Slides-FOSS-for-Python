"""Converters of chart shapes to markdown tables."""

from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta

from ....charts.ChartType import ChartType

_COLUMN_TYPES = frozenset([
    ChartType.CLUSTERED_COLUMN, ChartType.STACKED_COLUMN, ChartType.PERCENTS_STACKED_COLUMN,
    ChartType.CLUSTERED_COLUMN_3D, ChartType.STACKED_COLUMN_3D, ChartType.PERCENTS_STACKED_COLUMN_3D,
    ChartType.COLUMN_3D, ChartType.CLUSTERED_CYLINDER, ChartType.STACKED_CYLINDER,
    ChartType.PERCENTS_STACKED_CYLINDER, ChartType.CYLINDER_3D, ChartType.CLUSTERED_CONE,
    ChartType.STACKED_CONE, ChartType.PERCENTS_STACKED_CONE, ChartType.CONE_3D,
    ChartType.CLUSTERED_PYRAMID, ChartType.STACKED_PYRAMID, ChartType.PERCENTS_STACKED_PYRAMID,
    ChartType.PYRAMID_3D,
])

_BAR_TYPES = frozenset([
    ChartType.CLUSTERED_BAR, ChartType.STACKED_BAR, ChartType.PERCENTS_STACKED_BAR,
    ChartType.CLUSTERED_BAR_3D, ChartType.STACKED_BAR_3D, ChartType.PERCENTS_STACKED_BAR_3D,
    ChartType.CLUSTERED_HORIZONTAL_CYLINDER, ChartType.STACKED_HORIZONTAL_CYLINDER,
    ChartType.PERCENTS_STACKED_HORIZONTAL_CYLINDER, ChartType.CLUSTERED_HORIZONTAL_CONE,
    ChartType.STACKED_HORIZONTAL_CONE, ChartType.PERCENTS_STACKED_HORIZONTAL_CONE,
    ChartType.CLUSTERED_HORIZONTAL_PYRAMID, ChartType.STACKED_HORIZONTAL_PYRAMID,
    ChartType.PERCENTS_STACKED_HORIZONTAL_PYRAMID,
])

_LINE_TYPES = frozenset([
    ChartType.LINE, ChartType.STACKED_LINE, ChartType.PERCENTS_STACKED_LINE,
    ChartType.LINE_WITH_MARKERS, ChartType.STACKED_LINE_WITH_MARKERS,
    ChartType.PERCENTS_STACKED_LINE_WITH_MARKERS, ChartType.LINE_3D,
])

_STOCK_TYPES = frozenset([
    ChartType.HIGH_LOW_CLOSE, ChartType.OPEN_HIGH_LOW_CLOSE,
    ChartType.VOLUME_HIGH_LOW_CLOSE, ChartType.VOLUME_OPEN_HIGH_LOW_CLOSE,
])

_AREA_TYPES = frozenset([
    ChartType.AREA, ChartType.STACKED_AREA, ChartType.PERCENTS_STACKED_AREA,
    ChartType.AREA_3D, ChartType.STACKED_AREA_3D, ChartType.PERCENTS_STACKED_AREA_3D,
])

_PIE_TYPES = frozenset([
    ChartType.PIE, ChartType.PIE_3D, ChartType.PIE_OF_PIE, ChartType.EXPLODED_PIE,
    ChartType.EXPLODED_PIE_3D, ChartType.BAR_OF_PIE,
    ChartType.DOUGHNUT, ChartType.EXPLODED_DOUGHNUT,
])

_REGULAR_TYPES = _COLUMN_TYPES | _BAR_TYPES | _LINE_TYPES | _STOCK_TYPES | _AREA_TYPES | _PIE_TYPES

_BUBBLE_TYPES = frozenset([ChartType.BUBBLE, ChartType.BUBBLE_WITH_3D])

# Chart types whose series use X/Y value coordinates instead of categories.
_XY_TYPES = frozenset([
    ChartType.SCATTER_WITH_MARKERS, ChartType.SCATTER_WITH_SMOOTH_LINES_AND_MARKERS,
    ChartType.SCATTER_WITH_SMOOTH_LINES, ChartType.SCATTER_WITH_STRAIGHT_LINES_AND_MARKERS,
    ChartType.SCATTER_WITH_STRAIGHT_LINES,
]) | _BUBBLE_TYPES


def get_chart_converter(chart_type):
    """Returns the converter function for the chart type, or None for unsupported types."""
    if chart_type in _REGULAR_TYPES:
        return convert_regular_chart
    if chart_type in _XY_TYPES:
        return convert_xy_chart
    return None


def escape_cell(text):
    if text is None:
        return ''

    text = text.replace('\\', '\\\\')  # escape backslash first so our \| stays intact
    text = text.replace('|', '\\|')
    text = text.replace('\r\n', '<br>')
    text = text.replace('\n', '<br>')
    text = text.replace('\r', '<br>')
    return text


def _value_to_str(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _chart_value_data(chart_value):
    """Returns the raw data of an IBaseChartValue, resolving workbook-backed cells."""
    if chart_value is None:
        return None

    # Workbook-backed values reference a ChartDataCell; use its value.
    cell = getattr(chart_value, '_cell', None)
    if cell is not None:
        return cell.value

    data = chart_value.data

    # Some construction paths store the ChartDataCell object as data; unwrap it.
    if data is not None and not isinstance(data, (int, float, str, bool)) and hasattr(data, 'value'):
        return data.value

    return data


def _series_name_str(series):
    name = series.name
    if name is None:
        return ''
    return name.to_string()


_EXCEL_EPOCH = datetime(1899, 12, 30)

_date_separator = None


def _locale_date_separator():
    """The current user locale's date separator — the '/' in a date format
    code renders as this separator."""
    global _date_separator
    if _date_separator is None:
        separator = '/'
        if sys.platform == 'win32':
            try:
                import ctypes
                buf = ctypes.create_unicode_buffer(8)
                LOCALE_SDATE = 0x001D
                if ctypes.windll.kernel32.GetLocaleInfoEx(None, LOCALE_SDATE, buf, len(buf)):
                    separator = buf.value or '/'
            except Exception:
                pass
        _date_separator = separator
    return _date_separator


def _is_date_format(format_code):
    stripped = re.sub(r'"[^"]*"|\\.', '', format_code)
    if re.search(r'[#0?]', stripped):
        return False
    return re.search(r'[yYdD]', stripped) is not None


def _format_date_by_code(value, format_code):
    """Renders an Excel date serial by a date format code (y/m/d tokens)."""
    try:
        serial = float(value)
    except (TypeError, ValueError):
        return None

    if not 0 < serial < 2958466:  # 9999-12-31
        return None

    date = _EXCEL_EPOCH + timedelta(days=serial)

    out = []
    i = 0
    while i < len(format_code):
        ch = format_code[i]
        if ch == '"':
            end = format_code.find('"', i + 1)
            if end == -1:
                end = len(format_code)
            out.append(format_code[i + 1:end])
            i = end + 1
        elif ch == '\\':
            if i + 1 < len(format_code):
                out.append(format_code[i + 1])
            i += 2
        elif ch in 'yYmMdD':
            j = i
            while j < len(format_code) and format_code[j].lower() == ch.lower():
                j += 1
            run = j - i
            token = ch.lower()
            if token == 'y':
                out.append('{0:04d}'.format(date.year) if run >= 3
                           else '{0:02d}'.format(date.year % 100))
            elif token == 'm':
                if run >= 4:
                    out.append(date.strftime('%B'))
                elif run == 3:
                    out.append(date.strftime('%b'))
                elif run == 2:
                    out.append('{0:02d}'.format(date.month))
                else:
                    out.append(str(date.month))
            else:
                if run >= 4:
                    out.append(date.strftime('%A'))
                elif run == 3:
                    out.append(date.strftime('%a'))
                elif run == 2:
                    out.append('{0:02d}'.format(date.day))
                else:
                    out.append(str(date.day))
            i = j
        elif ch == '/':
            out.append(_locale_date_separator())
            i += 1
        else:
            out.append(ch)
            i += 1

    return ''.join(out)


def _get_category_text(category, chart):
    """Renders a category value the way the chart displays it — applying the
    category's number format so date serials show as dates, not integers."""
    value = category.value

    if value is None:
        return ''

    if isinstance(value, str):
        return value

    format_code = getattr(category, '_format_code', None)
    if not format_code:
        try:
            format_code = chart.axes.horizontal_axis.number_format
        except Exception:
            format_code = None

    if format_code and format_code != 'General' and _is_date_format(format_code):
        formatted = _format_date_by_code(value, format_code)
        if formatted is not None:
            return formatted

    return _value_to_str(value)


def _chart_header(chart, converter):
    nl = converter.get_new_line()
    parts = ['### {0} chart{1}'.format(chart.type.value, nl)]

    if chart.has_title and chart.chart_title is not None:
        title_frame = chart.chart_title.text_frame_for_overriding
        if title_frame is not None:
            parts.append('Chart title: ' + escape_cell(title_frame.text) + nl)

    return parts


def convert_regular_chart(chart, converter):
    nl = converter.get_new_line()
    parts = _chart_header(chart, converter)

    series = list(chart.chart_data.series)
    categories = list(chart.chart_data.categories)

    # Header
    parts.append('||')
    for s in series:
        parts.append(escape_cell(_series_name_str(s)))
        parts.append('|')

    parts.append(nl)

    # Separator
    parts.append('|-|')
    for _ in series:
        parts.append('-|')

    parts.append(nl)

    # Rows
    for j in range(len(categories)):
        parts.append('|')
        parts.append(escape_cell(_get_category_text(categories[j], chart)))
        parts.append('|')

        for s in series:
            data_points = list(s.data_points)
            cell = ''
            if j < len(data_points):
                dp = data_points[j]
                data = _chart_value_data(dp.value) if dp is not None else None
                if data is not None:
                    cell = _value_to_str(data)

            parts.append(escape_cell(cell))
            parts.append('|')

        parts.append(nl)

    return ''.join(parts)


def convert_xy_chart(chart, converter):
    nl = converter.get_new_line()
    parts = _chart_header(chart, converter)

    series = list(chart.chart_data.series)
    bubble = chart.type in _BUBBLE_TYPES

    # Header: shared X column, then per series a Y column (+ Size for bubble).
    parts.append('|X|')
    for s in series:
        name = _series_name_str(s)
        name = escape_cell(name) if name else ''
        parts.append(name + '|')
        if bubble:
            parts.append(name + ' Size|')

    parts.append(nl)

    columns = 1 + len(series) * (2 if bubble else 1)
    parts.append('|')
    for _ in range(columns):
        parts.append('-|')

    parts.append(nl)

    series_data_points = [list(s.data_points) for s in series]

    row_count = 0
    for dps in series_data_points:
        if len(dps) > row_count:
            row_count = len(dps)

    for j in range(row_count):
        # Shared X from the first series that has a point at this index.
        x_cell = ''
        for dps in series_data_points:
            if j < len(dps) and dps[j] is not None:
                x_data = _chart_value_data(dps[j].x_value)
                if x_data is not None:
                    x_cell = _value_to_str(x_data)
                    break

        parts.append('|')
        parts.append(escape_cell(x_cell))
        parts.append('|')

        for dps in series_data_points:
            dp = dps[j] if j < len(dps) else None

            y = ''
            y_data = _chart_value_data(dp.y_value) if dp is not None else None
            if y_data is not None:
                y = _value_to_str(y_data)

            parts.append(escape_cell(y))
            parts.append('|')

            if bubble:
                size = ''
                size_data = _chart_value_data(dp.bubble_size) if dp is not None else None
                if size_data is not None:
                    size = _value_to_str(size_data)

                parts.append(escape_cell(size))
                parts.append('|')

        parts.append(nl)

    return ''.join(parts)
