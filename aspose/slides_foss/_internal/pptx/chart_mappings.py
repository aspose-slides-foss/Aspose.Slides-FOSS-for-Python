"""
Chart type mapping tables.

Maps ChartType enum values to XML element tags, attributes, axis configurations,
and data point family types.
"""

from __future__ import annotations

# --- Axis configuration types ---
AXES_CAT_VAL = 'cat_val'         # catAx + valAx (most charts)
AXES_CAT_VAL_SER = 'cat_val_ser' # catAx + valAx + serAx (3D surface, 3D bar standard)
AXES_VAL_VAL = 'val_val'         # valAx + valAx (scatter, bubble)
AXES_NONE = 'none'               # no axes (pie, doughnut)

# --- Data point families ---
DP_BAR = 'bar'
DP_LINE = 'line'
DP_PIE = 'pie'
DP_DOUGHNUT = 'doughnut'
DP_AREA = 'area'
DP_SCATTER = 'scatter'
DP_BUBBLE = 'bubble'
DP_RADAR = 'radar'
DP_STOCK = 'stock'
DP_SURFACE = 'surface'

# --- ChartType enum value -> (xml_tag, attrs_dict, axis_config, dp_family) ---
# xml_tag is the local name under <c:plotArea>, prefixed with c: namespace at runtime.
# attrs_dict contains child elements like <c:barDir val="col"/>.

