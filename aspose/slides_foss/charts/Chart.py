from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET

from ..GraphicalObject import GraphicalObject
from .ChartData import ChartData
from .ChartType import ChartType
from .DataTable import DataTable
from .IChart import IChart

if TYPE_CHECKING:
    from .AxesManager import AxesManager
    from .ChartPlotArea import ChartPlotArea
    from .ChartTextFormat import ChartTextFormat
    from .ChartTitle import ChartTitle
    from .ChartWall import ChartWall
    from .DisplayBlanksAsType import DisplayBlanksAsType
    from .Legend import Legend
    from .Rotation3D import Rotation3D
    from .StyleType import StyleType
    from .._internal.pptx.chart_part import ChartPart
    from .._internal.pptx.slide_part import SlidePart
    from .IAxesManager import IAxesManager
    from .IChartData import IChartData
    from .IChartPlotArea import IChartPlotArea
    from .IChartTextFormat import IChartTextFormat
    from .IChartTitle import IChartTitle
    from .IChartWall import IChartWall
    from .IDataTable import IDataTable
    from .ILegend import ILegend
    from .IRotation3D import IRotation3D


# Mapping between DisplayBlanksAsType enum values and XML val attribute
_BLANKS_XML_MAP = {'Gap': 'gap', 'Span': 'span', 'Zero': 'zero'}
_BLANKS_XML_REV = {v: k for k, v in _BLANKS_XML_MAP.items()}


