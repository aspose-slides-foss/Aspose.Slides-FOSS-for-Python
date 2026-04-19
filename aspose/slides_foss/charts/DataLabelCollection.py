from __future__ import annotations
from typing import TYPE_CHECKING, Iterator
import lxml.etree as ET
from .IDataLabelCollection import IDataLabelCollection

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .ChartLinesFormat import ChartLinesFormat
    from .ChartSeries import ChartSeries
    from .DataLabel import DataLabel
    from .DataLabelFormat import DataLabelFormat
    from .IChartLinesFormat import IChartLinesFormat
    from .IChartSeries import IChartSeries
    from .IDataLabelFormat import IDataLabelFormat


class DataLabelCollection(IDataLabelCollection):
    """Represents the labels of a chart series.

    Wraps the <c:dLbls> element inside a <c:ser>. Persists across save/load
    because ChartSeries keeps a reference to the element and the sync path
    re-inserts it when rebuilding series XML.
    """

    def _init_internal(self, parent_series: 'ChartSeries', chart_part: 'ChartPart'):
        from .._internal.pptx.constants import NS
        self._parent_series = parent_series
        self._chart_part = chart_part
        self._ns_c = NS.C

    # ---- element helpers ----

    def _c(self, local: str) -> str:
        return f'{self._ns_c}{local}'

    @property
    def _dlbls(self):
        """Return the <c:dLbls> element for this series, or None."""
        return getattr(self._parent_series, '_dlbls_elem', None)

    def _ensure_dlbls(self):
        """Create (and remember on the series) a <c:dLbls> element."""
        existing = self._dlbls
        if existing is not None:
            return existing
        dlbls = ET.Element(self._c('dLbls'))
        self._parent_series._dlbls_elem = dlbls
        return dlbls

    # ---- public properties ----

    @property
    def chart(self):
        """Returns the parent chart."""
        chart_data = getattr(self._parent_series, '_chart_data', None)
        return getattr(chart_data, '_chart', None) if chart_data is not None else None

    @property
    def slide(self):
        c = self.chart
        return c.slide if c is not None else None

    @property
    def presentation(self):
        c = self.chart
        return c.presentation if c is not None else None

    @property
    def parent_series(self) -> 'IChartSeries':
        """Returns the parent series."""
        return self._parent_series

    @property
    def count(self) -> int:
        """Total number of data points in the parent series (each may have a label)."""
        return len(list(self._parent_series.data_points))

    @property
    def count_of_visible_data_labels(self) -> int:
        """Number of labels that would render text.

        A label is visible when it has its own show_* flags set, OR when the
        collection's default format has a show_* flag and no per-point
        <c:delete val='1'/> override.
        """
        default = self.default_data_label_format
        default_visible = any([
            default.show_legend_key, default.show_value, default.show_category_name,
            default.show_series_name, default.show_percentage, default.show_bubble_size,
            default.show_label_value_from_cell,
        ])
        dlbls = self._dlbls
        total = self.count
        if dlbls is None:
            return total if default_visible else 0

        # Collect per-point overrides (hide vs explicit show)
        hidden_idx = set()
        shown_idx = set()
        for dlbl in dlbls.findall(self._c('dLbl')):
            idx_elem = dlbl.find(self._c('idx'))
            if idx_elem is None:
                continue
            try:
                idx = int(idx_elem.get('val', '0'))
            except ValueError:
                continue
            delete = dlbl.find(self._c('delete'))
            if delete is not None and delete.get('val', '0') in ('1', 'true'):
                hidden_idx.add(idx)
                continue
            # Check if this label has any show-flag present (overriding default)
            from .DataLabel import DataLabel as _DL
            dl = _DL()
            dl._init_internal(dlbl, self, idx, self._chart_part)
            fmt = dl.data_label_format
            if any([
                fmt.show_legend_key, fmt.show_value, fmt.show_category_name,
                fmt.show_series_name, fmt.show_percentage, fmt.show_bubble_size,
                fmt.show_label_value_from_cell,
            ]):
                shown_idx.add(idx)

        if default_visible:
            return max(0, total - len(hidden_idx))
        return len(shown_idx - hidden_idx)

    @property
    def is_visible(self) -> bool:
        """True if any show_* flag is enabled on the collection default format."""
        default = self.default_data_label_format
        if any([
            default.show_legend_key, default.show_value, default.show_category_name,
            default.show_series_name, default.show_percentage, default.show_bubble_size,
            default.show_label_value_from_cell,
        ]):
            return True
        # Or any per-point label has any show flag set
        dlbls = self._dlbls
        if dlbls is None:
            return False
        for dlbl in dlbls.findall(self._c('dLbl')):
            for local in ('showLegendKey', 'showVal', 'showCatName',
                          'showSerName', 'showPercent', 'showBubbleSize'):
                e = dlbl.find(self._c(local))
                if e is not None and e.get('val', '0') in ('1', 'true'):
                    return True
        return False

    @property
    def default_data_label_format(self) -> 'IDataLabelFormat':
        """Default format for all data labels in the collection. Read-only."""
        from .DataLabelFormat import DataLabelFormat
        fmt = DataLabelFormat()
        fmt._init_internal(self._ensure_dlbls(), self._chart_part,
                           is_collection_default=True)
        return fmt

    @property
    def leader_lines_format(self) -> 'IChartLinesFormat':
        """Leader lines line/effect format. Read-only."""
        from .ChartLinesFormat import ChartLinesFormat
        dlbls = self._ensure_dlbls()
        ll = dlbls.find(self._c('leaderLines'))
        if ll is None:
            # Insert in correct ordinal position (leaderLines is near end).
            ll = ET.Element(self._c('leaderLines'))
            # Use DataLabelFormat's insertion helper to place correctly.
            from .DataLabelFormat import DataLabelFormat as _DF
            _tmp = _DF()
            _tmp._init_internal(dlbls, self._chart_part, is_collection_default=True)
            _tmp._insert_ordered(ll, 'leaderLines')
        cf = ChartLinesFormat()
        cf._init_internal(ll, self._chart_part)
        return cf

    # ---- hiding / enumeration ----

    def hide(self) -> None:
        """Hide all labels — sets <c:delete val='1'/> on <c:dLbls>."""
        dlbls = self._ensure_dlbls()
        # Remove any default format sub-elements, add delete.
        for child in list(dlbls):
            dlbls.remove(child)
        delete = ET.SubElement(dlbls, self._c('delete'))
        delete.set('val', '1')

    def index_of(self, value: 'DataLabel') -> int:
        """Index of the provided DataLabel in this collection."""
        if value is None:
            return -1
        for i in range(self.count):
            if self[i] is value or self[i]._elem is getattr(value, '_elem', None):
                return i
        return -1

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator['DataLabel']:
        for i in range(self.count):
            yield self[i]

    def __getitem__(self, index: int) -> 'DataLabel':
        if index < 0:
            index = self.count + index
        if index < 0 or index >= self.count:
            raise IndexError('data label index out of range')
        from .DataLabel import DataLabel
        dlbls = self._dlbls
        dlbl_elem = None
        if dlbls is not None:
            for child in dlbls.findall(self._c('dLbl')):
                idx_elem = child.find(self._c('idx'))
                if idx_elem is not None and idx_elem.get('val') == str(index):
                    dlbl_elem = child
                    break
        dl = DataLabel()
        dl._init_internal(dlbl_elem, self, index, self._chart_part)
        return dl
