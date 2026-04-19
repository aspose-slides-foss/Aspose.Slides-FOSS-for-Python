"""Tests for chart data markers (Marker)."""
from aspose.slides_foss import Presentation, FillType
from aspose.slides_foss.drawing import Color
from aspose.slides_foss.charts import ChartType, MarkerStyleType


class TestSeriesMarker:
    def test_default_symbol_is_not_defined(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        assert s.marker.symbol == MarkerStyleType.NOT_DEFINED
        assert s.marker.size == 0

    def test_set_symbol_and_size(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        s.marker.symbol = MarkerStyleType.CIRCLE
        s.marker.size = 12
        assert s.marker.symbol == MarkerStyleType.CIRCLE
        assert s.marker.size == 12

    def test_all_symbol_values(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        for sym in (MarkerStyleType.CIRCLE, MarkerStyleType.DASH,
                    MarkerStyleType.DIAMOND, MarkerStyleType.DOT,
                    MarkerStyleType.NONE, MarkerStyleType.PICTURE,
                    MarkerStyleType.PLUS, MarkerStyleType.SQUARE,
                    MarkerStyleType.STAR, MarkerStyleType.TRIANGLE,
                    MarkerStyleType.X):
            s.marker.symbol = sym
            assert s.marker.symbol == sym

    def test_reset_symbol_to_not_defined(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        s.marker.symbol = MarkerStyleType.SQUARE
        s.marker.symbol = MarkerStyleType.NOT_DEFINED
        assert s.marker.symbol == MarkerStyleType.NOT_DEFINED

    def test_round_trip_symbol_and_size(self, tmp_pptx):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        chart.chart_data.series[0].marker.symbol = MarkerStyleType.TRIANGLE
        chart.chart_data.series[0].marker.size = 15

        prs2 = tmp_pptx(prs)
        s = prs2.slides[0].shapes[0].chart_data.series[0]
        assert s.marker.symbol == MarkerStyleType.TRIANGLE
        assert s.marker.size == 15

    def test_round_trip_format_fill(self, tmp_pptx):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        s.marker.symbol = MarkerStyleType.CIRCLE
        s.marker.size = 10
        s.marker.format.fill.fill_type = FillType.SOLID
        s.marker.format.fill.solid_fill_color.color = Color.from_argb(255, 200, 50, 80)

        prs2 = tmp_pptx(prs)
        s2 = prs2.slides[0].shapes[0].chart_data.series[0]
        assert s2.marker.symbol == MarkerStyleType.CIRCLE
        assert s2.marker.size == 10
        assert s2.marker.format.fill.fill_type == FillType.SOLID
        c = s2.marker.format.fill.solid_fill_color.color
        assert (c.r, c.g, c.b) == (200, 50, 80)


class TestDataPointMarker:
    def test_per_point_marker_overrides_series(self, tmp_pptx):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        s.marker.symbol = MarkerStyleType.CIRCLE
        s.marker.size = 8

        dp0 = s.data_points[0]
        dp0.marker.symbol = MarkerStyleType.DIAMOND
        dp0.marker.size = 16

        assert dp0.marker.symbol == MarkerStyleType.DIAMOND
        assert dp0.marker.size == 16

        prs2 = tmp_pptx(prs)
        s2 = prs2.slides[0].shapes[0].chart_data.series[0]
        assert s2.marker.symbol == MarkerStyleType.CIRCLE
        assert s2.marker.size == 8
        assert s2.data_points[0].marker.symbol == MarkerStyleType.DIAMOND
        assert s2.data_points[0].marker.size == 16

    def test_untouched_point_has_no_marker_override(self):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        # Reading marker must not create a <c:dPt> (no symbol, no size).
        _ = s.data_points[1].marker.symbol
        _ = s.data_points[1].marker.size
        assert s._dpt_elems == {}

    def test_per_point_format_round_trip(self, tmp_pptx):
        prs = Presentation()
        chart = prs.slides[0].shapes.add_chart(
            ChartType.LINE_WITH_MARKERS, 0, 0, 300, 200)
        s = chart.chart_data.series[0]
        dp = s.data_points[2]
        dp.marker.symbol = MarkerStyleType.STAR
        dp.marker.format.fill.fill_type = FillType.SOLID
        dp.marker.format.fill.solid_fill_color.color = Color.from_argb(255, 0, 128, 64)

        prs2 = tmp_pptx(prs)
        dp2 = prs2.slides[0].shapes[0].chart_data.series[0].data_points[2]
        assert dp2.marker.symbol == MarkerStyleType.STAR
        assert dp2.marker.format.fill.fill_type == FillType.SOLID
        c = dp2.marker.format.fill.solid_fill_color.color
        assert (c.r, c.g, c.b) == (0, 128, 64)
