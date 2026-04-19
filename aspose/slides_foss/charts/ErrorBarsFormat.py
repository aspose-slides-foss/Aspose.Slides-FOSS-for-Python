from __future__ import annotations
from typing import TYPE_CHECKING

from .ErrorBarType import ErrorBarType
from .ErrorBarValueType import ErrorBarValueType
from .IErrorBarsFormat import IErrorBarsFormat

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart


# XML value mappings
_ERR_BAR_TYPE_TO_XML = {
    ErrorBarType.BOTH: 'both',
    ErrorBarType.PLUS: 'plus',
    ErrorBarType.MINUS: 'minus',
}
_XML_TO_ERR_BAR_TYPE = {v: k for k, v in _ERR_BAR_TYPE_TO_XML.items()}
_XML_TO_ERR_BAR_TYPE[''] = ErrorBarType.BOTH  # empty val attr = both

_ERR_VAL_TYPE_TO_XML = {
    ErrorBarValueType.FIXED: 'fixedVal',
    ErrorBarValueType.PERCENTAGE: 'percentage',
    ErrorBarValueType.STANDARD_DEVIATION: 'stdDev',
    ErrorBarValueType.STANDARD_ERROR: 'stdErr',
    ErrorBarValueType.CUSTOM: 'cust',
}
_XML_TO_ERR_VAL_TYPE = {v: k for k, v in _ERR_VAL_TYPE_TO_XML.items()}