class Chart(IChart, GraphicalObject):
    """Represents a chart on a slide."""

    # ---- chart-level formatting (overrides Shape) ----
    # Chart fill/line/effect live in <c:chartSpace>/<c:spPr>, not graphicFrame spPr.

    def _get_chart_spPr(self):
        """Get or create <c:spPr> as direct child of <c:chartSpace>."""
        from .._internal.pptx.constants import NS
        root = self._chart_part.root
        spPr = root.find(f'{NS.C}spPr')
        if spPr is None:
            spPr = ET.SubElement(root, f'{NS.C}spPr')
        return spPr

    @property
    def fill_format(self):
        from ..FillFormat import FillFormat
        ff = FillFormat()
        ff._init_internal(self._get_chart_spPr(), self._chart_part, None)
        return ff

    @property
    def line_format(self):
        from ..LineFormat import LineFormat
        lf = LineFormat()
        lf._init_internal(self._get_chart_spPr(), self._chart_part, None)
        return lf

    @property
    def effect_format(self):
        from ..EffectFormat import EffectFormat
        ef = EffectFormat()
        ef._init_internal(self._get_chart_spPr(), self._chart_part, None)
        return ef

    @property
    def three_d_format(self):
        from ..ThreeDFormat import ThreeDFormat
        td = ThreeDFormat()
        td._init_internal(self._get_chart_spPr(), self._chart_part, None)
        return td

    # ---- chart_data, type ----

    @property
    def chart_data(self) -> IChartData:
        return self._chart_data

    @property
    def type(self) -> ChartType:
        return self._chart_type

    @type.setter
    def type(self, value: ChartType):
        self._chart_type = value
        # Propagate to every series. At add_chart time this corrects the
        # result of XML-based detection when it can't tell look-alike types
        # apart (BubbleWith3D vs Bubble, cylinder vs Column3D, etc.) because
        # the distinguishing marker lives per-series and hasn't been emitted
        # yet when the freshly-created XML is first scanned.
        data = getattr(self, '_chart_data', None)
        if data is not None:
            for series in data.series:
                series._type = value

    # ---- title ----

    @property
    def has_title(self) -> bool:
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is not None:
            title = chart_elem.find(f'{NS.C}title')
            return title is not None
        return False

    @has_title.setter
    def has_title(self, value: bool):
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is None:
            return
        title = chart_elem.find(f'{NS.C}title')
        if value and title is None:
            title = ET.Element(f'{NS.C}title')
            chart_elem.insert(0, title)
        elif not value and title is not None:
            chart_elem.remove(title)
        atd = chart_elem.find(f'{NS.C}autoTitleDeleted')
        if atd is None:
            atd = ET.SubElement(chart_elem, f'{NS.C}autoTitleDeleted')
        atd.set('val', '0' if value else '1')

    @property
    def chart_title(self) -> 'IChartTitle':
        from .._internal.pptx.constants import NS
        from .ChartTitle import ChartTitle
        chart_elem = self._chart_part.get_chart_element()
        title_elem = chart_elem.find(f'{NS.C}title') if chart_elem is not None else None
        ct = ChartTitle()
        ct._init_internal(title_elem, self._chart_part, chart_elem)
        return ct

    # ---- legend ----

    @property
    def has_legend(self) -> bool:
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is not None:
            legend = chart_elem.find(f'{NS.C}legend')
            return legend is not None
        return False

    @has_legend.setter
    def has_legend(self, value: bool):
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is None:
            return
        legend = chart_elem.find(f'{NS.C}legend')
        if value and legend is None:
            leg = ET.SubElement(chart_elem, f'{NS.C}legend')
            lp = ET.SubElement(leg, f'{NS.C}legendPos')
            lp.set('val', 'b')
            ov = ET.SubElement(leg, f'{NS.C}overlay')
            ov.set('val', '0')
        elif not value and legend is not None:
            chart_elem.remove(legend)
        self._legend_cache = None

    @property
    def legend(self) -> 'ILegend':
        if getattr(self, '_legend_cache', None) is not None:
            return self._legend_cache
        from .._internal.pptx.constants import NS
        from .Legend import Legend
        chart_elem = self._chart_part.get_chart_element()
        legend_elem = chart_elem.find(f'{NS.C}legend') if chart_elem is not None else None
        lg = Legend()
        lg._init_internal(legend_elem, self._chart_part, chart_elem, self)
        self._legend_cache = lg
        return lg

    # ---- data table ----

    @property
    def has_data_table(self) -> bool:
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is not None:
            return plot_area.find(f'{NS.C}dTable') is not None
        return False

    @has_data_table.setter
    def has_data_table(self, value: bool):
        from .._internal.pptx.constants import NS
        plot_area = self._chart_part.get_plot_area()
        if plot_area is None:
            return
        dtable = plot_area.find(f'{NS.C}dTable')
        if value and dtable is None:
            self._ensure_data_table()._get_or_create_dtable()
        elif not value and dtable is not None:
            plot_area.remove(dtable)
            self._data_table = None

    @property
    def chart_data_table(self) -> IDataTable:
        return self._ensure_data_table()

    # ---- plot area & axes ----

    @property
    def plot_area(self) -> 'IChartPlotArea':
        if self._plot_area_cache is None:
            from .ChartPlotArea import ChartPlotArea
            pa = ChartPlotArea()
            pa._init_internal(self._chart_part, self)
            self._plot_area_cache = pa
        return self._plot_area_cache

    @property
    def axes(self) -> 'IAxesManager':
        if self._axes_manager is None:
            from .AxesManager import AxesManager
            self._axes_manager = AxesManager()
            self._axes_manager._init_internal(self._chart_part)
        return self._axes_manager

    # ---- display_blanks_as ----

    @property
    def display_blanks_as(self) -> 'DisplayBlanksAsType':
        from .DisplayBlanksAsType import DisplayBlanksAsType
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is not None:
            elem = chart_elem.find(f'{NS.C}dispBlanksAs')
            if elem is not None:
                # No val attribute = OOXML default "zero"
                xml_val = elem.get('val')
                if xml_val is None:
                    return DisplayBlanksAsType.ZERO
                enum_val = _BLANKS_XML_REV.get(xml_val, 'Zero')
                return DisplayBlanksAsType(enum_val)
        return DisplayBlanksAsType.ZERO

    @display_blanks_as.setter
    def display_blanks_as(self, value: 'DisplayBlanksAsType'):
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is None:
            return
        elem = chart_elem.find(f'{NS.C}dispBlanksAs')
        if elem is None:
            elem = ET.SubElement(chart_elem, f'{NS.C}dispBlanksAs')
        xml_val = _BLANKS_XML_MAP.get(value.value, 'zero')
        # Commercial omits val for default "zero"
        if xml_val == 'zero':
            if 'val' in elem.attrib:
                del elem.attrib['val']
        else:
            elem.set('val', xml_val)

    # ---- plot_visible_cells_only ----

    @property
    def plot_visible_cells_only(self) -> bool:
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is not None:
            elem = chart_elem.find(f'{NS.C}plotVisOnly')
            if elem is not None:
                return elem.get('val', '1') in ('1', 'true')
        return True

    @plot_visible_cells_only.setter
    def plot_visible_cells_only(self, value: bool):
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is None:
            return
        elem = chart_elem.find(f'{NS.C}plotVisOnly')
        if elem is None:
            elem = ET.SubElement(chart_elem, f'{NS.C}plotVisOnly')
        elem.set('val', '1' if value else '0')

    # ---- show_data_labels_over_maximum ----

    @property
    def show_data_labels_over_maximum(self) -> bool:
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is not None:
            elem = chart_elem.find(f'{NS.C}showDLblsOverMax')
            if elem is not None:
                return elem.get('val', '0') in ('1', 'true')
        return False

    @show_data_labels_over_maximum.setter
    def show_data_labels_over_maximum(self, value: bool):
        from .._internal.pptx.constants import NS
        chart_elem = self._chart_part.get_chart_element()
        if chart_elem is None:
            return
        elem = chart_elem.find(f'{NS.C}showDLblsOverMax')
        if elem is None:
            elem = ET.SubElement(chart_elem, f'{NS.C}showDLblsOverMax')
        elem.set('val', '1' if value else '0')

    # ---- has_rounded_corners ----

    @property
    def has_rounded_corners(self) -> bool:
        from .._internal.pptx.constants import NS
        root = self._chart_part.root  # <c:chartSpace>
        elem = root.find(f'{NS.C}roundedCorners')
        if elem is not None:
            return elem.get('val', '0') in ('1', 'true')
        return False

    @has_rounded_corners.setter
    def has_rounded_corners(self, value: bool):
        from .._internal.pptx.constants import NS
        root = self._chart_part.root
        elem = root.find(f'{NS.C}roundedCorners')
        if elem is None:
            elem = ET.SubElement(root, f'{NS.C}roundedCorners')
        elem.set('val', '1' if value else '0')

    # ---- style ----

    @property
    def style(self) -> 'StyleType':
        from .StyleType import StyleType
        from .._internal.pptx.constants import NS
        root = self._chart_part.root
        # Try direct <c:style> first, then mc:Fallback
        elem = root.find(f'{NS.C}style')
        if elem is not None:
            val = elem.get('val', '2')
        else:
            # Look inside mc:AlternateContent/mc:Fallback
            mc_ns = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'
            fallback = root.find(f'{mc_ns}AlternateContent/{mc_ns}Fallback/{NS.C}style')
            val = fallback.get('val', '2') if fallback is not None else '2'
        return StyleType(f'Style{val}')

    @style.setter
    def style(self, value: 'StyleType'):
        from .._internal.pptx.constants import NS
        # Extract numeric part from enum value like 'Style2' -> '2'
        num = value.value.replace('Style', '')
        root = self._chart_part.root
        elem = root.find(f'{NS.C}style')
        if elem is None:
            # Check mc:Fallback
            mc_ns = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'
            fallback = root.find(f'{mc_ns}AlternateContent/{mc_ns}Fallback/{NS.C}style')
            if fallback is not None:
                fallback.set('val', num)
                # Also update c14:style in mc:Choice if present
                choice = root.find(f'{mc_ns}AlternateContent/{mc_ns}Choice')
                if choice is not None:
                    for child in choice:
                        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                        if local == 'style':
                            child.set('val', num)
                            break
            else:
                elem = ET.SubElement(root, f'{NS.C}style')
                elem.set('val', num)
        else:
            elem.set('val', num)

    # ---- text_format ----

    @property
    def text_format(self) -> 'IChartTextFormat':
        if self._text_format_cache is None:
            from .ChartTextFormat import ChartTextFormat
            ctf = ChartTextFormat()
            # Chart-level txPr is on <c:chartSpace>
            ctf._init_internal(self._chart_part.root, self._chart_part)
            self._text_format_cache = ctf
        return self._text_format_cache

    # ---- rotation_3d ----

    @property
    def rotation_3d(self) -> 'IRotation3D':
        if self._rotation_3d_cache is None:
            from .Rotation3D import Rotation3D
            r = Rotation3D()
            r._init_internal(self._chart_part)
            self._rotation_3d_cache = r
        return self._rotation_3d_cache

    # ---- back_wall / side_wall / floor ----

    @property
    def back_wall(self) -> 'IChartWall':
        return self._get_wall('backWall')

    @property
    def side_wall(self) -> 'IChartWall':
        return self._get_wall('sideWall')

    @property
    def floor(self) -> 'IChartWall':
        return self._get_wall('floor')

    _CHART_CHILD_ORDER = (
        'title', 'autoTitleDeleted', 'pivotFmts', 'view3D',
        'floor', 'sideWall', 'backWall', 'plotArea',
        'legend', 'plotVisOnly', 'dispBlanksAs', 'showDLblsOverMax', 'extLst',
    )

    def _get_wall(self, local_name: str) -> 'ChartWall':
        cache_attr = f'_{local_name}_cache'
        cached = getattr(self, cache_attr, None)
        if cached is not None:
            return cached
        from .._internal.pptx.constants import NS
        from .ChartWall import ChartWall
        chart_elem = self._chart_part.get_chart_element()
        wall_elem = chart_elem.find(f'{NS.C}{local_name}')
        if wall_elem is None:
            wall_elem = ET.Element(f'{NS.C}{local_name}')
            target_idx = self._CHART_CHILD_ORDER.index(local_name)
            insert_pos = len(chart_elem)
            for i, child in enumerate(chart_elem):
                child_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if child_local in self._CHART_CHILD_ORDER and \
                        self._CHART_CHILD_ORDER.index(child_local) >= target_idx:
                    insert_pos = i
                    break
            chart_elem.insert(insert_pos, wall_elem)
        cw = ChartWall()
        cw._init_internal(wall_elem, self._chart_part)
        setattr(self, cache_attr, cw)
        return cw

    # ---- chart (self-reference, IChartComponent) ----

    @property
    def chart(self):
        return self

    # ---- validate_chart_layout ----

    def validate_chart_layout(self) -> None:
        pass

    # ---- internal ----

    def _ensure_data_table(self) -> DataTable:
        if not hasattr(self, '_data_table') or self._data_table is None:
            self._data_table = DataTable()
            self._data_table._init_internal(self._chart_part, self)
        return self._data_table

    def _init_internal(self, xml_element, slide_part: 'SlidePart', parent_slide):
        """Initialize from graphicFrame XML element."""
        super()._init_internal(xml_element, slide_part, parent_slide)

        from .._internal.pptx.constants import NS, Elements
        from .._internal.pptx.chart_part import ChartPart
        from ..charts.ChartSeriesCollection import ChartSeriesCollection
        from ..charts.ChartCategoryCollection import ChartCategoryCollection

        # Extract chart relationship ID from graphicData
        graphic_data = xml_element.find(f'.//{NS.A}graphicData')
        chart_ref = graphic_data.find(Elements.C_CHART) if graphic_data is not None else None
        if chart_ref is None:
            raise ValueError("graphicFrame does not contain a chart reference")

        r_id = chart_ref.get(f'{NS.R}id')
        if not r_id:
            raise ValueError("Chart reference missing r:id")

        # Resolve the chart part name from the relationship
        rel = slide_part._rels_manager.get_relationship(r_id)
        if rel is None:
            raise ValueError(f"Relationship {r_id} not found")

        chart_part_name = self._resolve_part_name(slide_part._part_name, rel.target)
        self._chart_part = ChartPart(slide_part._package, chart_part_name)
        self._axes_manager = None
        self._plot_area_cache = None
        self._legend_cache = None
        self._text_format_cache = None
        self._rotation_3d_cache = None

        # Register chart part on slide_part for save
        if not hasattr(slide_part, '_chart_parts'):
            slide_part._chart_parts = []
        if self._chart_part not in slide_part._chart_parts:
            slide_part._chart_parts.append(self._chart_part)

        # Detect chart type
        ct_val = self._chart_part.detect_chart_type()
        self._chart_type = ChartType(ct_val) if ct_val else ChartType.CLUSTERED_COLUMN

        # Initialize chart data
        self._chart_data = ChartData()
        self._chart_data._init_internal(self._chart_part)
        self._chart_data._chart = self

        # Register model for sync on save
        self._chart_part._chart_data_model = self._chart_data

        # Load existing series and categories from chart XML
        self._load_data_from_xml()

    def _load_data_from_xml(self):
        """Parse existing series/categories from chart XML into the object model.

        Iterates all chart-type elements in the plot area so combo charts
        (e.g. barChart + lineChart) load correctly with per-series types.
        """
        from .._internal.pptx.constants import NS
        from .._internal.pptx.chart_part import ChartPart as _CP
        from .DataSourceType import DataSourceType
        from .StringChartValue import StringChartValue
        from .DoubleChartValue import DoubleChartValue
        from .ChartDataPoint import ChartDataPoint
        from .ChartSeries import ChartSeries
        from .Trendline import Trendline
        from .ErrorBarsFormat import ErrorBarsFormat

        C = NS.C
        all_ser_elements = []  # flat list for category parsing

        from .._internal.pptx.chart_mappings import get_chart_type_info

        requested = getattr(self._chart_part, '_requested_chart_type', None)

        for ct_elem in self._chart_part.get_all_chart_type_elements():
            # Detect chart type for this element
            ct_val = _CP._detect_type_from_elem(ct_elem)
            # Freshly-created charts that share an xml_tag with another type
            # (cylinder vs clustered_column_3d, etc.) detect ambiguously — honor
            # the originally requested type when compatible.
            if requested and ct_val:
                info_req = get_chart_type_info(requested)
                info_det = get_chart_type_info(ct_val)
                if info_req and info_det and info_req[0] == info_det[0]:
                    ct_val = requested
            try:
                elem_chart_type = ChartType(ct_val) if ct_val else self._chart_type
            except ValueError:
                elem_chart_type = self._chart_type

            for ser_elem in ct_elem.findall(f'{C}ser'):
                all_ser_elements.append(ser_elem)

                # Series name
                tx = ser_elem.find(f'{C}tx')
                name_val = StringChartValue()
                if tx is not None:
                    str_ref = tx.find(f'{C}strRef')
                    if str_ref is not None:
                        cache = str_ref.find(f'{C}strCache')
                        if cache is not None:
                            pt = cache.find(f'{C}pt')
                            if pt is not None:
                                v = pt.find(f'{C}v')
                                if v is not None and v.text:
                                    name_val._init_internal(DataSourceType.STRING_LITERALS, literal=v.text)
                if name_val._data is None:
                    name_val._init_internal(DataSourceType.STRING_LITERALS, literal='')

                # Order
                order_elem = ser_elem.find(f'{C}order')
                order = int(order_elem.get('val', '0')) if order_elem is not None else 0

                series = ChartSeries()
                series._init_internal(name=name_val, chart_type=elem_chart_type, order=order)

                # Preserve existing data labels <c:dLbls> across save rebuilds.
                dlbls = ser_elem.find(f'{C}dLbls')
                if dlbls is not None:
                    ser_elem.remove(dlbls)
                    series._dlbls_elem = dlbls

                # Preserve series-level <c:marker> and per-point <c:dPt> across
                # save rebuilds.
                marker = ser_elem.find(f'{C}marker')
                if marker is not None:
                    ser_elem.remove(marker)
                    series._marker_elem = marker
                for dpt in ser_elem.findall(f'{C}dPt'):
                    idx_e = dpt.find(f'{C}idx')
                    if idx_e is None:
                        continue
                    try:
                        i = int(idx_e.get('val', '0'))
                    except ValueError:
                        continue
                    ser_elem.remove(dpt)
                    series._dpt_elems[i] = dpt

                # Restore per-point value_from_cell state from
                # <c:ser>/<c:extLst>/<c:ext uri={02D57815-...}>/<c15:datalabelsRange>.
                _restore_value_from_cell(self._chart_data, series, ser_elem)

                # Parse data points from <c:val> or <c:yVal>
                val_elem = ser_elem.find(f'{C}val')
                is_xy_series = False
                if val_elem is None:
                    val_elem = ser_elem.find(f'{C}yVal')
                    if val_elem is not None:
                        is_xy_series = True
                if val_elem is not None:
                    num_ref = val_elem.find(f'{C}numRef')
                    if num_ref is not None:
                        cache = num_ref.find(f'{C}numCache')
                        if cache is not None:
                            for pt in cache.findall(f'{C}pt'):
                                v = pt.find(f'{C}v')
                                if v is not None and v.text:
                                    try:
                                        val = float(v.text)
                                        if val == int(val):
                                            val = int(val)
                                    except ValueError:
                                        val = 0
                                    dv = DoubleChartValue()
                                    dv._init_internal(DataSourceType.DOUBLE_LITERALS, literal=float(val))
                                    dp = ChartDataPoint()
                                    # For scatter/bubble, also populate y_value so
                                    # the emitter round-trips through the xy path.
                                    y_val = None
                                    if is_xy_series:
                                        y_val = DoubleChartValue()
                                        y_val._init_internal(
                                            DataSourceType.DOUBLE_LITERALS,
                                            literal=float(val),
                                        )
                                    dp._init_internal(
                                        index=len(series.data_points._points),
                                        value=dv,
                                        y_value=y_val,
                                        parent_collection=series.data_points,
                                    )
                                    series.data_points._points.append(dp)

                # Parse X values from <c:xVal> (scatter/bubble) into dp.x_value
                if is_xy_series:
                    self._load_xvalues_into_points(series, ser_elem)

                # Parse bubble sizes from <c:bubbleSize> into dp.bubble_size
                self._load_bubble_sizes_into_points(series, ser_elem)

                # Parse trendlines
                series._trend_lines._chart_part = self._chart_part
                for tl_elem in ser_elem.findall(f'{C}trendline'):
                    tl = Trendline()
                    tl._init_from_xml(tl_elem, chart_part=self._chart_part)
                    series._trend_lines._trendlines.append(tl)

                # Parse error bars
                for eb_elem in ser_elem.findall(f'{C}errBars'):
                    eb = ErrorBarsFormat()
                    eb._init_from_xml(eb_elem, chart_part=self._chart_part)
                    if eb.direction == 'x':
                        series._error_bars_x = eb
                    else:
                        series._error_bars_y = eb

                # Distribute custom error bar values to data points
                self._distribute_custom_error_values(series)

                series._chart_data = self._chart_data
                self._chart_data.series._series.append(series)

        # Parse categories — find first series that has <c:cat> or <c:xVal>
        cat_elem = None
        for ser_elem in all_ser_elements:
            cat_elem = ser_elem.find(f'{C}cat')
            if cat_elem is None:
                cat_elem = ser_elem.find(f'{C}xVal')
            if cat_elem is not None:
                break
        if cat_elem is not None:
            str_ref = cat_elem.find(f'{C}strRef')
            if str_ref is not None:
                cache = str_ref.find(f'{C}strCache')
                if cache is not None:
                    for pt in cache.findall(f'{C}pt'):
                        v = pt.find(f'{C}v')
                        if v is not None and v.text:
                            from .ChartCategory import ChartCategory
                            cat = ChartCategory()
                            cat._init_internal(literal=v.text,
                                               parent_collection=self._chart_data.categories)
                            self._chart_data.categories._categories.append(cat)

    @staticmethod
    def _load_xvalues_into_points(series, ser_elem):
        """Populate dp.x_value on each data point from <c:xVal>.

        Handles both <c:numRef>/<c:numCache> and <c:strRef>/<c:strCache>.
        Points are expected to already exist in series.data_points._points.
        """
        from .._internal.pptx.constants import NS
        from .DataSourceType import DataSourceType
        from .StringOrDoubleChartValue import StringOrDoubleChartValue
        C = NS.C

        points = series.data_points._points
        if not points:
            return
        x_elem = ser_elem.find(f'{C}xVal')
        if x_elem is None:
            return

        num_ref = x_elem.find(f'{C}numRef')
        if num_ref is not None:
            cache = num_ref.find(f'{C}numCache')
            if cache is not None:
                for pt in cache.findall(f'{C}pt'):
                    idx = int(pt.get('idx', '0'))
                    v = pt.find(f'{C}v')
                    if v is not None and v.text and idx < len(points):
                        try:
                            val = float(v.text)
                        except ValueError:
                            continue
                        xv = StringOrDoubleChartValue()
                        xv._init_internal(DataSourceType.DOUBLE_LITERALS, literal=val)
                        points[idx]._x_value = xv
            return

        str_ref = x_elem.find(f'{C}strRef')
        if str_ref is not None:
            cache = str_ref.find(f'{C}strCache')
            if cache is not None:
                for pt in cache.findall(f'{C}pt'):
                    idx = int(pt.get('idx', '0'))
                    v = pt.find(f'{C}v')
                    if v is not None and v.text is not None and idx < len(points):
                        xv = StringOrDoubleChartValue()
                        xv._init_internal(DataSourceType.STRING_LITERALS, literal=v.text)
                        points[idx]._x_value = xv

    @staticmethod
    def _load_bubble_sizes_into_points(series, ser_elem):
        """Populate dp.bubble_size on each data point from <c:bubbleSize>."""
        from .._internal.pptx.constants import NS
        from .DataSourceType import DataSourceType
        from .DoubleChartValue import DoubleChartValue
        C = NS.C

        points = series.data_points._points
        if not points:
            return
        bub_elem = ser_elem.find(f'{C}bubbleSize')
        if bub_elem is None:
            return
        num_ref = bub_elem.find(f'{C}numRef')
        if num_ref is None:
            return
        cache = num_ref.find(f'{C}numCache')
        if cache is None:
            return
        for pt in cache.findall(f'{C}pt'):
            idx = int(pt.get('idx', '0'))
            v = pt.find(f'{C}v')
            if v is not None and v.text and idx < len(points):
                try:
                    val = float(v.text)
                except ValueError:
                    continue
                bs = DoubleChartValue()
                bs._init_internal(DataSourceType.DOUBLE_LITERALS, literal=val)
                points[idx]._bubble_size = bs

    @staticmethod
    def _distribute_custom_error_values(series):
        """Copy custom error bar values from ErrorBarsFormat lists into per-data-point objects."""
        from .ErrorBarValueType import ErrorBarValueType
        points = series.data_points._points
        for eb in (series._error_bars_x, series._error_bars_y):
            if eb is None or eb.value_type != ErrorBarValueType.CUSTOM:
                continue
            d = eb.direction  # 'x' or 'y'
            for i, dp in enumerate(points):
                cv = dp.error_bars_custom_values
                if d == 'x':
                    if i < len(eb.custom_plus_values):
                        cv.x_plus.as_literal_double = eb.custom_plus_values[i]
                    if i < len(eb.custom_minus_values):
                        cv.x_minus.as_literal_double = eb.custom_minus_values[i]
                else:
                    if i < len(eb.custom_plus_values):
                        cv.y_plus.as_literal_double = eb.custom_plus_values[i]
                    if i < len(eb.custom_minus_values):
                        cv.y_minus.as_literal_double = eb.custom_minus_values[i]

    @staticmethod
    def _resolve_part_name(source_part: str, target: str) -> str:
        if target.startswith('/'):
            return target.lstrip('/')
        base_dir = source_part.rsplit('/', 1)[0] if '/' in source_part else ''
        parts = (base_dir + '/' + target).split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)


