from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .IDataTable import IDataTable

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart


class DataTable(IDataTable):
    """Represents data table properties."""

    def _init_internal(self, chart_part: 'ChartPart', chart):
        """Initialize from the chart part. Creates <c:dTable> if absent."""
        from .._internal.pptx.constants import NS
        self._chart_part = chart_part
        self._chart = chart
        self._ns_c = NS.C

    def _get_or_create_dtable(self) -> ET._Element:
        """Get or create the <c:dTable> element in <c:plotArea>."""
        plot_area = self._chart_part.get_plot_area()
        dtable = plot_area.find(f'{self._ns_c}dTable')
        if dtable is None:
            # Insert dTable after chart-type elements and before axes
            axis_tags = {'catAx', 'valAx', 'dateAx', 'serAx'}
            insert_idx = len(list(plot_area))
            for i, child in enumerate(plot_area):
                local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if local in axis_tags:
                    insert_idx = i
                    break
            dtable = ET.Element(f'{self._ns_c}dTable')
            # Write default children expected by PowerPoint
            for tag, val in (('showHorzBorder', '0'), ('showVertBorder', '0'),
                             ('showOutline', '0'), ('showKeys', '0')):
                child = ET.SubElement(dtable, f'{self._ns_c}{tag}')
                child.set('val', val)
            plot_area.insert(insert_idx, dtable)
        return dtable

    def _get_dtable(self):
        """Get the <c:dTable> element, or None."""
        plot_area = self._chart_part.get_plot_area()
        return plot_area.find(f'{self._ns_c}dTable') if plot_area is not None else None

    def _get_bool_prop(self, tag_local: str, default: bool = True) -> bool:
        dtable = self._get_dtable()
        if dtable is None:
            return default
        elem = dtable.find(f'{self._ns_c}{tag_local}')
        if elem is None:
            return default
        return elem.get('val', '1') == '1'

    def _set_bool_prop(self, tag_local: str, value: bool):
        dtable = self._get_or_create_dtable()
        elem = dtable.find(f'{self._ns_c}{tag_local}')
        if elem is None:
            elem = ET.SubElement(dtable, f'{self._ns_c}{tag_local}')
        elem.set('val', '1' if value else '0')

    @property
    def has_border_horizontal(self) -> bool:
        """True if the chart data table has horizontal cell borders. Read/write."""
        return self._get_bool_prop('showHorzBorder')

    @has_border_horizontal.setter
    def has_border_horizontal(self, value: bool):
        self._set_bool_prop('showHorzBorder', value)

    @property
    def has_border_vertical(self) -> bool:
        """True if the chart data table has vertical cell borders. Read/write."""
        return self._get_bool_prop('showVertBorder')

    @has_border_vertical.setter
    def has_border_vertical(self, value: bool):
        self._set_bool_prop('showVertBorder', value)

    @property
    def has_border_outline(self) -> bool:
        """True if the chart data table has outline borders. Read/write."""
        return self._get_bool_prop('showOutline')

    @has_border_outline.setter
    def has_border_outline(self, value: bool):
        self._set_bool_prop('showOutline', value)

    @property
    def show_legend_key(self) -> bool:
        """True if the data label legend key is visible. Read/write."""
        return self._get_bool_prop('showKeys', default=False)

    @show_legend_key.setter
    def show_legend_key(self, value: bool):
        self._set_bool_prop('showKeys', value)

    @property
    def chart(self):
        """Returns chart. Read-only."""
        return self._chart
