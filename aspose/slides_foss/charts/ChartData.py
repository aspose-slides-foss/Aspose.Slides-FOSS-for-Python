from __future__ import annotations
from typing import TYPE_CHECKING

from .ChartDataWorkbook import ChartDataWorkbook
from .ChartSeriesCollection import ChartSeriesCollection
from .ChartCategoryCollection import ChartCategoryCollection
from .ChartSeriesGroupCollection import ChartSeriesGroupCollection
from .ChartDataSourceType import ChartDataSourceType
from .IChartData import IChartData

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .IChartCategoryCollection import IChartCategoryCollection
    from .IChartDataWorkbook import IChartDataWorkbook
    from .IChartSeriesCollection import IChartSeriesCollection
    from .IChartSeriesGroupCollection import IChartSeriesGroupCollection


def _deep_copy_elem(elem):
    """Deep copy an lxml element (without parent)."""
    import copy
    return copy.deepcopy(elem)


class ChartData(IChartData):
    """Represents data used for chart plotting."""

    @property
    def chart_data_workbook(self) -> IChartDataWorkbook:
        return self._workbook

    @property
    def series(self) -> IChartSeriesCollection:
        return self._series

    @property
    def categories(self) -> IChartCategoryCollection:
        return self._categories

    @property
    def series_groups(self) -> IChartSeriesGroupCollection:
        if self._series_groups_dirty:
            self._rebuild_series_groups()
        return self._series_groups

    @property
    def data_source_type(self) -> ChartDataSourceType:
        return ChartDataSourceType.INTERNAL_WORKBOOK

    def get_range(self) -> str:
        """Get the data range string."""
        return self._range or ''

    def set_range(self, formula: str) -> None:
        """Set the data range string."""
        self._range = formula

    def _invalidate_series_groups(self):
        """Mark series groups as needing rebuild."""
        self._series_groups_dirty = True

    def _rebuild_series_groups(self):
        """Build or refresh ChartSeriesGroup objects from plot area XML.

        Each chart-type element (e.g. <c:barChart>) in the plot area becomes
        one group.  Existing group objects are reused (preserving identity)
        and only their series lists are refreshed.
        """
        from .._internal.pptx.constants import NS
        from .._internal.pptx.chart_mappings import (
            get_combinable_group, detect_chart_type_from_xml,
        )
        from .._internal.pptx.chart_part import PRIMARY_AX_IDS
        from .ChartSeriesGroup import ChartSeriesGroup
        from .CombinableSeriesTypesGroup import CombinableSeriesTypesGroup

        C = NS.C
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            self._series_groups = ChartSeriesGroupCollection()
            self._series_groups._init_internal([])
            self._series_groups_dirty = False
            return

        # Index existing groups by their XML element for reuse
        existing = {id(g._ct_elem): g for g in self._series_groups}

        # Collect chart-type elements (skip layout, axes, spPr, dTable)
        skip_local = {'layout', 'catAx', 'valAx', 'dateAx', 'serAx', 'spPr', 'dTable'}
        ct_elements = []
        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local not in skip_local:
                ct_elements.append(child)

        # order → series lookup
        order_to_series = {}
        for s in self._series:
            order_to_series[s.order] = s

        # Collect all orders that have <c:ser> elements in ANY chart-type element,
        # so we don't accidentally grab them in the "newly added" pass.
        xml_assigned_orders = set()
        for ct_elem in ct_elements:
            for ser_elem in ct_elem.findall(f'{C}ser'):
                order_elem = ser_elem.find(f'{C}order')
                if order_elem is not None:
                    xml_assigned_orders.add(int(order_elem.get('val', '-1')))

        assigned_series = set()
        groups = []

        for ct_elem in ct_elements:
            local_tag = ct_elem.tag.split('}')[-1] if '}' in ct_elem.tag else ct_elem.tag

            attrs = {}
            for sub in ct_elem:
                sub_local = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                val = sub.get('val')
                if val is not None and sub_local not in ('ser', 'axId'):
                    attrs[sub_local] = val

            ct_val = detect_chart_type_from_xml(local_tag, attrs)
            comb_name = get_combinable_group(ct_val) if ct_val else None
            try:
                comb_type = CombinableSeriesTypesGroup[comb_name] if comb_name else CombinableSeriesTypesGroup.BAR_CHART_VERT_CLUSTERED
            except KeyError:
                comb_type = CombinableSeriesTypesGroup.BAR_CHART_VERT_CLUSTERED

            # Detect if this group plots on secondary axis
            ax_id_elems = ct_elem.findall(f'{C}axId')
            ax_ids = {e.get('val') for e in ax_id_elems if e.get('val')}
            on_second_axis = bool(ax_ids) and not ax_ids.issubset(PRIMARY_AX_IDS)

            # Collect series for this group
            ser_elems = ct_elem.findall(f'{C}ser')
            group_series = []
            for ser_elem in ser_elems:
                order_elem = ser_elem.find(f'{C}order')
                if order_elem is not None:
                    order = int(order_elem.get('val', '0'))
                    s = order_to_series.get(order)
                    if s is not None:
                        group_series.append(s)
                        assigned_series.add(id(s))

            # Pick up truly new series (no XML element anywhere) matching
            # this group's combinable type.
            for s in self._series:
                if id(s) in assigned_series:
                    continue
                if s.order in xml_assigned_orders:
                    continue  # has XML in another group — don't steal it
                s_comb_name = get_combinable_group(s.type.value if hasattr(s.type, 'value') else str(s.type))
                try:
                    s_comb = CombinableSeriesTypesGroup[s_comb_name] if s_comb_name else None
                except KeyError:
                    s_comb = None
                if s_comb == comb_type:
                    group_series.append(s)
                    assigned_series.add(id(s))

            # Reuse existing group object or create new one
            prev = existing.get(id(ct_elem))
            if prev is not None:
                prev._plot_on_second_axis = on_second_axis
                prev._update_series(group_series)
                groups.append(prev)
            else:
                group = ChartSeriesGroup()
                group._init_internal(
                    ct_elem=ct_elem,
                    chart_part=self._chart_part,
                    combinable_type=comb_type,
                    series_list=group_series,
                    plot_on_second_axis=on_second_axis,
                )
                groups.append(group)

        # Unassigned series fall back to the first group
        if groups:
            for s in self._series:
                if id(s) not in assigned_series:
                    groups[0]._series_readonly._series.append(s)
                    s._parent_series_group = groups[0]

        self._series_groups = ChartSeriesGroupCollection()
        self._series_groups._init_internal(groups)
        self._series_groups_dirty = False

    def _move_series_to_axis(self, series, to_second_axis: bool):
        """Move a series to the primary or secondary axis.

        This modifies the chart XML: moves the <c:ser> element from one
        chart-type element to another (creating the secondary chart-type
        element and secondary axes if needed).
        """
        from .._internal.pptx.constants import NS
        from .._internal.pptx.chart_part import (
            _CAT_AX_ID, _VAL_AX_ID, _VAL_AX_ID_2, _CAT_AX_ID_2,
            _build_cat_ax, _build_val_ax,
        )
        from .._internal.pptx.chart_mappings import get_chart_type_info, AXES_CAT_VAL, AXES_VAL_VAL
        import lxml.etree as ET

        C = NS.C
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return

        # Find the source chart-type element containing this series
        source_ct = None
        source_ser = None
        for ct_elem in self._chart_part.get_all_chart_type_elements():
            for ser_elem in ct_elem.findall(f'{C}ser'):
                order_elem = ser_elem.find(f'{C}order')
                if order_elem is not None and int(order_elem.get('val', '-1')) == series.order:
                    source_ct = ct_elem
                    source_ser = ser_elem
                    break
            if source_ct is not None:
                break

        if source_ct is None:
            return

        # Determine target axis IDs
        ct_val = series.type.value if hasattr(series.type, 'value') else str(series.type)
        info = get_chart_type_info(ct_val)
        if info is None:
            return
        xml_tag, attrs, axis_config, _ = info

        if axis_config == AXES_CAT_VAL:
            if to_second_axis:
                target_ax_ids = [_CAT_AX_ID_2, _VAL_AX_ID_2]
            else:
                target_ax_ids = [_CAT_AX_ID, _VAL_AX_ID]
        elif axis_config == AXES_VAL_VAL:
            if to_second_axis:
                target_ax_ids = [_VAL_AX_ID_2, _CAT_AX_ID_2]
            else:
                target_ax_ids = [_VAL_AX_ID, _VAL_AX_ID_2]
        else:
            # No axes (pie, etc.) — can't move to secondary
            return

        # Check if source already uses target IDs
        source_ax_ids = [e.get('val') for e in source_ct.findall(f'{C}axId')]
        if set(source_ax_ids) == set(target_ax_ids):
            return

        # Find or create a target chart-type element with matching tag and target axis IDs
        target_ct = None
        local_tag = source_ct.tag.split('}')[-1] if '}' in source_ct.tag else source_ct.tag
        for ct_elem in self._chart_part.get_all_chart_type_elements():
            ct_local = ct_elem.tag.split('}')[-1] if '}' in ct_elem.tag else ct_elem.tag
            if ct_local == local_tag:
                ct_ax_ids = {e.get('val') for e in ct_elem.findall(f'{C}axId')}
                if ct_ax_ids == set(target_ax_ids):
                    target_ct = ct_elem
                    break

        if target_ct is None:
            # Create a new chart-type element for the target axis
            target_ct = ET.Element(source_ct.tag)
            # Copy non-ser, non-axId children from source (grouping, barDir, varyColors, etc.)
            for child in source_ct:
                child_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if child_local not in ('ser', 'axId'):
                    target_ct.append(_deep_copy_elem(child))
            # Add axis ID references
            for ax_id in target_ax_ids:
                ax_id_elem = ET.SubElement(target_ct, f'{C}axId')
                ax_id_elem.set('val', ax_id)
            # Insert after source_ct in plot area
            idx = list(plot_area).index(source_ct) + 1
            plot_area.insert(idx, target_ct)

            # Ensure secondary axis elements exist
            if to_second_axis:
                self._ensure_secondary_axes(plot_area, axis_config)

        # Move the <c:ser> element
        source_ct.remove(source_ser)
        # Insert before axId elements in target
        ax_ids = target_ct.findall(f'{C}axId')
        if ax_ids:
            idx = list(target_ct).index(ax_ids[0])
            target_ct.insert(idx, source_ser)
        else:
            target_ct.append(source_ser)

        # If source_ct has no more <c:ser> children, remove it
        if not source_ct.findall(f'{C}ser'):
            plot_area.remove(source_ct)

        # Invalidate series groups so they rebuild with correct axis detection
        self._invalidate_series_groups()

    def _ensure_secondary_axes(self, plot_area, axis_config):
        """Create secondary axis elements in the plot area if not present."""
        from .._internal.pptx.constants import NS
        from .._internal.pptx.chart_part import (
            _CAT_AX_ID, _VAL_AX_ID, _CAT_AX_ID_2, _VAL_AX_ID_2,
            _build_cat_ax, _build_val_ax,
        )
        from .._internal.pptx.chart_mappings import AXES_CAT_VAL, AXES_VAL_VAL

        C = NS.C

        # Check which axis IDs already exist
        existing_ids = set()
        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local in ('catAx', 'valAx', 'dateAx', 'serAx'):
                ax_id_elem = child.find(f'{C}axId')
                if ax_id_elem is not None:
                    existing_ids.add(ax_id_elem.get('val'))

        if axis_config == AXES_CAT_VAL:
            if _CAT_AX_ID_2 not in existing_ids:
                _build_cat_ax(plot_area, _CAT_AX_ID_2, _VAL_AX_ID_2)
                self._configure_secondary_axis(plot_area, _CAT_AX_ID_2, 't')
            if _VAL_AX_ID_2 not in existing_ids:
                _build_val_ax(plot_area, _VAL_AX_ID_2, _CAT_AX_ID_2, 'r')
        elif axis_config == AXES_VAL_VAL:
            if _CAT_AX_ID_2 not in existing_ids:
                _build_val_ax(plot_area, _CAT_AX_ID_2, _VAL_AX_ID_2, 't')
                self._configure_secondary_axis(plot_area, _CAT_AX_ID_2, 't')
            if _VAL_AX_ID_2 not in existing_ids:
                _build_val_ax(plot_area, _VAL_AX_ID_2, _CAT_AX_ID_2, 'r')

    @staticmethod
    def _configure_secondary_axis(plot_area, axis_id, pos, hidden=False):
        """Configure a secondary axis element by its ID."""
        from .._internal.pptx.constants import NS
        C = NS.C
        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local in ('catAx', 'valAx', 'dateAx'):
                ax_id_elem = child.find(f'{C}axId')
                if ax_id_elem is not None and ax_id_elem.get('val') == axis_id:
                    # Update position
                    ax_pos = child.find(f'{C}axPos')
                    if ax_pos is not None:
                        ax_pos.set('val', pos)
                    # Set delete flag to hide secondary cat axis
                    if hidden:
                        delete = child.find(f'{C}delete')
                        if delete is not None:
                            delete.set('val', '1')
                    break

    def _init_internal(self, chart_part: 'ChartPart'):
        self._chart_part = chart_part
        self._workbook = ChartDataWorkbook()
        self._workbook._init_internal(chart_part)
        self._series = ChartSeriesCollection()
        self._series._init_internal(self)
        self._categories = ChartCategoryCollection()
        self._categories._init_internal()
        self._series_groups = ChartSeriesGroupCollection()
        self._series_groups._init_internal([])
        self._series_groups_dirty = True
        self._range = None
