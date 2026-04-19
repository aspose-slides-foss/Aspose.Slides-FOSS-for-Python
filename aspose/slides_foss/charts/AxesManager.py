from __future__ import annotations
from typing import TYPE_CHECKING
from .IAxesManager import IAxesManager

if TYPE_CHECKING:
    from .Axis import Axis
    from .._internal.pptx.chart_part import ChartPart
    from .IAxis import IAxis

# Axis XML element local names
_AXIS_TAGS = frozenset({'catAx', 'valAx', 'dateAx', 'serAx'})

# Well-known axis IDs (must match chart_part.py constants)
_CAT_AX_ID = '111111111'
_VAL_AX_ID = '222222222'
_VAL_AX_ID_2 = '333333333'
_CAT_AX_ID_2 = '444444444'


class AxesManager(IAxesManager):
    """Provides access to chart axes."""

    @property
    def horizontal_axis(self) -> IAxis:
        """Gets the chart's horizontal axis (primary category or first value axis). Read-only."""
        return self._horizontal

    @property
    def vertical_axis(self) -> IAxis:
        """Gets the chart's vertical axis (primary value axis). Read-only."""
        return self._vertical

    @property
    def secondary_horizontal_axis(self) -> IAxis:
        """Gets the chart's secondary horizontal axis. Read-only."""
        return self._secondary_horizontal

    @property
    def secondary_vertical_axis(self) -> IAxis:
        """Gets the chart's secondary vertical axis. Read-only."""
        return self._secondary_vertical

    @property
    def series_axis(self) -> IAxis:
        """Gets the chart's series axis. Read-only."""
        return self._series_axis

    # ------------------------------------------------------------------ #
    #  _init_internal
    # ------------------------------------------------------------------ #

    def _init_internal(self, chart_part: 'ChartPart'):
        """
        Build Axis objects from all axis elements in the plot area.

        Strategy:
        - Collect all <c:catAx>, <c:valAx>, <c:dateAx>, <c:serAx> elements
        - Identify primary vs secondary by axis ID and position
        - Map to horizontal/vertical/secondary slots
        """
        from .Axis import Axis
        from .._internal.pptx.constants import NS

        self._chart_part = chart_part
        self._horizontal = None
        self._vertical = None
        self._secondary_horizontal = None
        self._secondary_vertical = None
        self._series_axis = None
        self._axes_by_id: dict[str, Axis] = {}

        plot_area = chart_part.get_plot_area()
        if plot_area is None:
            return

        C = NS.C

        # Collect all axis elements
        cat_axes = []  # catAx or dateAx elements
        val_axes = []  # valAx elements
        ser_axes = []  # serAx elements

        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local in ('catAx', 'dateAx'):
                cat_axes.append(child)
            elif local == 'valAx':
                val_axes.append(child)
            elif local == 'serAx':
                ser_axes.append(child)

        # Create Axis objects for all found axes and index by ID
        all_ax_elems = cat_axes + val_axes + ser_axes
        for ax_elem in all_ax_elems:
            axis = Axis()
            axis._init_internal(ax_elem, chart_part)
            ax_id = axis._axis_id
            if ax_id:
                self._axes_by_id[ax_id] = axis

        # Determine which chart-type elements reference which axis IDs
        # to figure out primary vs secondary axis sets
        primary_ax_ids = set()
        secondary_ax_ids = set()

        ct_elements = chart_part.get_all_chart_type_elements()
        for i, ct_elem in enumerate(ct_elements):
            ax_id_elems = ct_elem.findall(f'{C}axId')
            ids = [e.get('val') for e in ax_id_elems if e.get('val')]
            if i == 0:
                primary_ax_ids.update(ids)
            else:
                # If same IDs as primary, it's still primary group
                # If different IDs, it's secondary
                if ids and not set(ids).issubset(primary_ax_ids):
                    secondary_ax_ids.update(ids)
                else:
                    primary_ax_ids.update(ids)

        # Assign cat/val axes to horizontal/vertical
        # Primary: first catAx → horizontal, first valAx with primary ID → vertical
        # Secondary: remaining catAx → secondary_horizontal, valAx with secondary ID → secondary_vertical

        for ax_elem in cat_axes:
            axis = self._get_axis_for_elem(ax_elem)
            if axis is None:
                continue
            ax_id = axis._axis_id
            if ax_id in secondary_ax_ids and self._secondary_horizontal is None:
                self._secondary_horizontal = axis
            elif self._horizontal is None:
                self._horizontal = axis
            elif self._secondary_horizontal is None:
                self._secondary_horizontal = axis

        for ax_elem in val_axes:
            axis = self._get_axis_for_elem(ax_elem)
            if axis is None:
                continue
            ax_id = axis._axis_id
            pos_elem = ax_elem.find(f'{C}axPos')
            pos = pos_elem.get('val', '') if pos_elem is not None else ''

            if ax_id in secondary_ax_ids and self._secondary_vertical is None:
                self._secondary_vertical = axis
            elif self._vertical is None:
                self._vertical = axis
            elif self._secondary_vertical is None:
                self._secondary_vertical = axis

        # For val-val charts (scatter/bubble): first valAx is horizontal, second is vertical
        if self._horizontal is None and len(val_axes) >= 2:
            ax1 = self._get_axis_for_elem(val_axes[0])
            ax2 = self._get_axis_for_elem(val_axes[1])
            if ax1 is not None and ax2 is not None:
                # The one at bottom is horizontal
                from .AxisPositionType import AxisPositionType
                if ax1.position in (AxisPositionType.BOTTOM, AxisPositionType.TOP):
                    self._horizontal = ax1
                    self._vertical = ax2
                else:
                    self._horizontal = ax2
                    self._vertical = ax1

        # Series axis
        if ser_axes:
            self._series_axis = self._get_axis_for_elem(ser_axes[0])

    def _get_axis_for_elem(self, ax_elem) -> Axis:
        """Look up the Axis object for a given XML element."""
        from .._internal.pptx.constants import NS
        ax_id_elem = ax_elem.find(f'{NS.C}axId')
        if ax_id_elem is not None:
            ax_id = ax_id_elem.get('val', '')
            return self._axes_by_id.get(ax_id)
        return None

    def get_axis_by_id(self, axis_id: str) -> Axis:
        """Get an Axis object by its ID string."""
        return self._axes_by_id.get(axis_id)
