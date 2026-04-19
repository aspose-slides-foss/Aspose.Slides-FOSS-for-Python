from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET

from .LayoutTargetType import LayoutTargetType
from .IChartPlotArea import IChartPlotArea

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart


# OOXML CT_PlotArea child element order (for layout insertion)
_PLOT_AREA_LAYOUT_CHILDREN = [
    'layout',
    # chart-type elements come next (barChart, lineChart, etc.)
    # then axes, spPr, etc.
]


class ChartPlotArea(IChartPlotArea):
    """Represents rectangle where chart should be plotted."""

    def _init_internal(self, chart_part: 'ChartPart', chart):
        """
        Args:
            chart_part: The owning ChartPart.
            chart: The parent Chart object.
        """
        self._chart_part = chart_part
        self._chart = chart
        self._format_cache = None
        return self

    # ------------------------------------------------------------------ #
    #  format (fill / line / effect / 3D)
    # ------------------------------------------------------------------ #

    @property
    def format(self):
        """Returns the format of a plot area. Read-only."""
        if self._format_cache is not None:
            return self._format_cache
        from .Format import Format
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return None
        fmt = Format()
        fmt._init_internal(plot_area, self._chart_part)
        self._format_cache = fmt
        return fmt

    # ------------------------------------------------------------------ #
    #  layout properties (x, y, width, height)
    # ------------------------------------------------------------------ #

    @property
    def x(self) -> float:
        """X coordinate as a fraction of the chart width (0 to 1). Read/write."""
        return self._read_layout_val('x')

    @x.setter
    def x(self, value: float):
        self._write_layout_val('x', value)

    @property
    def y(self) -> float:
        """Y coordinate as a fraction of the chart height (0 to 1). Read/write."""
        return self._read_layout_val('y')

    @y.setter
    def y(self, value: float):
        self._write_layout_val('y', value)

    @property
    def width(self) -> float:
        """Width as a fraction of the chart width (0 to 1). Read/write."""
        return self._read_layout_val('w')

    @width.setter
    def width(self, value: float):
        self._write_layout_val('w', value)

    @property
    def height(self) -> float:
        """Height as a fraction of the chart height (0 to 1). Read/write."""
        return self._read_layout_val('h')

    @height.setter
    def height(self, value: float):
        self._write_layout_val('h', value)

    @property
    def right(self) -> float:
        """Right boundary (x + width). Read-only."""
        return self.x + self.width

    @property
    def bottom(self) -> float:
        """Bottom boundary (y + height). Read-only."""
        return self.y + self.height

    # ------------------------------------------------------------------ #
    #  is_location_autocalculated
    # ------------------------------------------------------------------ #

    @property
    def is_location_autocalculated(self) -> bool:
        """Defines how location should be calculated: True if auto-calculated,
        False if defined by X, Y, Width, Height properties. Read-only."""
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return True
        layout = plot_area.find(f'{NS.C}layout')
        if layout is None:
            return True
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            return True
        # If manualLayout exists but has no positioning children, still auto
        has_position = False
        for tag in ('x', 'y', 'w', 'h'):
            if ml.find(f'{NS.C}{tag}') is not None:
                has_position = True
                break
        return not has_position

    # ------------------------------------------------------------------ #
    #  layout_target_type
    # ------------------------------------------------------------------ #

    @property
    def layout_target_type(self) -> LayoutTargetType:
        """If layout defined manually, specifies whether to layout by inside
        (not including axis/labels) or outside (including axis/labels). Read/write."""
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return LayoutTargetType.INNER
        layout = plot_area.find(f'{NS.C}layout')
        if layout is None:
            return LayoutTargetType.INNER
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            return LayoutTargetType.INNER
        lt = ml.find(f'{NS.C}layoutTarget')
        if lt is not None:
            val = lt.get('val', 'inner')
            if val.lower() == 'outer':
                return LayoutTargetType.OUTER
        return LayoutTargetType.INNER

    @layout_target_type.setter
    def layout_target_type(self, value: LayoutTargetType):
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return
        layout = plot_area.find(f'{NS.C}layout')
        if layout is None:
            layout = ET.SubElement(plot_area, f'{NS.C}layout')
            # Move layout to be the first child of plotArea
            plot_area.remove(layout)
            plot_area.insert(0, layout)
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            ml = ET.SubElement(layout, f'{NS.C}manualLayout')
        lt = ml.find(f'{NS.C}layoutTarget')
        if lt is None:
            # layoutTarget goes before xMode per OOXML spec
            lt = ET.Element(f'{NS.C}layoutTarget')
            ml.insert(0, lt)
        lt.set('val', 'outer' if value == LayoutTargetType.OUTER else 'inner')
        self._chart_part.save()

    # ------------------------------------------------------------------ #
    #  actual layout (read-only, based on manual layout values)
    # ------------------------------------------------------------------ #

    @property
    def actual_x(self) -> float:
        """Actual x location of the chart element. Read-only."""
        return self._read_layout_val('x')

    @property
    def actual_y(self) -> float:
        """Actual top of the chart element. Read-only."""
        return self._read_layout_val('y')

    @property
    def actual_width(self) -> float:
        """Actual width of the chart element. Read-only."""
        return self._read_layout_val('w')

    @property
    def actual_height(self) -> float:
        """Actual height of the chart element. Read-only."""
        return self._read_layout_val('h')

    # ------------------------------------------------------------------ #
    #  chart / slide / presentation references
    # ------------------------------------------------------------------ #

    @property
    def chart(self):
        """Returns the parent chart. Read-only."""
        return self._chart

    @property
    def slide(self):
        """Returns the parent slide. Read-only."""
        if self._chart is not None:
            return getattr(self._chart, '_parent_slide', None)
        return None

    @property
    def presentation(self):
        """Returns the parent presentation. Read-only."""
        slide = self.slide
        if slide is not None:
            return getattr(slide, 'presentation', None)
        return None

    @property
    def as_i_layoutable(self):
        return self

    @property
    def as_i_actual_layout(self):
        return self

    @property
    def as_i_chart_component(self):
        return self

    @property
    def as_i_slide_component(self):
        return self

    @property
    def as_i_presentation_component(self):
        return self

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _read_layout_val(self, attr: str) -> float:
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return 0.0
        layout = plot_area.find(f'{NS.C}layout')
        if layout is None:
            return 0.0
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            return 0.0
        elem = ml.find(f'{NS.C}{attr}')
        if elem is not None:
            try:
                return float(elem.get('val', '0'))
            except ValueError:
                pass
        return 0.0

    # OOXML CT_ManualLayout child order
    _ML_CHILD_ORDER = [
        'layoutTarget', 'xMode', 'yMode', 'wMode', 'hMode', 'x', 'y', 'w', 'h', 'extLst',
    ]

    def _write_layout_val(self, attr: str, value: float):
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return
        layout = plot_area.find(f'{NS.C}layout')
        if layout is None:
            layout = ET.SubElement(plot_area, f'{NS.C}layout')
            # Move layout to be the first child of plotArea
            plot_area.remove(layout)
            plot_area.insert(0, layout)
        ml = layout.find(f'{NS.C}manualLayout')
        if ml is None:
            ml = ET.SubElement(layout, f'{NS.C}manualLayout')
            x_mode = ET.SubElement(ml, f'{NS.C}xMode')
            x_mode.set('val', 'edge')
            y_mode = ET.SubElement(ml, f'{NS.C}yMode')
            y_mode.set('val', 'edge')
        elem = ml.find(f'{NS.C}{attr}')
        if elem is None:
            elem = ET.Element(f'{NS.C}{attr}')
            self._insert_ml_child_ordered(ml, elem, attr, NS.C)
        elem.set('val', str(value))
        self._chart_part.save()

    @staticmethod
    def _insert_ml_child_ordered(ml, new_elem, tag_local, ns_c):
        """Insert element at correct OOXML position in manualLayout."""
        order = ChartPlotArea._ML_CHILD_ORDER
        try:
            target_idx = order.index(tag_local)
        except ValueError:
            ml.append(new_elem)
            return
        for i, child in enumerate(ml):
            child_local = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag
            try:
                child_idx = order.index(child_local)
            except ValueError:
                continue
            if child_idx > target_idx:
                ml.insert(i, new_elem)
                return
        ml.append(new_elem)
