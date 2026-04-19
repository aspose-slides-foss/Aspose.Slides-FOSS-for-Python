"""Tests for error bar support on chart series."""
import os, tempfile, pytest
from aspose.slides_foss import Presentation
from aspose.slides_foss.export import SaveFormat
from aspose.slides_foss.charts import (
    ChartType, ErrorBarType, ErrorBarValueType, DataSourceType,
    ErrorBarsFormat, ErrorBarsCustomValues, DataSourceTypeForErrorBarsCustomValues,
)


def _save_and_reload(prs):
    with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as f:
        path = f.name
    try:
        prs.save(path, SaveFormat.PPTX)
        return Presentation(path)
    finally:
        os.unlink(path)


# --- Availability tests ---

class TestErrorBarAvailability:
    def test_line_has_y_only(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.LINE, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        assert s.error_bars_y_format is not None
        assert s.error_bars_x_format is None

    def test_scatter_has_both(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.SCATTER_WITH_SMOOTH_LINES, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        assert s.error_bars_x_format is not None
        assert s.error_bars_y_format is not None

    def test_column_has_y_only(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        assert s.error_bars_y_format is not None
        assert s.error_bars_x_format is None

    def test_pie_has_none(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.PIE, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        assert s.error_bars_y_format is None
        assert s.error_bars_x_format is None

    def test_bubble_has_both(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.BUBBLE, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        assert s.error_bars_x_format is not None
        assert s.error_bars_y_format is not None


# --- Fixed error bar round-trip ---

class TestFixedErrorBars:
    def test_y_fixed_round_trip(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.LINE, 0, 0, 300, 200)
        eb = chart.chart_data.series[0].error_bars_y_format
        eb.is_visible = True
        eb.value_type = ErrorBarValueType.FIXED
        eb.value = 5.0
        eb.type = ErrorBarType.BOTH
        eb.has_end_cap = True

        prs2 = _save_and_reload(prs)
        eb2 = prs2.slides[0].shapes[0].chart_data.series[0].error_bars_y_format
        assert eb2.is_visible is True
        assert eb2.value_type == ErrorBarValueType.FIXED
        assert eb2.value == 5.0
        assert eb2.type == ErrorBarType.BOTH
        assert eb2.has_end_cap is True

    def test_percentage_plus_no_end_cap(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.SCATTER_WITH_SMOOTH_LINES, 0, 0, 300, 200)
        eb = chart.chart_data.series[0].error_bars_x_format
        eb.is_visible = True
        eb.value_type = ErrorBarValueType.PERCENTAGE
        eb.value = 10.0
        eb.type = ErrorBarType.PLUS
        eb.has_end_cap = False

        prs2 = _save_and_reload(prs)
        eb2 = prs2.slides[0].shapes[0].chart_data.series[0].error_bars_x_format
        assert eb2.value_type == ErrorBarValueType.PERCENTAGE
        assert eb2.value == 10.0
        assert eb2.type == ErrorBarType.PLUS
        assert eb2.has_end_cap is False

    def test_minus_direction(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 300, 200)
        eb = chart.chart_data.series[0].error_bars_y_format
        eb.is_visible = True
        eb.value_type = ErrorBarValueType.FIXED
        eb.value = 3.0
        eb.type = ErrorBarType.MINUS

        prs2 = _save_and_reload(prs)
        eb2 = prs2.slides[0].shapes[0].chart_data.series[0].error_bars_y_format
        assert eb2.type == ErrorBarType.MINUS
        assert eb2.value == 3.0


# --- Custom error bar round-trip ---

class TestCustomErrorBars:
    def test_custom_y_values_round_trip(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 300, 200)
        series = chart.chart_data.series[0]

        eb = series.error_bars_y_format
        eb.is_visible = True
        eb.value_type = ErrorBarValueType.CUSTOM

        points = series.data_points
        points.data_source_type_for_error_bars_custom_values.data_source_type_for_y_minus_values = DataSourceType.DOUBLE_LITERALS
        points.data_source_type_for_error_bars_custom_values.data_source_type_for_y_plus_values = DataSourceType.DOUBLE_LITERALS

        for i in range(len(points)):
            points[i].error_bars_custom_values.y_minus.as_literal_double = (i + 1) * 0.5
            points[i].error_bars_custom_values.y_plus.as_literal_double = (i + 1) * 1.0

        prs2 = _save_and_reload(prs)
        s2 = prs2.slides[0].shapes[0].chart_data.series[0]
        eb2 = s2.error_bars_y_format
        assert eb2.is_visible is True
        assert eb2.value_type == ErrorBarValueType.CUSTOM

        for i in range(len(s2.data_points)):
            cv = s2.data_points[i].error_bars_custom_values
            assert cv.y_plus.as_literal_double == (i + 1) * 1.0
            assert cv.y_minus.as_literal_double == (i + 1) * 0.5

    def test_custom_x_values_on_scatter(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.SCATTER_WITH_SMOOTH_LINES, 0, 0, 300, 200)
        series = chart.chart_data.series[0]

        eb = series.error_bars_x_format
        eb.is_visible = True
        eb.value_type = ErrorBarValueType.CUSTOM

        points = series.data_points
        for i in range(len(points)):
            points[i].error_bars_custom_values.x_plus.as_literal_double = i * 2.0
            points[i].error_bars_custom_values.x_minus.as_literal_double = i * 1.5

        prs2 = _save_and_reload(prs)
        s2 = prs2.slides[0].shapes[0].chart_data.series[0]
        eb2 = s2.error_bars_x_format
        assert eb2.value_type == ErrorBarValueType.CUSTOM

        for i in range(len(s2.data_points)):
            cv = s2.data_points[i].error_bars_custom_values
            assert cv.x_plus.as_literal_double == i * 2.0
            assert cv.x_minus.as_literal_double == i * 1.5


# --- Invisible error bars should not write XML ---

class TestInvisibleErrorBars:
    def test_invisible_not_written(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.LINE, 0, 0, 300, 200)
        # Don't set is_visible — should remain False
        eb = chart.chart_data.series[0].error_bars_y_format
        assert eb.is_visible is False

        prs2 = _save_and_reload(prs)
        s2 = prs2.slides[0].shapes[0].chart_data.series[0]
        # After round-trip, since nothing was written, the format object should
        # exist but not be visible (it's created by default for supported types)
        assert s2.error_bars_y_format.is_visible is False


# --- DataSourceTypeForErrorBarsCustomValues ---

class TestDataSourceTypeForErrorBarsCustomValues:
    def test_default_values(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 300, 200)
        dst = chart.chart_data.series[0].data_points.data_source_type_for_error_bars_custom_values
        assert dst.data_source_type_for_x_minus_values == DataSourceType.DOUBLE_LITERALS
        assert dst.data_source_type_for_x_plus_values == DataSourceType.DOUBLE_LITERALS
        assert dst.data_source_type_for_y_minus_values == DataSourceType.DOUBLE_LITERALS
        assert dst.data_source_type_for_y_plus_values == DataSourceType.DOUBLE_LITERALS

    def test_setter(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 300, 200)
        dst = chart.chart_data.series[0].data_points.data_source_type_for_error_bars_custom_values
        dst.data_source_type_for_y_plus_values = DataSourceType.WORKSHEET
        assert dst.data_source_type_for_y_plus_values == DataSourceType.WORKSHEET


# --- ErrorBarsCustomValues lazy init ---

class TestErrorBarsCustomValues:
    def test_lazy_init(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(ChartType.CLUSTERED_COLUMN, 0, 0, 300, 200)
        dp = chart.chart_data.series[0].data_points[0]
        cv = dp.error_bars_custom_values
        assert cv is not None
        assert cv.x_plus.as_literal_double == 0.0
        assert cv.y_minus.as_literal_double == 0.0
        # Same object on second access
        assert dp.error_bars_custom_values is cv