_C15_NS = 'http://schemas.microsoft.com/office/drawing/2012/chart'
_DATALABELS_RANGE_EXT_URI = '{02D57815-91ED-43cb-92C2-25804820EDAC}'


def _restore_value_from_cell(chart_data, series, ser_elem) -> None:
    """Parse <c:ser>/<c:extLst>/<c:ext uri={02D57815-...}>/<c15:datalabelsRange>
    and populate series._value_from_cell_cells mapping.

    The ext element is removed from ser_elem since the series is rebuilt on
    save and the cells map drives regeneration.
    """
    from .._internal.pptx.constants import NS
    from .ChartDataCell import ChartDataCell

    C = NS.C
    ext_lst = ser_elem.find(f'{C}extLst')
    if ext_lst is None:
        return
    target_ext = None
    for ext in ext_lst.findall(f'{C}ext'):
        if ext.get('uri') == _DATALABELS_RANGE_EXT_URI:
            target_ext = ext
            break
    if target_ext is None:
        return
    dlr = target_ext.find(f'{{{_C15_NS}}}datalabelsRange')
    if dlr is None:
        return

    f_elem = dlr.find(f'{{{_C15_NS}}}f')
    formula = f_elem.text if f_elem is not None else ''
    cells = _parse_range_formula(formula)
    if not cells:
        return

    workbook = None
    if chart_data is not None:
        try:
            workbook = chart_data.chart_data_workbook
        except AttributeError:
            workbook = None
    if workbook is None:
        return

    mapping = {}
    cache = dlr.find(f'{{{_C15_NS}}}dlblRangeCache')
    pt_count = 0
    if cache is not None:
        pc = cache.find(f'{C}ptCount')
        if pc is not None:
            try:
                pt_count = int(pc.get('val', '0'))
            except ValueError:
                pt_count = 0
    pts = cache.findall(f'{C}pt') if cache is not None else []
    # Map sequential cells to data point indexes via pt elements or range length.
    limit = pt_count if pt_count else max(len(cells), len(pts))
    for i in range(min(limit, len(cells))):
        row, col = cells[i]
        cell = ChartDataCell()
        cell._init_internal(workbook, worksheet_index=0, row=row, column=col)
        mapping[i] = cell

    series._value_from_cell_cells = mapping
    ext_lst.remove(target_ext)
    if len(ext_lst) == 0:
        ser_elem.remove(ext_lst)


