"""
Chart part management for PPTX packages.

Manages ppt/charts/chartN.xml — the chart definition XML including
series data, categories, and the embedded XLSX workbook reference.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import NS, NAMESPACES
from ..opc.relationships import RelationshipsManager, REL_TYPES
from ..opc.content_types import ContentTypesManager, CONTENT_TYPES
from .chart_mappings import get_chart_type_info, get_bar3d_shape, detect_chart_type_from_xml, AXES_CAT_VAL, AXES_CAT_VAL_SER, AXES_VAL_VAL

if TYPE_CHECKING:
    from ..opc.opc_package import OpcPackage
    from ..xlsx.xlsx_package import XlsxPackage

C_NS = NS.C
A_NS = NS.A
R_NS = NS.R

CHART_NSMAP = {
    'c': NAMESPACES['c'],
    'a': NAMESPACES['a'],
    'r': NAMESPACES['r'],
}

# Chart XML element tags
_CHART_SPACE = f'{C_NS}chartSpace'
_CHART = f'{C_NS}chart'
_PLOT_AREA = f'{C_NS}plotArea'
_LAYOUT = f'{C_NS}layout'
_SER = f'{C_NS}ser'
_IDX = f'{C_NS}idx'
_ORDER = f'{C_NS}order'
_TX = f'{C_NS}tx'
_CAT = f'{C_NS}cat'
_VAL = f'{C_NS}val'
_X_VAL = f'{C_NS}xVal'
_Y_VAL = f'{C_NS}yVal'
_BUBBLE_SIZE = f'{C_NS}bubbleSize'
_STR_REF = f'{C_NS}strRef'
_NUM_REF = f'{C_NS}numRef'
_STR_CACHE = f'{C_NS}strCache'
_NUM_CACHE = f'{C_NS}numCache'
_F = f'{C_NS}f'
_V = f'{C_NS}v'
_PT = f'{C_NS}pt'
_PT_COUNT = f'{C_NS}ptCount'
_FORMAT_CODE = f'{C_NS}formatCode'
_AX_ID = f'{C_NS}axId'
_CAT_AX = f'{C_NS}catAx'
_VAL_AX = f'{C_NS}valAx'
_SER_AX = f'{C_NS}serAx'
_MAJOR_TICK = f'{C_NS}majorTickMark'
_MINOR_TICK = f'{C_NS}minorTickMark'
_SCALING = f'{C_NS}scaling'
_ORIENTATION = f'{C_NS}orientation'
_DELETE = f'{C_NS}delete'
_AX_POS = f'{C_NS}axPos'
_CROSS_AX = f'{C_NS}crossAx'
_EXTERNAL_DATA = f'{C_NS}externalData'
_AUTO_UPDATE = f'{C_NS}autoUpdate'
_DATE1904 = f'{C_NS}date1904'
_LANG = f'{C_NS}lang'
_ROUND_MODE = f'{C_NS}roundedCorners'
_LEGEND = f'{C_NS}legend'
_LEGEND_POS = f'{C_NS}legendPos'
_OVERLAY = f'{C_NS}overlay'

# Axis IDs
_CAT_AX_ID = '111111111'
_VAL_AX_ID = '222222222'
_VAL_AX_ID_2 = '333333333'  # secondary valAx
_CAT_AX_ID_2 = '444444444'  # secondary catAx
_SER_AX_ID = '555555555'    # series (depth) axis for 3D surface / bar3D standard

# Sets for quick membership checks
PRIMARY_AX_IDS = frozenset({_CAT_AX_ID, _VAL_AX_ID})
SECONDARY_AX_IDS = frozenset({_CAT_AX_ID_2, _VAL_AX_ID_2})


class ChartPart:
    """Manages a chart part (ppt/charts/chartN.xml) and its embedded XLSX."""

    def __init__(self, package: OpcPackage, part_name: str):
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._rels_manager = RelationshipsManager(package, part_name)
        self._xlsx: Optional['XlsxPackage'] = None
        self._xlsx_dirty = False
        self._chart_data_model = None  # Set by Chart._init_internal for sync on save
        self._load()

    def _load(self) -> None:
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Chart part not found: {self._part_name}")

    @property
    def root(self) -> ET._Element:
        return self._root

    @property
    def rels_manager(self) -> RelationshipsManager:
        return self._rels_manager

    # --- Chart structure accessors ---

    def get_chart_element(self) -> Optional[ET._Element]:
        """Get the <c:chart> element."""
        return self._root.find(_CHART)

    def get_plot_area(self) -> Optional[ET._Element]:
        """Get the <c:plotArea> element."""
        chart = self.get_chart_element()
        if chart is not None:
            return chart.find(_PLOT_AREA)
        return None

    _SKIP_LOCAL = frozenset({'layout', 'catAx', 'valAx', 'dateAx', 'serAx', 'spPr', 'dTable'})

    def get_chart_type_element(self) -> Optional[ET._Element]:
        """Get the *first* chart-type element (e.g., <c:barChart>) from plotArea."""
        elems = self.get_all_chart_type_elements()
        return elems[0] if elems else None

    def get_all_chart_type_elements(self) -> list[ET._Element]:
        """Get all chart-type elements from plotArea (one per series group)."""
        plot_area = self.get_plot_area()
        if plot_area is None:
            return []
        result = []
        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local not in self._SKIP_LOCAL:
                result.append(child)
        return result

    def detect_chart_type(self) -> Optional[str]:
        """Detect ChartType enum value from the loaded XML."""
        ct_elem = self.get_chart_type_element()
        if ct_elem is None:
            return None
        detected = self._detect_type_from_elem(ct_elem)
        # For freshly created charts, series haven't been emitted yet so
        # BubbleWith3D / Bubble look identical. Honor the requested type.
        requested = getattr(self, '_requested_chart_type', None)
        if requested and detected:
            info_req = get_chart_type_info(requested)
            info_det = get_chart_type_info(detected)
            if info_req and info_det and info_req[0] == info_det[0]:
                return requested
        return detected

    @staticmethod
    def _detect_type_from_elem(ct_elem: ET._Element) -> Optional[str]:
        local_tag = ct_elem.tag.split('}')[-1] if '}' in ct_elem.tag else ct_elem.tag
        attrs = {}
        for child in ct_elem:
            child_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            val = child.get('val')
            if val is not None and child_local not in ('ser', 'axId'):
                attrs[child_local] = val
        # bubble3D can also live inside each <c:ser> (PowerPoint emits it there).
        # Promote it into attrs so BubbleWith3D is detected.
        if local_tag == 'bubbleChart' and 'bubble3D' not in attrs:
            for ser_elem in ct_elem.findall(_SER):
                b3d = ser_elem.find(f'{C_NS}bubble3D')
                if b3d is not None and b3d.get('val') == '1':
                    attrs['bubble3D'] = '1'
                    break
        # <c:shape> for bar3DChart cylinder/cone/pyramid. May appear on the
        # chart-type element or on any series. Promote into attrs so the
        # detector can pick cylinder/cone/pyramid over plain bar3D.
        if local_tag == 'bar3DChart' and 'shape' not in attrs:
            for ser_elem in ct_elem.findall(_SER):
                sh = ser_elem.find(f'{C_NS}shape')
                if sh is not None and sh.get('val'):
                    attrs['shape'] = sh.get('val')
                    break
        return detect_chart_type_from_xml(local_tag, attrs)

    def get_series_elements(self) -> list[ET._Element]:
        """Get all <c:ser> elements across all chart-type elements."""
        result = []
        for ct_elem in self.get_all_chart_type_elements():
            result.extend(ct_elem.findall(_SER))
        return result

    # --- Embedded XLSX ---

    def get_xlsx_part_name(self) -> Optional[str]:
        """Get the part name of the embedded XLSX."""
        rels = self._rels_manager.get_relationships_by_type(REL_TYPES['package'])
        if not rels:
            return None
        target = rels[0].target
        # Resolve relative path
        base_dir = self._part_name.rsplit('/', 1)[0] if '/' in self._part_name else ''
        parts = (base_dir + '/' + target).split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)

    def get_xlsx(self) -> 'XlsxPackage':
        """Get the embedded XlsxPackage (lazy-loaded)."""
        if self._xlsx is None:
            from ..xlsx.xlsx_package import XlsxPackage
            xlsx_part_name = self.get_xlsx_part_name()
            if xlsx_part_name:
                xlsx_bytes = self._package.get_part(xlsx_part_name)
                if xlsx_bytes:
                    self._xlsx = XlsxPackage.from_bytes(xlsx_bytes)
                else:
                    self._xlsx = XlsxPackage.create_new()
                    self._xlsx_dirty = True
            else:
                self._xlsx = XlsxPackage.create_new()
                self._xlsx_dirty = True
        return self._xlsx

    def mark_xlsx_dirty(self):
        """Mark the embedded XLSX as needing save."""
        self._xlsx_dirty = True

    # --- Sync model to XML ---

    def sync_from_model(self, chart_data) -> None:
        """
        Write series/categories/data points from the public API model back
        to chart XML.  Handles combo charts: series with different types are
        placed into separate chart-type elements in the plot area.

        Series that have plot_on_second_axis=True (via their parent group)
        are placed in a separate chart-type element referencing secondary axes.
        """
        plot_area = self.get_plot_area()
        if plot_area is None:
            return

        from ..xlsx.cell_reference import format_cell_ref

        categories = list(chart_data.categories)
        series_list = list(chart_data.series)

        # Force series group rebuild to ensure back-references are current
        if hasattr(chart_data, '_series_groups_dirty') and chart_data._series_groups_dirty:
            _ = chart_data.series_groups

        # Group series by (xml_tag, on_second_axis)
        groups: dict[tuple[str, bool], list] = {}
        for si, series in enumerate(series_list):
            ct_val = series.type.value if hasattr(series.type, 'value') else str(series.type)
            info = get_chart_type_info(ct_val)
            xml_tag = info[0] if info else 'barChart'
            on_second = (hasattr(series, '_parent_series_group')
                         and series._parent_series_group is not None
                         and series._parent_series_group.plot_on_second_axis)
            key = (xml_tag, on_second)
            groups.setdefault(key, []).append((si, series))

        # Existing chart-type elements by (xml_tag, axis_key)
        existing_ct: dict[tuple[str, bool], ET._Element] = {}
        for ct_elem in self.get_all_chart_type_elements():
            local = ct_elem.tag.split('}')[-1] if '}' in ct_elem.tag else ct_elem.tag
            ax_id_elems = ct_elem.findall(_AX_ID)
            ax_ids = {e.get('val') for e in ax_id_elems if e.get('val')}
            on_second = bool(ax_ids) and not ax_ids.issubset(PRIMARY_AX_IDS)
            existing_ct[(local, on_second)] = ct_elem

        used_keys = set()

        # Find the insertion anchor in plot area (first axis element)
        pa_insert_before = None
        for child in plot_area:
            local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if local in ('catAx', 'valAx', 'dateAx', 'serAx'):
                pa_insert_before = child
                break

        last_si = len(series_list) - 1

        for (xml_tag, on_second), group_series in groups.items():
            used_keys.add((xml_tag, on_second))

            if (xml_tag, on_second) in existing_ct:
                ct_elem = existing_ct[(xml_tag, on_second)]
                # Remove old ser elements
                for old_ser in ct_elem.findall(_SER):
                    ct_elem.remove(old_ser)
            else:
                # Create a new chart-type element
                first_series = group_series[0][1]
                ct_val = first_series.type.value if hasattr(first_series.type, 'value') else str(first_series.type)
                info = get_chart_type_info(ct_val)
                if info is None:
                    continue
                _, attrs, axis_config, _ = info

                ct_elem = ET.Element(f'{C_NS}{xml_tag}')
                for attr_name, attr_val in attrs.items():
                    if attr_name in ('bubble3D', 'shape'):
                        continue
                    child = ET.SubElement(ct_elem, f'{C_NS}{attr_name}')
                    child.set('val', attr_val)
                _add_default_sg_props(ct_elem, xml_tag, attrs)

                # Add axId refs — secondary if on_second_axis
                _add_axis_refs(ct_elem, axis_config, on_second)

                # Insert into plot area before axes
                if pa_insert_before is not None:
                    plot_area.insert(list(plot_area).index(pa_insert_before), ct_elem)
                else:
                    plot_area.append(ct_elem)

                # Ensure axis elements exist for this chart-type element.
                # Primary axes may be missing if an earlier sync wiped them via
                # _remove_orphaned_axes (e.g. when chart_part.save() ran before
                # the user populated series). The axis set depends on the chart
                # type's axis_config — pie/doughnut (AXES_NONE) have none,
                # scatter/bubble use val+val, 3D standard bar/surface add serAx.
                if on_second:
                    _ensure_secondary_axes_in_plot_area(plot_area, axis_config)
                else:
                    _ensure_primary_axes_in_plot_area(plot_area, axis_config)

            # Insert ser elements before axId in this ct_elem
            ax_ids = ct_elem.findall(_AX_ID)
            insert_before = ax_ids[0] if ax_ids else None

            for si, series in group_series:
                ct_val = series.type.value if hasattr(series.type, 'value') else str(series.type)
                s_info = get_chart_type_info(ct_val)
                s_dp_family = s_info[3] if s_info else 'bar'
                ser = self._build_ser_element(si, series, categories,
                                              si == last_si,
                                              dp_family=s_dp_family)
                if insert_before is not None:
                    ct_elem.insert(list(ct_elem).index(insert_before), ser)
                else:
                    ct_elem.append(ser)

            _ensure_stacked_defaults(ct_elem)

            # If any series in the group carries data labels, also emit an
            # all-zero chart-type-level <c:dLbls> so PowerPoint does not fall
            # back to chart-type-default visibility.
            if any(getattr(s, '_dlbls_elem', None) is not None
                   for _, s in group_series):
                _ensure_chart_type_dlbls(ct_elem)

            # Chart-type-level <c:shape> for cylinder/cone/pyramid bar3D variants.
            # Must sit after ser/gapWidth/gapDepth/dLbls but before <c:axId>.
            # Strip any existing occurrence (create_new emits one at the wrong
            # position so the detector can see it) and re-insert here.
            first_ct_val = (group_series[0][1].type.value
                            if hasattr(group_series[0][1].type, 'value')
                            else '')
            ct_shape = get_bar3d_shape(first_ct_val)
            for old in ct_elem.findall(f'{C_NS}shape'):
                ct_elem.remove(old)
            if ct_shape is not None:
                shape_el = ET.Element(f'{C_NS}shape')
                shape_el.set('val', ct_shape)
                ax_ids = ct_elem.findall(_AX_ID)
                if ax_ids:
                    ct_elem.insert(list(ct_elem).index(ax_ids[0]), shape_el)
                else:
                    ct_elem.append(shape_el)

        # Remove chart-type elements that no longer have series
        for key, ct_elem in existing_ct.items():
            if key not in used_keys:
                plot_area.remove(ct_elem)

        # Remove orphaned axes — axes not referenced by any chart-type element
        _remove_orphaned_axes(plot_area)

    @staticmethod
    def _build_ser_element(si: int, series, categories: list,
                           is_last: bool,
                           dp_family: str = 'bar') -> ET._Element:
        """Build a <c:ser> XML element for a single series."""
        from ..xlsx.cell_reference import format_cell_ref

        ser = ET.Element(_SER)

        idx_elem = ET.SubElement(ser, _IDX)
        idx_elem.set('val', str(si))
        order_elem = ET.SubElement(ser, _ORDER)
        order_elem.set('val', str(series.order))

        # Series name <c:tx>
        name_str = series.name.as_literal_string if series.name else f'Series {si+1}'
        name_cell = _name_cell(series.name)
        tx = ET.SubElement(ser, _TX)
        str_ref = ET.SubElement(tx, _STR_REF)
        f_elem = ET.SubElement(str_ref, _F)
        if name_cell is not None:
            f_elem.text = _single_cell_ref(name_cell)
        else:
            col_ref = format_cell_ref(0, si + 1)
            f_elem.text = f'Sheet1!${col_ref[0]}$1'
        str_cache = ET.SubElement(str_ref, _STR_CACHE)
        pt_count = ET.SubElement(str_cache, _PT_COUNT)
        pt_count.set('val', '1')
        pt = ET.SubElement(str_cache, _PT)
        pt.set('idx', '0')
        v = ET.SubElement(pt, _V)
        v.text = name_str

        # <c:explosion> for ExplodedPie / ExplodedPie3D — goes after <c:tx>
        # and before <c:cat> per OOXML schema.
        ct_val_s = series.type.value if hasattr(series.type, 'value') else ''
        if ct_val_s in ('ExplodedPie', 'ExplodedPie3D'):
            expl = ET.SubElement(ser, f'{C_NS}explosion')
            expl.set('val', '25')

        # Series-level <c:marker> (after tx, before dPt/dLbls) — preserved
        # across rebuilds. Emitted only if it has any content.
        marker_elem = getattr(series, '_marker_elem', None)
        if marker_elem is not None and len(marker_elem) > 0:
            ser.append(marker_elem)

        # Per-point <c:dPt> overrides (after marker, before dLbls), ordered by idx.
        dpt_elems = getattr(series, '_dpt_elems', None) or {}
        for idx in sorted(dpt_elems.keys()):
            dpt = dpt_elems[idx]
            # Skip empty dPt (only has idx/invertIfNegative scaffolding).
            meaningful = any(
                (child.tag.split('}')[-1] if '}' in child.tag else child.tag)
                not in ('idx', 'invertIfNegative')
                for child in dpt
            )
            if meaningful:
                ser.append(dpt)

        # Data labels (after dPt, before trendlines) — preserve across rebuilds.
        dlbls_elem = getattr(series, '_dlbls_elem', None)
        if dlbls_elem is not None and len(dlbls_elem) > 0:
            ser.append(dlbls_elem)

        # Trendlines (before cat/val to match OOXML element order)
        if hasattr(series, '_trend_lines'):
            for tl in series._trend_lines:
                ser.append(tl._to_xml())

        # Error bars (after trendlines, before cat/val)
        _append_error_bars(ser, series)

        # Scatter/bubble use <c:xVal>/<c:yVal>; others use <c:cat>/<c:val>
        is_xy = dp_family in ('scatter', 'bubble')
        cat_tag = _X_VAL if is_xy else _CAT
        val_tag = _Y_VAL if is_xy else _VAL

        data_points = list(series.data_points)

        # For scatter/bubble, prefer per-point x_value over the shared
        # categories collection. Categories are the legacy/loader fallback.
        xy_x_values = None
        if is_xy and data_points and any(dp.x_value is not None for dp in data_points):
            xy_x_values = [dp.x_value for dp in data_points]

        # Categories / X values
        if xy_x_values is not None:
            x_range = _cells_range(xy_x_values)
            _emit_xy_x_values(ser, cat_tag, xy_x_values, len(data_points),
                              range_override=x_range)
        elif categories:
            cat = ET.SubElement(ser, cat_tag)
            cat_str_ref = ET.SubElement(cat, _STR_REF)
            cat_f = ET.SubElement(cat_str_ref, _F)
            cat_f.text = f'Sheet1!$A$2:$A${len(categories) + 1}'
            cat_cache = ET.SubElement(cat_str_ref, _STR_CACHE)
            cat_pt_count = ET.SubElement(cat_cache, _PT_COUNT)
            cat_pt_count.set('val', str(len(categories)))
            for ci, category in enumerate(categories):
                cat_pt = ET.SubElement(cat_cache, _PT)
                cat_pt.set('idx', str(ci))
                cat_v = ET.SubElement(cat_pt, _V)
                cat_v.text = str(category.value) if category.value is not None else ''

        # Values / Y values
        if data_points:
            # Prefer range derived from cell-backed values so the
            # chart-cached data and the embedded workbook stay in sync.
            y_values = [
                (dp.y_value if is_xy else None) or dp.value for dp in data_points
            ]
            y_range = _cells_range(y_values)
            val = ET.SubElement(ser, val_tag)
            num_ref = ET.SubElement(val, _NUM_REF)
            val_f = ET.SubElement(num_ref, _F)
            if y_range is not None:
                val_f.text = y_range
            else:
                col_ref = format_cell_ref(0, si + 1)
                val_f.text = f'Sheet1!${col_ref[0]}$2:${col_ref[0]}${len(data_points) + 1}'
            num_cache = ET.SubElement(num_ref, _NUM_CACHE)
            fmt = ET.SubElement(num_cache, _FORMAT_CODE)
            fmt.text = 'General'
            val_pt_count = ET.SubElement(num_cache, _PT_COUNT)
            val_pt_count.set('val', str(len(data_points)))
            for di, dp in enumerate(data_points):
                val_pt = ET.SubElement(num_cache, _PT)
                val_pt.set('idx', str(di))
                val_v = ET.SubElement(val_pt, _V)
                # For scatter/bubble, y_value holds the Y coordinate.
                # For other chart types, value holds it. Fall back either way.
                dv = (dp.y_value if is_xy else None) or dp.value
                if dv is not None:
                    val_v.text = _format_num(dv.to_double())
                else:
                    val_v.text = '0'

            # Bubble size (bubble charts only)
            if dp_family == 'bubble':
                size_values = [dp.bubble_size for dp in data_points]
                size_range = _cells_range(size_values)
                bub = ET.SubElement(ser, _BUBBLE_SIZE)
                bub_num_ref = ET.SubElement(bub, _NUM_REF)
                bub_f = ET.SubElement(bub_num_ref, _F)
                if size_range is not None:
                    bub_f.text = size_range
                else:
                    # bubble size in next column after values
                    bub_col_ref = format_cell_ref(0, si + 2)
                    bub_f.text = f'Sheet1!${bub_col_ref[0]}$2:${bub_col_ref[0]}${len(data_points) + 1}'
                bub_cache = ET.SubElement(bub_num_ref, _NUM_CACHE)
                bub_fmt = ET.SubElement(bub_cache, _FORMAT_CODE)
                bub_fmt.text = 'General'
                bub_pt_count = ET.SubElement(bub_cache, _PT_COUNT)
                bub_pt_count.set('val', str(len(data_points)))
                for di, dp in enumerate(data_points):
                    bub_pt = ET.SubElement(bub_cache, _PT)
                    bub_pt.set('idx', str(di))
                    bub_v = ET.SubElement(bub_pt, _V)
                    bs = dp.bubble_size
                    if bs is not None:
                        bub_v.text = _format_num(bs.to_double())
                    else:
                        bub_v.text = '1'

                # Always emit <c:bubble3D> after bubbleSize — PowerPoint does
                # the same for plain bubble series (val="0") and 3D ones (val="1").
                ct_val = series.type.value if hasattr(series.type, 'value') else ''
                b3d = ET.SubElement(ser, f'{C_NS}bubble3D')
                b3d.set('val', '1' if ct_val == 'BubbleWith3D' else '0')

        # Smooth line for scatter charts — emit explicit val so PowerPoint
        # doesn't default to smooth-on for straight-line subtypes.
        if dp_family == 'scatter':
            ct_val = series.type.value if hasattr(series.type, 'value') else ''
            smooth = ET.SubElement(ser, f'{C_NS}smooth')
            smooth.set('val', '1' if 'Smooth' in ct_val else '0')

        # <c:shape> for bar3DChart-based cylinder/cone/pyramid series.
        # Without this, PowerPoint renders the series as rectangular 3D bars.
        ct_val = series.type.value if hasattr(series.type, 'value') else ''
        shape_val = get_bar3d_shape(ct_val)
        if shape_val is not None:
            shape_elem = ET.SubElement(ser, f'{C_NS}shape')
            shape_elem.set('val', shape_val)

        # Series-level c15:datalabelsRange extension (value_from_cell cells).
        _append_datalabels_range_ext(ser, series, len(data_points))

        return ser

    # --- Save ---

    def save(self) -> None:
        """Save chart XML, relationships, and embedded XLSX to the package."""
        # Sync data model to chart XML before saving
        if self._chart_data_model is not None:
            self.sync_from_model(self._chart_data_model)

        ET.indent(self._root, space='  ')
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True,
        )
        self._package.set_part(self._part_name, xml_bytes)
        self._rels_manager.save()

        # Save embedded XLSX if loaded
        if self._xlsx is not None:
            xlsx_part_name = self.get_xlsx_part_name()
            if xlsx_part_name:
                self._package.set_part(xlsx_part_name, self._xlsx.to_bytes())

    # --- Static creation ---

    @staticmethod
    def create_new(
        package: OpcPackage,
        chart_part_name: str,
        chart_type_value: str,
        xlsx_part_name: str,
    ) -> 'ChartPart':
        """
        Create a new chart part with minimal XML skeleton.

        Args:
            package: The PPTX OPC package.
            chart_part_name: e.g., 'ppt/charts/chart1.xml'
            chart_type_value: ChartType enum value string (e.g., 'ClusteredColumn')
            xlsx_part_name: e.g., 'ppt/charts/chart1.xlsx'
        """
        info = get_chart_type_info(chart_type_value)
        if info is None:
            raise ValueError(f"Unsupported chart type: {chart_type_value}")

        xml_tag, attrs, axis_config, dp_family = info

        # Build chartSpace
        root = ET.Element(_CHART_SPACE, nsmap=CHART_NSMAP)

        date1904 = ET.SubElement(root, _DATE1904)
        date1904.set('val', '0')
        lang = ET.SubElement(root, _LANG)
        lang.set('val', 'en-US')
        rounded = ET.SubElement(root, _ROUND_MODE)
        rounded.set('val', '0')

        # mc:AlternateContent with style (matching PowerPoint output)
        MC_NS = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
        C14_NS = 'http://schemas.microsoft.com/office/drawing/2007/8/2/chart'
        mc_ac = ET.SubElement(root, f'{{{MC_NS}}}AlternateContent',
                              nsmap={'mc': MC_NS})
        mc_choice = ET.SubElement(mc_ac, f'{{{MC_NS}}}Choice',
                                  nsmap={'c14': C14_NS})
        mc_choice.set('Requires', 'c14')
        c14_style = ET.SubElement(mc_choice, f'{{{C14_NS}}}style')
        c14_style.set('val', '102')
        mc_fb = ET.SubElement(mc_ac, f'{{{MC_NS}}}Fallback')
        fb_style = ET.SubElement(mc_fb, f'{C_NS}style')
        fb_style.set('val', '2')

        # c:chart
        chart = ET.SubElement(root, _CHART)
        atd = ET.SubElement(chart, f'{C_NS}autoTitleDeleted')
        atd.set('val', '1')
        plot_area = ET.SubElement(chart, _PLOT_AREA)
        ET.SubElement(plot_area, _LAYOUT)

        # Chart type element
        ct_elem = ET.SubElement(plot_area, f'{C_NS}{xml_tag}')
        for attr_name, attr_val in attrs.items():
            # bubble3D is series-level (emitted per <c:ser> during sync),
            # not chart-type-level — including it here corrupts the file.
            # shape is emitted separately below at the OOXML-correct position.
            if attr_name in ('bubble3D', 'shape'):
                continue
            child = ET.SubElement(ct_elem, f'{C_NS}{attr_name}')
            child.set('val', attr_val)

        # Default series-group properties (matching PowerPoint output)
        _add_default_sg_props(ct_elem, xml_tag, attrs)

        # <c:shape> for bar3DChart cylinder/cone/pyramid variants — written at
        # create time so detect_chart_type_from_xml can disambiguate these from
        # plain Column3D/Bar3D on any subsequent ChartPart reinstantiation.
        shape_val = get_bar3d_shape(chart_type_value)
        if shape_val is not None:
            shape_el = ET.SubElement(ct_elem, f'{C_NS}shape')
            shape_el.set('val', shape_val)

        # Axes
        if axis_config == AXES_CAT_VAL:
            ax_id1 = ET.SubElement(ct_elem, _AX_ID)
            ax_id1.set('val', _CAT_AX_ID)
            ax_id2 = ET.SubElement(ct_elem, _AX_ID)
            ax_id2.set('val', _VAL_AX_ID)

            _build_cat_ax(plot_area, _CAT_AX_ID, _VAL_AX_ID)
            _build_val_ax(plot_area, _VAL_AX_ID, _CAT_AX_ID, 'l')

        elif axis_config == AXES_CAT_VAL_SER:
            # surface3DChart and bar3DChart-standard require a third axis
            # (serAx — depth). Commercial expects 3 axIds in the chart-type
            # element and 3 axis elements in plotArea.
            for aid in (_CAT_AX_ID, _VAL_AX_ID, _SER_AX_ID):
                e = ET.SubElement(ct_elem, _AX_ID)
                e.set('val', aid)
            _build_cat_ax(plot_area, _CAT_AX_ID, _VAL_AX_ID)
            _build_val_ax(plot_area, _VAL_AX_ID, _CAT_AX_ID, 'l')
            _build_ser_ax(plot_area, _SER_AX_ID, _VAL_AX_ID)

        elif axis_config == AXES_VAL_VAL:
            ax_id1 = ET.SubElement(ct_elem, _AX_ID)
            ax_id1.set('val', _VAL_AX_ID)
            ax_id2 = ET.SubElement(ct_elem, _AX_ID)
            ax_id2.set('val', _VAL_AX_ID_2)

            _build_val_ax(plot_area, _VAL_AX_ID, _VAL_AX_ID_2, 'b')
            _build_val_ax(plot_area, _VAL_AX_ID_2, _VAL_AX_ID, 'l')

        # Legend
        legend = ET.SubElement(chart, _LEGEND)
        legend_pos = ET.SubElement(legend, _LEGEND_POS)
        legend_pos.set('val', 'b')
        overlay = ET.SubElement(legend, _OVERLAY)
        overlay.set('val', '0')

        # Default chart-level properties (matching PowerPoint output)
        pv = ET.SubElement(chart, f'{C_NS}plotVisOnly')
        pv.set('val', '1')
        ET.SubElement(chart, f'{C_NS}dispBlanksAs')  # no val = default "zero"
        sdl = ET.SubElement(chart, f'{C_NS}showDLblsOverMax')
        sdl.set('val', '1')

        # Default text properties at chartSpace level
        txPr = ET.SubElement(root, f'{C_NS}txPr')
        ET.SubElement(txPr, f'{A_NS}bodyPr')
        txPr_p = ET.SubElement(txPr, f'{A_NS}p')
        txPr_pPr = ET.SubElement(txPr_p, f'{A_NS}pPr')
        ET.SubElement(txPr_pPr, f'{A_NS}defRPr', attrib={'sz': '1800'})
        ET.SubElement(txPr_p, f'{A_NS}endParaRPr', attrib={'lang': 'en-US'})

        # externalData reference
        ext_data = ET.SubElement(root, _EXTERNAL_DATA)
        # rel_id will be set after we create the relationship
        auto_update = ET.SubElement(ext_data, _AUTO_UPDATE)
        auto_update.set('val', '0')

        # Serialize to package
        ET.indent(root, space='  ')
        xml_bytes = ET.tostring(
            root, pretty_print=True, xml_declaration=True,
            encoding='UTF-8', standalone=True,
        )
        package.set_part(chart_part_name, xml_bytes)

        # Register content type
        ct_mgr = ContentTypesManager(package)
        ct_mgr.add_override(chart_part_name, CONTENT_TYPES['chart'])
        ct_mgr.save()

        # Create relationships
        rels = RelationshipsManager(package, chart_part_name)

        # Relative path from ppt/charts/ to the xlsx (e.g. ../embeddings/...)
        chart_dir = chart_part_name.rsplit('/', 1)[0]  # ppt/charts
        xlsx_dir = xlsx_part_name.rsplit('/', 1)[0]     # ppt/embeddings
        xlsx_file = xlsx_part_name.rsplit('/', 1)[-1]
        if chart_dir == xlsx_dir:
            rel_target = xlsx_file
        else:
            rel_target = '../' + xlsx_dir.split('/')[-1] + '/' + xlsx_file
        rel_id = rels.add_relationship(REL_TYPES['package'], rel_target)
        rels.save()

        # Set the externalData r:id
        ext_data.set(f'{R_NS}id', rel_id)

        # Re-save with the r:id set
        xml_bytes = ET.tostring(
            root, pretty_print=True, xml_declaration=True,
            encoding='UTF-8', standalone=True,
        )
        package.set_part(chart_part_name, xml_bytes)

        # Create embedded XLSX
        from ..xlsx.xlsx_package import XlsxPackage
        xlsx = XlsxPackage.create_new()
        package.set_part(xlsx_part_name, xlsx.to_bytes())

        # Ensure xlsx extension has a default content type
        _ensure_xlsx_default_content_type(package)

        part = ChartPart(package, chart_part_name)
        part._xlsx = xlsx
        # Remember the requested chart type so detect_chart_type() can
        # distinguish BubbleWith3D from Bubble before any series are added
        # (both share the <c:bubbleChart> tag and distinguishing attr lives
        # in <c:ser>).
        part._requested_chart_type = chart_type_value
        return part


def _build_cat_ax(plot_area: ET._Element, ax_id: str, cross_ax_id: str) -> None:
    """Build a minimal <c:catAx> element."""
    cat_ax = ET.SubElement(plot_area, _CAT_AX)
    _build_ax_common(cat_ax, ax_id, cross_ax_id, 'b')


def _build_val_ax(plot_area: ET._Element, ax_id: str, cross_ax_id: str, pos: str) -> None:
    """Build a minimal <c:valAx> element."""
    val_ax = ET.SubElement(plot_area, _VAL_AX)
    _build_ax_common(val_ax, ax_id, cross_ax_id, pos)


def _build_ser_ax(plot_area: ET._Element, ax_id: str, cross_ax_id: str) -> None:
    """Build a minimal <c:serAx> (series/depth axis) used by surface3DChart
    and by bar3DChart with grouping=standard to supply the third axis."""
    ser_ax = ET.SubElement(plot_area, _SER_AX)
    id_elem = ET.SubElement(ser_ax, _AX_ID)
    id_elem.set('val', ax_id)
    scaling = ET.SubElement(ser_ax, _SCALING)
    orient = ET.SubElement(scaling, _ORIENTATION)
    orient.set('val', 'minMax')
    delete = ET.SubElement(ser_ax, _DELETE)
    delete.set('val', '0')
    ax_pos = ET.SubElement(ser_ax, _AX_POS)
    ax_pos.set('val', 'b')
    major_tick = ET.SubElement(ser_ax, _MAJOR_TICK)
    major_tick.set('val', 'out')
    minor_tick = ET.SubElement(ser_ax, _MINOR_TICK)
    minor_tick.set('val', 'none')
    cross = ET.SubElement(ser_ax, _CROSS_AX)
    cross.set('val', cross_ax_id)


def _build_ax_common(ax_elem: ET._Element, ax_id: str, cross_ax_id: str, pos: str) -> None:
    """Common axis structure."""
    id_elem = ET.SubElement(ax_elem, _AX_ID)
    id_elem.set('val', ax_id)
    scaling = ET.SubElement(ax_elem, _SCALING)
    orient = ET.SubElement(scaling, _ORIENTATION)
    orient.set('val', 'minMax')
    delete = ET.SubElement(ax_elem, _DELETE)
    delete.set('val', '0')
    ax_pos = ET.SubElement(ax_elem, _AX_POS)
    ax_pos.set('val', pos)
    cross = ET.SubElement(ax_elem, _CROSS_AX)
    cross.set('val', cross_ax_id)


def _format_num(value: float) -> str:
    """Format a number for chart XML: integers without .0, floats as-is."""
    if value == int(value):
        return str(int(value))
    return str(value)


def _value_cell(value):
    """Return a ChartDataCell if `value` is cell-backed, else None.

    Handles DoubleChartValue / StringOrDoubleChartValue (both have `_cell`).
    """
    if value is None:
        return None
    cell = getattr(value, '_cell', None)
    return cell if cell is not None and hasattr(cell, 'row') else None


def _name_cell(name_value):
    """Return a single ChartDataCell backing a series name, or None.

    StringChartValue stores cells in a list; use the first one.
    """
    if name_value is None:
        return None
    cells = getattr(name_value, '_cells', None)
    if cells:
        return cells[0]
    return None


def _single_cell_ref(cell) -> str:
    """Build a `Sheet1!$A$1`-style reference from one cell."""
    col = _col_letters(cell.column)
    row = cell.row + 1
    ws_name = 'Sheet1'
    try:
        ws = cell.chart_data_worksheet
        if ws is not None and getattr(ws, 'name', None):
            ws_name = ws.name
    except Exception:
        pass
    return f'{ws_name}!${col}${row}'


def _cells_range(values: list):
    """Given a list of chart values, return a contiguous-column range string
    like `Sheet1!$B$2:$B$7`, or None if the values aren't all cell-backed in
    the same column.
    """
    cells = [_value_cell(v) for v in values]
    if not cells or any(c is None for c in cells):
        return None
    cols = {c.column for c in cells}
    if len(cols) != 1:
        return None
    col = _col_letters(cells[0].column)
    rows = [c.row + 1 for c in cells]
    ws_name = 'Sheet1'
    try:
        ws = cells[0].chart_data_worksheet
        if ws is not None and getattr(ws, 'name', None):
            ws_name = ws.name
    except Exception:
        pass
    return f'{ws_name}!${col}${min(rows)}:${col}${max(rows)}'


def _emit_xy_x_values(ser_elem: ET._Element, tag: str, x_values: list,
                      pt_count: int, range_override: str = None) -> None:
    """Emit <c:xVal> for scatter/bubble from per-point x_value objects.

    If every value is numeric (DOUBLE_LITERALS or worksheet numeric) the
    element uses <c:numRef>/<c:numCache>; otherwise <c:strRef>/<c:strCache>.
    """
    from ...charts.DataSourceType import DataSourceType

    def _is_numeric(xv) -> bool:
        ds = getattr(xv, '_data_source_type', None)
        if ds == DataSourceType.STRING_LITERALS:
            return False
        if ds == DataSourceType.DOUBLE_LITERALS:
            return True
        # WORKSHEET or unknown — try to coerce
        try:
            float(xv.as_literal_string) if hasattr(xv, 'as_literal_string') else None
            float(xv.to_double() if hasattr(xv, 'to_double') else 0.0)
            return True
        except (ValueError, TypeError):
            return False

    all_numeric = all(_is_numeric(xv) for xv in x_values)
    x_range = range_override or f'Sheet1!$A$2:$A${pt_count + 1}'

    x_elem = ET.SubElement(ser_elem, tag)
    if all_numeric:
        num_ref = ET.SubElement(x_elem, _NUM_REF)
        f_elem = ET.SubElement(num_ref, _F)
        f_elem.text = x_range
        num_cache = ET.SubElement(num_ref, _NUM_CACHE)
        fmt = ET.SubElement(num_cache, _FORMAT_CODE)
        fmt.text = 'General'
        pt_count_elem = ET.SubElement(num_cache, _PT_COUNT)
        pt_count_elem.set('val', str(pt_count))
        for i, xv in enumerate(x_values):
            pt = ET.SubElement(num_cache, _PT)
            pt.set('idx', str(i))
            v = ET.SubElement(pt, _V)
            v.text = _format_num(xv.to_double())
    else:
        str_ref = ET.SubElement(x_elem, _STR_REF)
        f_elem = ET.SubElement(str_ref, _F)
        f_elem.text = x_range
        str_cache = ET.SubElement(str_ref, _STR_CACHE)
        pt_count_elem = ET.SubElement(str_cache, _PT_COUNT)
        pt_count_elem.set('val', str(pt_count))
        for i, xv in enumerate(x_values):
            pt = ET.SubElement(str_cache, _PT)
            pt.set('idx', str(i))
            v = ET.SubElement(pt, _V)
            v.text = xv.as_literal_string


def _ensure_chart_type_dlbls(ct_elem: ET._Element) -> None:
    """Insert a chart-type-level <c:dLbls> with all show_* flags set to '0'.

    Commercial Aspose emits this sibling to <c:ser> so PowerPoint does not
    apply chart-type default visibility when a series configures labels.
    Inserts after the last <c:ser>, before <c:gapWidth>/<c:overlap>/<c:axId>.
    Preserves any existing chart-type-level <c:dLbls> unchanged.
    """
    existing = ct_elem.find(f'{C_NS}dLbls')
    if existing is not None:
        return
    new_dlbls = ET.Element(f'{C_NS}dLbls')
    for tag in ('showLegendKey', 'showVal', 'showCatName', 'showSerName',
                'showPercent', 'showBubbleSize', 'showLeaderLines'):
        e = ET.SubElement(new_dlbls, f'{C_NS}{tag}')
        e.set('val', '0')

    ser_elems = ct_elem.findall(_SER)
    if ser_elems:
        insert_pos = list(ct_elem).index(ser_elems[-1]) + 1
    else:
        ax_ids = ct_elem.findall(_AX_ID)
        insert_pos = list(ct_elem).index(ax_ids[0]) if ax_ids else len(list(ct_elem))
    ct_elem.insert(insert_pos, new_dlbls)


def _ensure_stacked_defaults(ct_elem: ET._Element) -> None:
    """For stacked bar/column charts, ensure overlap=100 and serLines exist.

    Called after sync_from_model writes <c:ser> elements. Elements are
    placed after ser and before axId to match commercial element order.
    """
    local_tag = ct_elem.tag.split('}')[-1] if '}' in ct_elem.tag else ct_elem.tag
    if local_tag not in ('barChart', 'bar3DChart'):
        return

    # Check grouping
    grouping_elem = ct_elem.find(f'{C_NS}grouping')
    if grouping_elem is None:
        return
    grouping = grouping_elem.get('val', '')
    if grouping not in ('stacked', 'percentStacked'):
        return

    # Find insertion point (before first axId)
    ax_ids = ct_elem.findall(_AX_ID)
    insert_idx = list(ct_elem).index(ax_ids[0]) if ax_ids else len(list(ct_elem))

    # overlap — add default 100 if absent
    overlap = ct_elem.find(f'{C_NS}overlap')
    if overlap is None:
        overlap = ET.Element(f'{C_NS}overlap')
        overlap.set('val', '100')
        ct_elem.insert(insert_idx, overlap)
        insert_idx += 1

    # serLines: PowerPoint adds it by default for stacked bar (barDir=bar)
    # but NOT for stacked column (barDir=col)
    bar_dir_elem = ct_elem.find(f'{C_NS}barDir')
    if bar_dir_elem is not None and bar_dir_elem.get('val') == 'bar':
        ser_lines = ct_elem.find(f'{C_NS}serLines')
        if ser_lines is None:
            ser_lines = ET.Element(f'{C_NS}serLines')
            ct_elem.insert(insert_idx, ser_lines)


def _add_default_sg_props(ct_elem: ET._Element, xml_tag: str, attrs: dict) -> None:
    """Add default series-group properties to match commercial Aspose output.

    Only adds varyColors here (must precede <c:ser> elements).
    Other defaults (overlap, serLines for stacked) are handled in
    sync_from_model since they must follow <c:ser> elements.
    """
    # varyColors: 0 for bar/line/area/radar/stock/scatter, 1 for pie/doughnut
    pie_like = {'pieChart', 'pie3DChart', 'doughnutChart', 'ofPieChart'}
    vary_val = '1' if xml_tag in pie_like else '0'
    vc = ET.SubElement(ct_elem, f'{C_NS}varyColors')
    vc.set('val', vary_val)


def _add_axis_refs(ct_elem: ET._Element, axis_config: str, on_second: bool) -> None:
    """Add <c:axId> references to a chart-type element."""
    if axis_config == AXES_CAT_VAL:
        if on_second:
            ids = [_CAT_AX_ID_2, _VAL_AX_ID_2]
        else:
            ids = [_CAT_AX_ID, _VAL_AX_ID]
    elif axis_config == AXES_CAT_VAL_SER:
        # serAx has no secondary-axis variant in practice.
        ids = [_CAT_AX_ID, _VAL_AX_ID, _SER_AX_ID]
    elif axis_config == AXES_VAL_VAL:
        if on_second:
            ids = [_VAL_AX_ID_2, _CAT_AX_ID_2]
        else:
            ids = [_VAL_AX_ID, _VAL_AX_ID_2]
    else:
        return
    for ax_id in ids:
        el = ET.SubElement(ct_elem, _AX_ID)
        el.set('val', ax_id)


def _ensure_secondary_axes_in_plot_area(plot_area: ET._Element, axis_config: str) -> None:
    """Create secondary axis elements in the plot area if not already present."""
    # Collect existing axis IDs
    existing_ids = set()
    for child in plot_area:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local in ('catAx', 'valAx', 'dateAx', 'serAx'):
            ax_id_elem = child.find(_AX_ID)
            if ax_id_elem is not None:
                existing_ids.add(ax_id_elem.get('val'))

    if axis_config == AXES_CAT_VAL:
        if _CAT_AX_ID_2 not in existing_ids:
            _build_cat_ax(plot_area, _CAT_AX_ID_2, _VAL_AX_ID_2)
            # Hide the secondary category axis and set position to top
            _configure_axis_elem(plot_area, _CAT_AX_ID_2, pos='t')
        if _VAL_AX_ID_2 not in existing_ids:
            _build_val_ax(plot_area, _VAL_AX_ID_2, _CAT_AX_ID_2, 'r')
    elif axis_config == AXES_VAL_VAL:
        if _CAT_AX_ID_2 not in existing_ids:
            _build_val_ax(plot_area, _CAT_AX_ID_2, _VAL_AX_ID_2, 't')
            _configure_axis_elem(plot_area, _CAT_AX_ID_2, pos='t')
        if _VAL_AX_ID_2 not in existing_ids:
            _build_val_ax(plot_area, _VAL_AX_ID_2, _CAT_AX_ID_2, 'r')


def _ensure_primary_axes_in_plot_area(plot_area: ET._Element, axis_config: str) -> None:
    """Create primary axis elements in the plot area if not already present.

    Mirrors the axis construction in ChartPart.create_new so that axes wiped
    by a previous orphan-cleanup pass are re-created with the correct layout
    for the given axis_config. AXES_NONE (pie/doughnut) is a no-op.
    """
    existing_ids = set()
    for child in plot_area:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local in ('catAx', 'valAx', 'dateAx', 'serAx'):
            ax_id_elem = child.find(_AX_ID)
            if ax_id_elem is not None:
                existing_ids.add(ax_id_elem.get('val'))

    if axis_config == AXES_CAT_VAL:
        if _CAT_AX_ID not in existing_ids:
            _build_cat_ax(plot_area, _CAT_AX_ID, _VAL_AX_ID)
        if _VAL_AX_ID not in existing_ids:
            _build_val_ax(plot_area, _VAL_AX_ID, _CAT_AX_ID, 'l')
    elif axis_config == AXES_CAT_VAL_SER:
        if _CAT_AX_ID not in existing_ids:
            _build_cat_ax(plot_area, _CAT_AX_ID, _VAL_AX_ID)
        if _VAL_AX_ID not in existing_ids:
            _build_val_ax(plot_area, _VAL_AX_ID, _CAT_AX_ID, 'l')
        if _SER_AX_ID not in existing_ids:
            _build_ser_ax(plot_area, _SER_AX_ID, _VAL_AX_ID)
    elif axis_config == AXES_VAL_VAL:
        if _VAL_AX_ID not in existing_ids:
            _build_val_ax(plot_area, _VAL_AX_ID, _VAL_AX_ID_2, 'b')
        if _VAL_AX_ID_2 not in existing_ids:
            _build_val_ax(plot_area, _VAL_AX_ID_2, _VAL_AX_ID, 'l')


def _configure_axis_elem(plot_area: ET._Element, axis_id: str,
                          pos: str = None, hidden: bool = False) -> None:
    """Update position and delete flag on an axis element by ID."""
    for child in plot_area:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local in ('catAx', 'valAx', 'dateAx'):
            ax_id_elem = child.find(_AX_ID)
            if ax_id_elem is not None and ax_id_elem.get('val') == axis_id:
                if pos:
                    ax_pos = child.find(_AX_POS)
                    if ax_pos is not None:
                        ax_pos.set('val', pos)
                if hidden:
                    delete = child.find(_DELETE)
                    if delete is not None:
                        delete.set('val', '1')
                break


def _remove_orphaned_axes(plot_area: ET._Element) -> None:
    """Remove axis elements not referenced by any chart-type element's <c:axId>."""
    # Collect all axis IDs referenced by chart-type elements
    referenced_ids = set()
    axis_tags = frozenset({'catAx', 'valAx', 'dateAx', 'serAx'})
    skip_tags = axis_tags | frozenset({'layout', 'spPr', 'dTable'})
    for child in plot_area:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local not in skip_tags:
            for ax_id_elem in child.findall(_AX_ID):
                val = ax_id_elem.get('val')
                if val:
                    referenced_ids.add(val)

    # Remove axes whose ID is not referenced
    to_remove = []
    for child in plot_area:
        local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if local in axis_tags:
            ax_id_elem = child.find(_AX_ID)
            if ax_id_elem is not None:
                if ax_id_elem.get('val') not in referenced_ids:
                    to_remove.append(child)
    for elem in to_remove:
        plot_area.remove(elem)


