from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET

from .TrendlineType import TrendlineType
from .ITrendline import ITrendline

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart

# XML tag mapping: TrendlineType enum -> OOXML trendlineType/@val
_TYPE_TO_XML = {
    TrendlineType.EXPONENTIAL: 'exp',
    TrendlineType.LINEAR: 'linear',
    TrendlineType.LOGARITHMIC: 'log',
    TrendlineType.MOVING_AVERAGE: 'movingAvg',
    TrendlineType.POLYNOMIAL: 'poly',
    TrendlineType.POWER: 'power',
}
_XML_TO_TYPE = {v: k for k, v in _TYPE_TO_XML.items()}


class Trendline(ITrendline):
    """Represents a trend line of a chart series."""

    @property
    def trendline_name(self) -> str:
        return self._trendline_name

    @trendline_name.setter
    def trendline_name(self, value: str):
        self._trendline_name = value

    @property
    def trendline_type(self) -> TrendlineType:
        return self._trendline_type

    @trendline_type.setter
    def trendline_type(self, value: TrendlineType):
        self._trendline_type = value

    @property
    def backward(self) -> float:
        return self._backward

    @backward.setter
    def backward(self, value: float):
        self._backward = value

    @property
    def forward(self) -> float:
        return self._forward

    @forward.setter
    def forward(self, value: float):
        self._forward = value

    @property
    def intercept(self) -> float:
        return self._intercept

    @intercept.setter
    def intercept(self, value: float):
        self._intercept = value

    @property
    def display_equation(self) -> bool:
        return self._display_equation

    @display_equation.setter
    def display_equation(self, value: bool):
        self._display_equation = value

    @property
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, value: int):
        if value < 2 or value > 6:
            raise ValueError("Polynomial order must be between 2 and 6")
        self._order = value

    @property
    def period(self) -> int:
        return self._period

    @period.setter
    def period(self, value: int):
        if value < 2 or value > 255:
            raise ValueError("Moving average period must be between 2 and 255")
        self._period = value

    @property
    def display_r_squared_value(self) -> bool:
        return self._display_r_squared_value

    @display_r_squared_value.setter
    def display_r_squared_value(self, value: bool):
        self._display_r_squared_value = value

    def _init_internal(self, trendline_type: TrendlineType,
                       chart_part: 'ChartPart' = None):
        """Initialize a new trendline with defaults."""
        self._trendline_type = trendline_type
        self._chart_part = chart_part
        self._trendline_name = ''
        self._backward = 0.0
        self._forward = 0.0
        self._intercept = float('nan')  # NaN means "not set" (auto)
        self._display_equation = False
        self._display_r_squared_value = False
        self._order = 2  # default for polynomial
        self._period = 2  # default for moving average

    def _init_from_xml(self, trendline_elem: ET._Element,
                       chart_part: 'ChartPart' = None):
        """Initialize from an existing <c:trendline> XML element."""
        from .._internal.pptx.constants import NS
        C = NS.C
        self._chart_part = chart_part

        # trendlineType
        type_elem = trendline_elem.find(f'{C}trendlineType')
        xml_val = type_elem.get('val', 'linear') if type_elem is not None else 'linear'
        self._trendline_type = _XML_TO_TYPE.get(xml_val, TrendlineType.LINEAR)

        # name
        name_elem = trendline_elem.find(f'{C}name')
        self._trendline_name = name_elem.text if name_elem is not None and name_elem.text else ''

        # forward/backward
        fwd_elem = trendline_elem.find(f'{C}forward')
        self._forward = float(fwd_elem.get('val', '0')) if fwd_elem is not None else 0.0

        bwd_elem = trendline_elem.find(f'{C}backward')
        self._backward = float(bwd_elem.get('val', '0')) if bwd_elem is not None else 0.0

        # intercept
        intercept_elem = trendline_elem.find(f'{C}intercept')
        if intercept_elem is not None:
            self._intercept = float(intercept_elem.get('val', '0'))
        else:
            self._intercept = float('nan')

        # display equation
        disp_eq_elem = trendline_elem.find(f'{C}dispEq')
        self._display_equation = (disp_eq_elem is not None
                                  and disp_eq_elem.get('val', '0') == '1')

        # display R-squared
        disp_rsq_elem = trendline_elem.find(f'{C}dispRSqr')
        self._display_r_squared_value = (disp_rsq_elem is not None
                                         and disp_rsq_elem.get('val', '0') == '1')

        # order (polynomial)
        order_elem = trendline_elem.find(f'{C}order')
        self._order = int(order_elem.get('val', '2')) if order_elem is not None else 2

        # period (moving average)
        period_elem = trendline_elem.find(f'{C}period')
        self._period = int(period_elem.get('val', '2')) if period_elem is not None else 2

    def _to_xml(self) -> ET._Element:
        """Serialize this trendline to a <c:trendline> XML element."""
        from .._internal.pptx.constants import NS
        C = NS.C

        trendline = ET.Element(f'{C}trendline')

        # name (optional)
        if self._trendline_name:
            name_elem = ET.SubElement(trendline, f'{C}name')
            name_elem.text = self._trendline_name

        # trendlineType
        type_elem = ET.SubElement(trendline, f'{C}trendlineType')
        type_elem.set('val', _TYPE_TO_XML[self._trendline_type])

        # order (polynomial only)
        if self._trendline_type == TrendlineType.POLYNOMIAL:
            order_elem = ET.SubElement(trendline, f'{C}order')
            order_elem.set('val', str(self._order))

        # period (moving average only)
        if self._trendline_type == TrendlineType.MOVING_AVERAGE:
            period_elem = ET.SubElement(trendline, f'{C}period')
            period_elem.set('val', str(self._period))

        # forward
        if self._forward != 0.0:
            fwd_elem = ET.SubElement(trendline, f'{C}forward')
            fwd_elem.set('val', _format_float(self._forward))

        # backward
        if self._backward != 0.0:
            bwd_elem = ET.SubElement(trendline, f'{C}backward')
            bwd_elem.set('val', _format_float(self._backward))

        # intercept (only for exp, linear, poly)
        import math
        if not math.isnan(self._intercept):
            if self._trendline_type in (TrendlineType.EXPONENTIAL,
                                        TrendlineType.LINEAR,
                                        TrendlineType.POLYNOMIAL):
                intercept_elem = ET.SubElement(trendline, f'{C}intercept')
                intercept_elem.set('val', _format_float(self._intercept))

        # dispRSqr (always emit to match PowerPoint output)
        disp_rsq = ET.SubElement(trendline, f'{C}dispRSqr')
        disp_rsq.set('val', '1' if self._display_r_squared_value else '0')

        # dispEq (always emit to match PowerPoint output)
        disp_eq = ET.SubElement(trendline, f'{C}dispEq')
        disp_eq.set('val', '1' if self._display_equation else '0')

        return trendline


def _format_float(value: float) -> str:
    """Format float: integers without decimal, otherwise full precision."""
    if value == int(value):
        return str(int(value))
    return str(value)