def _parse_range_formula(formula: str) -> list[tuple[int, int]]:
    """Parse 'Sheet1!$G$2:$G$5' or 'Sheet1!$G$2' (or comma-joined) into
    a list of (row, col) tuples in 0-based indices.
    """
    if not formula:
        return []
    result = []
    for part in formula.split(','):
        part = part.strip()
        if '!' in part:
            _, ref = part.split('!', 1)
        else:
            ref = part
        ref = ref.replace('$', '')
        if ':' in ref:
            s, e = ref.split(':', 1)
            sc, sr = _split_cell_ref(s)
            ec, er = _split_cell_ref(e)
            if sc == ec:
                for r in range(sr, er + 1):
                    result.append((r, sc))
            else:
                # Non-column range: fall back to start/end only
                result.append((sr, sc))
                result.append((er, ec))
        else:
            c, r = _split_cell_ref(ref)
            result.append((r, c))
    return result


def _split_cell_ref(ref: str) -> tuple[int, int]:
    """Parse 'G2' → (col=6, row=1) in 0-based indices."""
    letters = ''
    digits = ''
    for ch in ref:
        if ch.isalpha():
            letters += ch
        elif ch.isdigit():
            digits += ch
    col = 0
    for ch in letters.upper():
        col = col * 26 + (ord(ch) - ord('A') + 1)
    col -= 1
    row = int(digits) - 1 if digits else 0
    return col, row