_C15_NS = 'http://schemas.microsoft.com/office/drawing/2012/chart'
_DATALABELS_RANGE_EXT_URI = '{02D57815-91ED-43cb-92C2-25804820EDAC}'


def _append_datalabels_range_ext(ser_elem: ET._Element, series,
                                 data_point_count: int) -> None:
    """Emit series-level <c15:datalabelsRange> if any per-point label has
    value_from_cell set. This is where PowerPoint expects to find the mapping
    from data points to workbook cells for 'label text from cell' mode.
    """
    cells = getattr(series, '_value_from_cell_cells', None)
    if not cells:
        return

    # Build the range formula. For contiguous same-column cells use
    # 'Sheet1!$Col$r1:$Col$r2'; otherwise join with commas.
    ordered_idxs = sorted(cells.keys())
    ordered = [cells[i] for i in ordered_idxs]
    formula = _build_cells_formula(ordered)

    ext_lst = ET.SubElement(ser_elem, f'{C_NS}extLst')
    ext = ET.SubElement(
        ext_lst, f'{C_NS}ext',
        attrib={'uri': _DATALABELS_RANGE_EXT_URI},
        nsmap={'c15': _C15_NS},
    )
    dlr = ET.SubElement(ext, f'{{{_C15_NS}}}datalabelsRange')
    f_elem = ET.SubElement(dlr, f'{{{_C15_NS}}}f')
    f_elem.text = formula
    cache = ET.SubElement(dlr, f'{{{_C15_NS}}}dlblRangeCache')
    pc = ET.SubElement(cache, f'{C_NS}ptCount')
    pc.set('val', str(data_point_count))
    for idx in ordered_idxs:
        cell = cells[idx]
        pt = ET.SubElement(cache, f'{C_NS}pt')
        pt.set('idx', str(idx))
        v = ET.SubElement(pt, f'{C_NS}v')
        cv = cell.value
        v.text = '' if cv is None else str(cv)