CHART_TYPE_INFO = {
    # Column charts (barChart with barDir=col)
    'ClusteredColumn':           ('barChart', {'barDir': 'col', 'grouping': 'clustered'}, AXES_CAT_VAL, DP_BAR),
    'StackedColumn':             ('barChart', {'barDir': 'col', 'grouping': 'stacked'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedColumn':     ('barChart', {'barDir': 'col', 'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_BAR),
    'ClusteredColumn3D':         ('bar3DChart', {'barDir': 'col', 'grouping': 'clustered'}, AXES_CAT_VAL, DP_BAR),
    'StackedColumn3D':           ('bar3DChart', {'barDir': 'col', 'grouping': 'stacked'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedColumn3D':   ('bar3DChart', {'barDir': 'col', 'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_BAR),
    'Column3D':                  ('bar3DChart', {'barDir': 'col', 'grouping': 'standard'}, AXES_CAT_VAL_SER, DP_BAR),

    # Cylinder/Cone/Pyramid columns (bar3DChart with shape attribute).
    # The `shape` attr here is not emitted by the template loop (skipped like
    # bubble3D); it's written separately at the correct OOXML position AND
    # lets the detector disambiguate these from plain Column3D/Bar3D on load.
    'ClusteredCylinder':         ('bar3DChart', {'barDir': 'col', 'grouping': 'clustered', 'shape': 'cylinder'}, AXES_CAT_VAL, DP_BAR),
    'StackedCylinder':           ('bar3DChart', {'barDir': 'col', 'grouping': 'stacked', 'shape': 'cylinder'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedCylinder':   ('bar3DChart', {'barDir': 'col', 'grouping': 'percentStacked', 'shape': 'cylinder'}, AXES_CAT_VAL, DP_BAR),
    'Cylinder3D':                ('bar3DChart', {'barDir': 'col', 'grouping': 'standard', 'shape': 'cylinder'}, AXES_CAT_VAL_SER, DP_BAR),
    'ClusteredCone':             ('bar3DChart', {'barDir': 'col', 'grouping': 'clustered', 'shape': 'cone'}, AXES_CAT_VAL, DP_BAR),
    'StackedCone':               ('bar3DChart', {'barDir': 'col', 'grouping': 'stacked', 'shape': 'cone'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedCone':       ('bar3DChart', {'barDir': 'col', 'grouping': 'percentStacked', 'shape': 'cone'}, AXES_CAT_VAL, DP_BAR),
    'Cone3D':                    ('bar3DChart', {'barDir': 'col', 'grouping': 'standard', 'shape': 'cone'}, AXES_CAT_VAL_SER, DP_BAR),
    'ClusteredPyramid':          ('bar3DChart', {'barDir': 'col', 'grouping': 'clustered', 'shape': 'pyramid'}, AXES_CAT_VAL, DP_BAR),
    'StackedPyramid':            ('bar3DChart', {'barDir': 'col', 'grouping': 'stacked', 'shape': 'pyramid'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedPyramid':    ('bar3DChart', {'barDir': 'col', 'grouping': 'percentStacked', 'shape': 'pyramid'}, AXES_CAT_VAL, DP_BAR),
    'Pyramid3D':                 ('bar3DChart', {'barDir': 'col', 'grouping': 'standard', 'shape': 'pyramid'}, AXES_CAT_VAL_SER, DP_BAR),

    # Bar charts (barChart with barDir=bar)
    'ClusteredBar':              ('barChart', {'barDir': 'bar', 'grouping': 'clustered'}, AXES_CAT_VAL, DP_BAR),
    'StackedBar':                ('barChart', {'barDir': 'bar', 'grouping': 'stacked'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedBar':        ('barChart', {'barDir': 'bar', 'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_BAR),
    'ClusteredBar3D':            ('bar3DChart', {'barDir': 'bar', 'grouping': 'clustered'}, AXES_CAT_VAL, DP_BAR),
    'StackedBar3D':              ('bar3DChart', {'barDir': 'bar', 'grouping': 'stacked'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedBar3D':      ('bar3DChart', {'barDir': 'bar', 'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_BAR),

    # Horizontal Cylinder/Cone/Pyramid bars (bar3DChart with shape attribute)
    'ClusteredHorizontalCylinder':        ('bar3DChart', {'barDir': 'bar', 'grouping': 'clustered', 'shape': 'cylinder'}, AXES_CAT_VAL, DP_BAR),
    'StackedHorizontalCylinder':          ('bar3DChart', {'barDir': 'bar', 'grouping': 'stacked', 'shape': 'cylinder'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedHorizontalCylinder':  ('bar3DChart', {'barDir': 'bar', 'grouping': 'percentStacked', 'shape': 'cylinder'}, AXES_CAT_VAL, DP_BAR),
    'ClusteredHorizontalCone':            ('bar3DChart', {'barDir': 'bar', 'grouping': 'clustered', 'shape': 'cone'}, AXES_CAT_VAL, DP_BAR),
    'StackedHorizontalCone':              ('bar3DChart', {'barDir': 'bar', 'grouping': 'stacked', 'shape': 'cone'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedHorizontalCone':      ('bar3DChart', {'barDir': 'bar', 'grouping': 'percentStacked', 'shape': 'cone'}, AXES_CAT_VAL, DP_BAR),
    'ClusteredHorizontalPyramid':         ('bar3DChart', {'barDir': 'bar', 'grouping': 'clustered', 'shape': 'pyramid'}, AXES_CAT_VAL, DP_BAR),
    'StackedHorizontalPyramid':           ('bar3DChart', {'barDir': 'bar', 'grouping': 'stacked', 'shape': 'pyramid'}, AXES_CAT_VAL, DP_BAR),
    'PercentsStackedHorizontalPyramid':   ('bar3DChart', {'barDir': 'bar', 'grouping': 'percentStacked', 'shape': 'pyramid'}, AXES_CAT_VAL, DP_BAR),

    # Line charts
    'Line':                              ('lineChart', {'grouping': 'standard'}, AXES_CAT_VAL, DP_LINE),
    'StackedLine':                       ('lineChart', {'grouping': 'stacked'}, AXES_CAT_VAL, DP_LINE),
    'PercentsStackedLine':               ('lineChart', {'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_LINE),
    'LineWithMarkers':                   ('lineChart', {'grouping': 'standard'}, AXES_CAT_VAL, DP_LINE),
    'StackedLineWithMarkers':            ('lineChart', {'grouping': 'stacked'}, AXES_CAT_VAL, DP_LINE),
    'PercentsStackedLineWithMarkers':    ('lineChart', {'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_LINE),
    'Line3D':                            ('line3DChart', {'grouping': 'standard'}, AXES_CAT_VAL_SER, DP_LINE),

    # Pie charts
    'Pie':            ('pieChart', {}, AXES_NONE, DP_PIE),
    'Pie3D':          ('pie3DChart', {}, AXES_NONE, DP_PIE),
    'PieOfPie':       ('ofPieChart', {'ofPieType': 'pie'}, AXES_NONE, DP_PIE),
    'ExplodedPie':    ('pieChart', {}, AXES_NONE, DP_PIE),
    'ExplodedPie3D':  ('pie3DChart', {}, AXES_NONE, DP_PIE),
    'BarOfPie':       ('ofPieChart', {'ofPieType': 'bar'}, AXES_NONE, DP_PIE),

    # Doughnut
    'Doughnut':         ('doughnutChart', {}, AXES_NONE, DP_DOUGHNUT),
    'ExplodedDoughnut': ('doughnutChart', {}, AXES_NONE, DP_DOUGHNUT),

    # Area charts
    'Area':                  ('areaChart', {'grouping': 'standard'}, AXES_CAT_VAL, DP_AREA),
    'StackedArea':           ('areaChart', {'grouping': 'stacked'}, AXES_CAT_VAL, DP_AREA),
    'PercentsStackedArea':   ('areaChart', {'grouping': 'percentStacked'}, AXES_CAT_VAL, DP_AREA),
    'Area3D':                ('area3DChart', {'grouping': 'standard'}, AXES_CAT_VAL_SER, DP_AREA),
    'StackedArea3D':         ('area3DChart', {'grouping': 'stacked'}, AXES_CAT_VAL_SER, DP_AREA),
    'PercentsStackedArea3D': ('area3DChart', {'grouping': 'percentStacked'}, AXES_CAT_VAL_SER, DP_AREA),

    # Scatter charts
    'ScatterWithMarkers':                    ('scatterChart', {'scatterStyle': 'lineMarker'}, AXES_VAL_VAL, DP_SCATTER),
    'ScatterWithSmoothLinesAndMarkers':      ('scatterChart', {'scatterStyle': 'smoothMarker'}, AXES_VAL_VAL, DP_SCATTER),
    'ScatterWithSmoothLines':                ('scatterChart', {'scatterStyle': 'smooth'}, AXES_VAL_VAL, DP_SCATTER),
    'ScatterWithStraightLinesAndMarkers':    ('scatterChart', {'scatterStyle': 'lineMarker'}, AXES_VAL_VAL, DP_SCATTER),
    'ScatterWithStraightLines':              ('scatterChart', {'scatterStyle': 'line'}, AXES_VAL_VAL, DP_SCATTER),

    # Stock charts
    'HighLowClose':           ('stockChart', {}, AXES_CAT_VAL, DP_STOCK),
    'OpenHighLowClose':       ('stockChart', {}, AXES_CAT_VAL, DP_STOCK),
    'VolumeHighLowClose':     ('stockChart', {}, AXES_CAT_VAL, DP_STOCK),
    'VolumeOpenHighLowClose': ('stockChart', {}, AXES_CAT_VAL, DP_STOCK),

    # Surface charts
    'Surface3D':           ('surface3DChart', {}, AXES_CAT_VAL_SER, DP_SURFACE),
    'WireframeSurface3D':  ('surface3DChart', {'wireframe': '1'}, AXES_CAT_VAL_SER, DP_SURFACE),
    'Contour':             ('surfaceChart', {}, AXES_CAT_VAL, DP_SURFACE),
    'WireframeContour':    ('surfaceChart', {'wireframe': '1'}, AXES_CAT_VAL, DP_SURFACE),

    # Bubble charts
    'Bubble':       ('bubbleChart', {}, AXES_VAL_VAL, DP_BUBBLE),
    'BubbleWith3D': ('bubbleChart', {'bubble3D': '1'}, AXES_VAL_VAL, DP_BUBBLE),

    # Radar charts
    'Radar':            ('radarChart', {'radarStyle': 'radar'}, AXES_CAT_VAL, DP_RADAR),
    'RadarWithMarkers': ('radarChart', {'radarStyle': 'marker'}, AXES_CAT_VAL, DP_RADAR),
    'FilledRadar':      ('radarChart', {'radarStyle': 'filled'}, AXES_CAT_VAL, DP_RADAR),
}


# --- ChartType enum value -> CombinableSeriesTypesGroup enum value ---
# Used by ChartSeriesGroup to determine the group type for a given chart type.
CHART_TYPE_TO_COMBINABLE_GROUP = {
    # Area
    'Area': 'AREA_CHART_AREA',
    'StackedArea': 'AREA_CHART_STACKED_AREA',
    'PercentsStackedArea': 'AREA_CHART_PERCENTS_STACKED_AREA',
    'Area3D': 'AREA_CHART_AREA_3D',
    'StackedArea3D': 'AREA_CHART_STACKED_AREA_3D',
    'PercentsStackedArea3D': 'AREA_CHART_PERCENTS_STACKED_AREA_3D',
    # Line
    'Line': 'LINE_CHART_LINE',
    'LineWithMarkers': 'LINE_CHART_LINE',
    'StackedLine': 'LINE_CHART_STACKED_LINE',
    'StackedLineWithMarkers': 'LINE_CHART_STACKED_LINE',
    'PercentsStackedLine': 'LINE_CHART_PERCENTS_STACKED_LINE',
    'PercentsStackedLineWithMarkers': 'LINE_CHART_PERCENTS_STACKED_LINE',
    'Line3D': 'LINE_3D_CHART',
    # Column (barChart barDir=col)
    'ClusteredColumn': 'BAR_CHART_VERT_CLUSTERED',
    'StackedColumn': 'BAR_CHART_VERT_STACKED',
    'PercentsStackedColumn': 'BAR_CHART_VERT_PERCENTS_STACKED',
    # Bar (barChart barDir=bar)
    'ClusteredBar': 'BAR_CHART_HORIZ_CLUSTERED',
    'StackedBar': 'BAR_CHART_HORIZ_STACKED',
    'PercentsStackedBar': 'BAR_CHART_HORIZ_PERCENTS_STACKED',
    # 3D Column
    'ClusteredColumn3D': 'BAR_3D_CHART_VERT_CLUSTERED',
    'StackedColumn3D': 'BAR_3D_CHART_VERT_STACKED_COLUMN_3D',
    'PercentsStackedColumn3D': 'BAR_3D_CHART_VERT_PERCENTS_STACKED_COLUMN_3D',
    'Column3D': 'BAR_3D_CHART_VERT',
    'ClusteredCylinder': 'BAR_3D_CHART_VERT_CLUSTERED',
    'StackedCylinder': 'BAR_3D_CHART_VERT_STACKED_CYLINDER',
    'PercentsStackedCylinder': 'BAR_3D_CHART_VERT_PERCENTS_STACKED_CYLINDER',
    'Cylinder3D': 'BAR_3D_CHART_VERT',
    'ClusteredCone': 'BAR_3D_CHART_VERT_CLUSTERED',
    'StackedCone': 'BAR_3D_CHART_VERT_STACKED_CONE',
    'PercentsStackedCone': 'BAR_3D_CHART_VERT_PERCENTS_STACKED_CONE',
    'Cone3D': 'BAR_3D_CHART_VERT',
    'ClusteredPyramid': 'BAR_3D_CHART_VERT_CLUSTERED',
    'StackedPyramid': 'BAR_3D_CHART_VERT_STACKED_PYRAMID',
    'PercentsStackedPyramid': 'BAR_3D_CHART_VERT_PERCENTS_STACKED_PYRAMID',
    'Pyramid3D': 'BAR_3D_CHART_VERT',
    # 3D Bar
    'ClusteredBar3D': 'BAR_3D_CHART_HORIZ_CLUSTERED',
    'StackedBar3D': 'BAR_3D_CHART_HORIZ_STACKED_BAR_3D',
    'PercentsStackedBar3D': 'BAR_3D_CHART_HORIZ_PERCENTS_STACKED_BAR_3D',
    'ClusteredHorizontalCylinder': 'BAR_3D_CHART_HORIZ_CLUSTERED',
    'StackedHorizontalCylinder': 'BAR_3D_CHART_HORIZ_STACKED_CYLINDER',
    'PercentsStackedHorizontalCylinder': 'BAR_3D_CHART_HORIZ_PERCENTS_STACKED_CYLINDER',
    'ClusteredHorizontalCone': 'BAR_3D_CHART_HORIZ_CLUSTERED',
    'StackedHorizontalCone': 'BAR_3D_CHART_HORIZ_STACKED_CONE',
    'PercentsStackedHorizontalCone': 'BAR_3D_CHART_HORIZ_PERCENTS_STACKED_CONE',
    'ClusteredHorizontalPyramid': 'BAR_3D_CHART_HORIZ_CLUSTERED',
    'StackedHorizontalPyramid': 'BAR_3D_CHART_HORIZ_STACKED_PYRAMID',
    'PercentsStackedHorizontalPyramid': 'BAR_3D_CHART_HORIZ_PERCENTS_STACKED_PYRAMID',
    # Pie
    'Pie': 'PIE_CHART',
    'ExplodedPie': 'PIE_CHART',
    'Pie3D': 'PIE_3D_CHART',
    'ExplodedPie3D': 'PIE_3D_CHART',
    'PieOfPie': 'PIE_OF_PIE_CHART',
    'BarOfPie': 'BAR_OF_PIE_CHART',
    # Doughnut
    'Doughnut': 'DOUGHNUT_CHART',
    'ExplodedDoughnut': 'DOUGHNUT_CHART',
    # Scatter
    'ScatterWithMarkers': 'SCATTER_STRAIGHT_MARKER',
    'ScatterWithStraightLines': 'SCATTER_STRAIGHT_MARKER',
    'ScatterWithStraightLinesAndMarkers': 'SCATTER_STRAIGHT_MARKER',
    'ScatterWithSmoothLines': 'SCATTER_SMOOTH_MARKER',
    'ScatterWithSmoothLinesAndMarkers': 'SCATTER_SMOOTH_MARKER',
    # Bubble
    'Bubble': 'BUBBLE_CHART',
    'BubbleWith3D': 'BUBBLE_CHART',
    # Radar
    'Radar': 'RADAR_CHART',
    'RadarWithMarkers': 'RADAR_CHART',
    'FilledRadar': 'FILLED_RADAR_CHART',
    # Stock
    'HighLowClose': 'STOCK_HIGH_LOW_CLOSE',
    'OpenHighLowClose': 'STOCK_OPEN_HIGH_LOW_CLOSE',
    'VolumeHighLowClose': 'STOCK_VOLUME_HIGH_LOW_CLOSE',
    'VolumeOpenHighLowClose': 'STOCK_VOLUME_OPEN_HIGH_LOW_CLOSE',
    # Surface
    'Surface3D': 'SURFACE_CHART_SURFACE_3D',
    'WireframeSurface3D': 'SURFACE_CHART_WIREFRAME_SURFACE_3D',
    'Contour': 'SURFACE_CHART_CONTOUR',
    'WireframeContour': 'SURFACE_CHART_WIREFRAME_CONTOUR',
}


def get_combinable_group(chart_type_value: str) -> str | None:
    """Return CombinableSeriesTypesGroup enum member name for a ChartType value."""
    return CHART_TYPE_TO_COMBINABLE_GROUP.get(chart_type_value)


def get_chart_type_info(chart_type_value: str):
    """
    Get chart type info tuple for a ChartType enum value.

    Returns (xml_tag, attrs_dict, axis_config, dp_family) or None.
    """
    return CHART_TYPE_INFO.get(chart_type_value)


# ChartType enum value -> OOXML <c:shape val="..."> for bar3DChart variants.
# Cylinder/cone/pyramid types share the bar3DChart element and only differ
# by this attribute on each <c:ser> and on the chart-type element.
_CYLINDER_TYPES = {
    'ClusteredCylinder', 'StackedCylinder', 'PercentsStackedCylinder', 'Cylinder3D',
    'ClusteredHorizontalCylinder', 'StackedHorizontalCylinder',
    'PercentsStackedHorizontalCylinder',
}
_CONE_TYPES = {
    'ClusteredCone', 'StackedCone', 'PercentsStackedCone', 'Cone3D',
    'ClusteredHorizontalCone', 'StackedHorizontalCone',
    'PercentsStackedHorizontalCone',
}
_PYRAMID_TYPES = {
    'ClusteredPyramid', 'StackedPyramid', 'PercentsStackedPyramid', 'Pyramid3D',
    'ClusteredHorizontalPyramid', 'StackedHorizontalPyramid',
    'PercentsStackedHorizontalPyramid',
}


def get_bar3d_shape(chart_type_value: str) -> str | None:
    """Return 'cylinder'|'cone'|'pyramid' for shaped bar3D types, else None."""
    if chart_type_value in _CYLINDER_TYPES:
        return 'cylinder'
    if chart_type_value in _CONE_TYPES:
        return 'cone'
    if chart_type_value in _PYRAMID_TYPES:
        return 'pyramid'
    return None


# Reverse mapping: XML tag -> list of possible ChartType values
# Used when loading existing charts to determine ChartType from XML
_XML_TAG_TO_CHART_TYPES: dict[str, list[str]] = {}
for _ct_val, (_tag, _attrs, _axes, _dp) in CHART_TYPE_INFO.items():
    _XML_TAG_TO_CHART_TYPES.setdefault(_tag, []).append(_ct_val)


def detect_chart_type_from_xml(xml_tag: str, attrs: dict[str, str]) -> str | None:
    """
    Detect ChartType enum value from XML element tag and attributes.

    Args:
        xml_tag: Local name of the chart type element (e.g., 'barChart')
        attrs: Dict of child element values (e.g., {'barDir': 'col', 'grouping': 'clustered'})

    Returns:
        ChartType enum value string, or None if unknown.
    """
    candidates = _XML_TAG_TO_CHART_TYPES.get(xml_tag, [])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    # Find best match by attributes
    best = None
    best_score = -1
    for ct_val in candidates:
        _, expected_attrs, _, _ = CHART_TYPE_INFO[ct_val]
        score = sum(1 for k, v in expected_attrs.items() if attrs.get(k) == v)
        if score > best_score:
            best_score = score
            best = ct_val
    return best
