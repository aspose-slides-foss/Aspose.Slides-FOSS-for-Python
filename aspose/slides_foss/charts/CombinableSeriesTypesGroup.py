from __future__ import annotations
from enum import Enum

class CombinableSeriesTypesGroup(Enum):
    """Enumeration of groups of combinable series types. Each element relates to group of types of chart series that can persist simultaneously in one ChartSeriesGroup. For example: ChartType.PercentsStackedArea series cannot be simultaneously with ChartType.StackedArea series in one ChartSeriesGroup. But two or more ChartType.PercentsStackedArea can be in one ChartSeriesGroup simultaneously (CombinableSeriesTypesGroup.AreaChart_PercentsStackedArea). And ChartType.Line series can be with ChartType.LineWithMarkers series simultaneously in one CombinableSeriesTypesGroup.LineChart_Line ChartSeriesGroup."""
    AREA_CHART_AREA = 'AreaChart_Area'  # Groups this set of series types: { ChartType.Area }
    AREA_CHART_PERCENTS_STACKED_AREA = 'AreaChart_PercentsStackedArea'  # Groups this set of series types: { ChartType.PercentsStackedArea }
    AREA_CHART_STACKED_AREA = 'AreaChart_StackedArea'  # Groups this set of series types: { ChartType.StackedArea }
    AREA_CHART_AREA_3D = 'AreaChart_Area3D'  # Groups this set of series types: { ChartType.Area3D }
    AREA_CHART_STACKED_AREA_3D = 'AreaChart_StackedArea3D'  # Groups this set of series types: { ChartType.StackedArea3D }
    AREA_CHART_PERCENTS_STACKED_AREA_3D = 'AreaChart_PercentsStackedArea3D'  # Groups this set of series types: { ChartType.PercentsStackedArea3D }
    LINE_CHART_LINE = 'LineChart_Line'  # Groups this set of series types: { ChartType.Line, ChartType.LineWithMarkers }
    LINE_CHART_STACKED_LINE = 'LineChart_StackedLine'  # Groups this set of series types: { ChartType.StackedLine, ChartType.StackedLineWithMarkers }
    LINE_CHART_PERCENTS_STACKED_LINE = 'LineChart_PercentsStackedLine'  # Groups this set of series types: { ChartType.PercentsStackedLine, ChartType.PercentsStackedLineWithMarkers }
    LINE_3D_CHART = 'Line3DChart'  # Groups this set of series types: { ChartType.Line3D }
    STOCK_HIGH_LOW_CLOSE = 'StockHighLowClose'  # Groups this set of series types: { ChartType.HighLowClose }
    STOCK_OPEN_HIGH_LOW_CLOSE = 'StockOpenHighLowClose'  # Groups this set of series types: { ChartType.OpenHighLowClose }
    STOCK_VOLUME_HIGH_LOW_CLOSE = 'StockVolumeHighLowClose'  # Groups this set of series types: { ChartType.VolumeHighLowClose }
    STOCK_VOLUME_OPEN_HIGH_LOW_CLOSE = 'StockVolumeOpenHighLowClose'  # Groups this set of series types: { ChartType.VolumeOpenHighLowClose }
    RADAR_CHART = 'RadarChart'  # Groups this set of series types: { ChartType.Radar, ChartType.RadarWithMarkers }
    FILLED_RADAR_CHART = 'FilledRadarChart'  # Groups this set of series types: { ChartType.FilledRadar }
    SCATTER_STRAIGHT_MARKER = 'ScatterStraightMarker'  # Groups this set of series types: { ChartType.ScatterWithMarkers, ChartType.ScatterWithStraightLines, ChartType.ScatterWithStraightLinesAndMarkers }
    SCATTER_SMOOTH_MARKER = 'ScatterSmoothMarker'  # Groups this set of series types: { ChartType.ScatterWithSmoothLines, ChartType.ScatterWithSmoothLinesAndMarkers }
    PIE_CHART = 'PieChart'  # Groups this set of series types: { ChartType.Pie, ChartType.ExplodedPie }
    PIE_3D_CHART = 'Pie3DChart'  # Groups this set of series types: { ChartType.Pie3D, ChartType.ExplodedPie3D }
    DOUGHNUT_CHART = 'DoughnutChart'  # Groups this set of series types: { ChartType.Doughnut, ChartType.ExplodedDoughnut }
    BAR_CHART_VERT_CLUSTERED = 'BarChart_VertClustered'  # Groups this set of series types: { ChartType.ClusteredColumn }
    BAR_CHART_VERT_STACKED = 'BarChart_VertStacked'  # Groups this set of series types: { ChartType.StackedColumn }
    BAR_CHART_VERT_PERCENTS_STACKED = 'BarChart_VertPercentsStacked'  # Groups this set of series types: { ChartType.PercentsStackedColumn }
    BAR_CHART_HORIZ_CLUSTERED = 'BarChart_HorizClustered'  # Groups this set of series types: { ChartType.ClusteredBar }
    BAR_CHART_HORIZ_STACKED = 'BarChart_HorizStacked'  # Groups this set of series types: { ChartType.StackedBar }
    BAR_CHART_HORIZ_PERCENTS_STACKED = 'BarChart_HorizPercentsStacked'  # Groups this set of series types: { ChartType.PercentsStackedBar }
    BAR_3D_CHART_VERT = 'Bar3DChart_Vert'  # Groups this set of series types: { ChartType.Column3D, ChartType.Cylinder3D, ChartType.Cone3D, ChartType.Pyramid3D }
    BAR_3D_CHART_VERT_CLUSTERED = 'Bar3DChart_VertClustered'  # Groups this set of series types: { ChartType.ClusteredColumn3D, ChartType.ClusteredCone, ChartType.ClusteredCylinder, ChartType.ClusteredPyramid }
    BAR_3D_CHART_VERT_PERCENTS_STACKED_COLUMN_3D = 'Bar3DChart_VertPercentsStackedColumn3D'  # Groups this set of series types: { ChartType.PercentsStackedColumn3D }
    BAR_3D_CHART_VERT_PERCENTS_STACKED_CONE = 'Bar3DChart_VertPercentsStackedCone'  # Groups this set of series types: { ChartType.PercentsStackedCone }
    BAR_3D_CHART_VERT_PERCENTS_STACKED_CYLINDER = 'Bar3DChart_VertPercentsStackedCylinder'  # Groups this set of series types: { ChartType.PercentsStackedCylinder }
    BAR_3D_CHART_VERT_PERCENTS_STACKED_PYRAMID = 'Bar3DChart_VertPercentsStackedPyramid'  # Groups this set of series types: { ChartType.PercentsStackedPyramid }
    BAR_3D_CHART_VERT_STACKED_COLUMN_3D = 'Bar3DChart_VertStackedColumn3D'  # Groups this set of series types: { ChartType.StackedColumn3D }
    BAR_3D_CHART_VERT_STACKED_CONE = 'Bar3DChart_VertStackedCone'  # Groups this set of series types: { ChartType.StackedCone }
    BAR_3D_CHART_VERT_STACKED_CYLINDER = 'Bar3DChart_VertStackedCylinder'  # Groups this set of series types: { ChartType.StackedCylinder }
    BAR_3D_CHART_VERT_STACKED_PYRAMID = 'Bar3DChart_VertStackedPyramid'  # Groups this set of series types: { ChartType.StackedPyramid }
    BAR_3D_CHART_HORIZ_CLUSTERED = 'Bar3DChart_HorizClustered'  # Groups this set of series types: { ChartType.ClusteredBar3D, ChartType.ClusteredHorizontalCone, ChartType.ClusteredHorizontalCylinder, ChartType.ClusteredHorizontalPyramid }
    BAR_3D_CHART_HORIZ_STACKED_BAR_3D = 'Bar3DChart_HorizStackedBar3D'  # Groups this set of series types: { ChartType.StackedBar3D }
    BAR_3D_CHART_HORIZ_STACKED_CONE = 'Bar3DChart_HorizStackedCone'  # Groups this set of series types: { ChartType.StackedHorizontalCone }
    BAR_3D_CHART_HORIZ_STACKED_CYLINDER = 'Bar3DChart_HorizStackedCylinder'  # Groups this set of series types: { ChartType.StackedHorizontalCylinder }
    BAR_3D_CHART_HORIZ_STACKED_PYRAMID = 'Bar3DChart_HorizStackedPyramid'  # Groups this set of series types: { ChartType.StackedHorizontalPyramid }
    BAR_3D_CHART_HORIZ_PERCENTS_STACKED_BAR_3D = 'Bar3DChart_HorizPercentsStackedBar3D'  # Groups this set of series types: { ChartType.PercentsStackedBar3D }
    BAR_3D_CHART_HORIZ_PERCENTS_STACKED_CONE = 'Bar3DChart_HorizPercentsStackedCone'  # Groups this set of series types: { ChartType.PercentsStackedHorizontalCone }
    BAR_3D_CHART_HORIZ_PERCENTS_STACKED_CYLINDER = 'Bar3DChart_HorizPercentsStackedCylinder'  # Groups this set of series types: { ChartType.PercentsStackedHorizontalCylinder }
    BAR_3D_CHART_HORIZ_PERCENTS_STACKED_PYRAMID = 'Bar3DChart_HorizPercentsStackedPyramid'  # Groups this set of series types: { ChartType.PercentsStackedHorizontalPyramid }
    BAR_OF_PIE_CHART = 'BarOfPieChart'  # Groups this set of series types: { ChartType.BarOfPie }
    PIE_OF_PIE_CHART = 'PieOfPieChart'  # Groups this set of series types: { ChartType.PieOfPie }
    SURFACE_CHART_CONTOUR = 'SurfaceChart_Contour'  # Groups this set of series types: { ChartType.Contour }
    SURFACE_CHART_WIREFRAME_CONTOUR = 'SurfaceChart_WireframeContour'  # Groups this set of series types: { ChartType.WireframeContour }
    SURFACE_CHART_SURFACE_3D = 'SurfaceChart_Surface3D'  # Groups this set of series types: { ChartType.Surface3D }
    SURFACE_CHART_WIREFRAME_SURFACE_3D = 'SurfaceChart_WireframeSurface3D'  # Groups this set of series types: { ChartType.WireframeSurface3D }
    BUBBLE_CHART = 'BubbleChart'  # Groups this set of series types: { ChartType.Bubble, ChartType.BubbleWith3D }