class ErrorBarsFormat(IErrorBarsFormat):
    """Represents error bars of chart series."""

    @property
    def type(self) -> ErrorBarType:
        return self._type

    @type.setter
    def type(self, value: ErrorBarType):
        self._type = value

    @property
    def value_type(self) -> ErrorBarValueType:
        return self._value_type

    @value_type.setter
    def value_type(self, value: ErrorBarValueType):
        self._value_type = value

    @property
    def has_end_cap(self) -> bool:
        return self._has_end_cap

    @has_end_cap.setter
    def has_end_cap(self, value: bool):
        self._has_end_cap = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool):
        self._is_visible = value

    @property
    def direction(self) -> str:
        """Internal: 'x' or 'y'."""
        return self._direction

    @property
    def custom_plus_values(self) -> list[float]:
        """Internal: custom plus values per data point."""
        return self._custom_plus

    @property
    def custom_minus_values(self) -> list[float]:
        """Internal: custom minus values per data point."""
        return self._custom_minus

    def _init_internal(self, direction: str, chart_part: 'ChartPart' = None):
        self._direction = direction  # 'x' or 'y'
        self._chart_part = chart_part
        self._type = ErrorBarType.BOTH
        self._value_type = ErrorBarValueType.FIXED
        self._has_end_cap = True
        self._value = 0.0
        self._is_visible = False
        self._custom_plus: list[float] = []
        self._custom_minus: list[float] = []

    def _init_from_xml(self, err_bars_elem, chart_part: 'ChartPart' = None):
        """Parse an <c:errBars> XML element."""
        from .._internal.pptx.constants import NS
        C = NS.C

        self._chart_part = chart_part
        self._is_visible = True

        # Direction
        dir_elem = err_bars_elem.find(f'{C}errDir')
        self._direction = dir_elem.get('val', 'y') if dir_elem is not None else 'y'

        # Error bar type (both/plus/minus)
        type_elem = err_bars_elem.find(f'{C}errBarType')
        if type_elem is not None:
            val = type_elem.get('val', '')
            self._type = _XML_TO_ERR_BAR_TYPE.get(val, ErrorBarType.BOTH)
        else:
            self._type = ErrorBarType.BOTH

        # Value type
        val_type_elem = err_bars_elem.find(f'{C}errValType')
        if val_type_elem is not None:
            val = val_type_elem.get('val', 'fixedVal')
            self._value_type = _XML_TO_ERR_VAL_TYPE.get(val, ErrorBarValueType.FIXED)
        else:
            self._value_type = ErrorBarValueType.FIXED

        # No end cap
        no_end_cap_elem = err_bars_elem.find(f'{C}noEndCap')
        if no_end_cap_elem is not None:
            self._has_end_cap = no_end_cap_elem.get('val', '0') == '0'
        else:
            self._has_end_cap = True

        # Value (for fixed/percentage/stdDev)
        val_elem = err_bars_elem.find(f'{C}val')
        if val_elem is not None:
            try:
                self._value = float(val_elem.get('val', '0'))
            except (ValueError, TypeError):
                self._value = 0.0
        else:
            self._value = 0.0

        # Custom values
        self._custom_plus = []
        self._custom_minus = []
        if self._value_type == ErrorBarValueType.CUSTOM:
            self._custom_plus = _parse_num_lit(err_bars_elem.find(f'{C}plus'), C)
            self._custom_minus = _parse_num_lit(err_bars_elem.find(f'{C}minus'), C)

    def _to_xml(self):
        """Build an <c:errBars> XML element."""
        import lxml.etree as ET
        from .._internal.pptx.constants import NS
        C = NS.C

        err_bars = ET.Element(f'{C}errBars')

        # errDir
        dir_elem = ET.SubElement(err_bars, f'{C}errDir')
        dir_elem.set('val', self._direction)

        # errBarType
        type_elem = ET.SubElement(err_bars, f'{C}errBarType')
        xml_type = _ERR_BAR_TYPE_TO_XML.get(self._type, 'both')
        if xml_type != 'both':
            type_elem.set('val', xml_type)
        # val attribute is omitted for 'both' per OOXML convention

        # errValType
        val_type_elem = ET.SubElement(err_bars, f'{C}errValType')
        val_type_elem.set('val', _ERR_VAL_TYPE_TO_XML.get(self._value_type, 'fixedVal'))

        # noEndCap
        no_end_cap = ET.SubElement(err_bars, f'{C}noEndCap')
        no_end_cap.set('val', '0' if self._has_end_cap else '1')

        if self._value_type == ErrorBarValueType.CUSTOM:
            # Custom: write <c:plus>/<c:minus> with numLit
            _build_num_lit(err_bars, f'{C}plus', self._custom_plus, C)
            _build_num_lit(err_bars, f'{C}minus', self._custom_minus, C)
        else:
            # Value element for fixed/percentage/stdDev/stdErr
            val_elem = ET.SubElement(err_bars, f'{C}val')
            val_elem.set('val', _format_num(self._value))

        return err_bars


def _parse_num_lit(container_elem, C: str) -> list[float]:
    """Parse <c:plus>/<c:minus> → <c:numLit> → list of floats."""
    if container_elem is None:
        return []
    num_lit = container_elem.find(f'{C}numLit')
    if num_lit is None:
        return []
    values = []
    for pt in num_lit.findall(f'{C}pt'):
        v_elem = pt.find(f'{C}v')
        if v_elem is not None and v_elem.text:
            try:
                values.append(float(v_elem.text))
            except ValueError:
                values.append(0.0)
        else:
            values.append(0.0)
    return values


def _build_num_lit(parent, tag: str, values: list[float], C: str):
    """Build <c:plus>/<c:minus> → <c:numLit> from a list of floats."""
    import lxml.etree as ET

    container = ET.SubElement(parent, tag)
    num_lit = ET.SubElement(container, f'{C}numLit')
    fmt = ET.SubElement(num_lit, f'{C}formatCode')
    fmt.text = 'General'
    pt_count = ET.SubElement(num_lit, f'{C}ptCount')
    pt_count.set('val', str(len(values)))
    for i, val in enumerate(values):
        pt = ET.SubElement(num_lit, f'{C}pt')
        pt.set('idx', str(i))
        v = ET.SubElement(pt, f'{C}v')
        v.text = _format_num(val)


def _format_num(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)