def _build_cells_formula(cells: list) -> str:
    """Build an Excel-style formula for a list of ChartDataCell."""
    if not cells:
        return ''
    # Check contiguous same-column
    first = cells[0]
    same_col = all(c.column == first.column for c in cells)
    sequential = same_col and all(
        cells[i].row == cells[i - 1].row + 1 for i in range(1, len(cells)))
    if sequential and len(cells) > 1:
        col = _col_letters(first.column)
        return f"Sheet1!${col}${first.row + 1}:${col}${cells[-1].row + 1}"
    if len(cells) == 1:
        col = _col_letters(first.column)
        return f"Sheet1!${col}${first.row + 1}"
    # Fallback: comma-separated single-cell refs
    parts = [f"Sheet1!${_col_letters(c.column)}${c.row + 1}" for c in cells]
    return ','.join(parts)


def _col_letters(col_idx: int) -> str:
    result = ''
    n = col_idx
    while True:
        n, rem = divmod(n, 26)
        result = chr(ord('A') + rem) + result
        if n == 0:
            break
        n -= 1
    return result


def _append_error_bars(ser_elem: ET._Element, series) -> None:
    """Append <c:errBars> elements to a <c:ser> for visible error bars.

    Before writing custom error bars, syncs per-data-point custom values
    from the ChartDataPoint.error_bars_custom_values back into the
    ErrorBarsFormat._custom_plus/_custom_minus lists.
    """
    for eb in (getattr(series, '_error_bars_x', None),
               getattr(series, '_error_bars_y', None)):
        if eb is None or not eb.is_visible:
            continue
        # Sync custom values from data points into the ErrorBarsFormat lists
        from ...charts.ErrorBarValueType import ErrorBarValueType
        if eb.value_type == ErrorBarValueType.CUSTOM:
            plus_vals = []
            minus_vals = []
            for dp in series.data_points:
                cv = dp.error_bars_custom_values
                if eb.direction == 'x':
                    plus_vals.append(cv.x_plus.as_literal_double)
                    minus_vals.append(cv.x_minus.as_literal_double)
                else:
                    plus_vals.append(cv.y_plus.as_literal_double)
                    minus_vals.append(cv.y_minus.as_literal_double)
            eb._custom_plus = plus_vals
            eb._custom_minus = minus_vals
        ser_elem.append(eb._to_xml())


def _ensure_xlsx_default_content_type(package: OpcPackage) -> None:
    """Ensure the .xlsx extension has a default content type."""
    from ..opc.content_types import CT_NS
    ct_mgr = ContentTypesManager(package)
    # Check if xlsx default already exists
    for default in ct_mgr._root.findall(f"{CT_NS}Default"):
        if default.get('Extension') == 'xlsx':
            return
    # Add it
    default_elem = ET.SubElement(ct_mgr._root, f"{CT_NS}Default")
    default_elem.set('Extension', 'xlsx')
    default_elem.set('ContentType',
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    ct_mgr.save()
